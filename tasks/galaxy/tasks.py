import sys
import json
from time import sleep
from celery import Celery
from bioblend import galaxy

from tasks import config
from tasks.galaxy import galaxydata
from tasks.galaxy.util import get_galaxy_instance

TESTING_FLAG = True

# worker module for running workflow mods

app = Celery('galaxy_workflows', backend='amqp')
app.conf.update(
    BROKER_HOST=config.BROKER_URL,
    BROKER_PORT=config.BROKER_PORT,
    CELERY_TASK_SERIALIZER=config.CELERY_TASK_SERIALIZER,
    CELERY_ACCEPT_CONTENT=[config.CELERY_TASK_SERIALIZER],
)
if TESTING_FLAG:
    app.conf.update(
        CELERY_ACKS_LATE=True
    )


@app.task(queue=config.QUEUE_GALAXY_WORKFLOW, bind=True)
def reuse_history(self, inputstore):
    input_labels = inputstore['wf']['rerun_inputs']
    print('Checking reusable other history for datasets for '
          'input steps {}'.format(input_labels))
    gi = get_galaxy_instance(inputstore)
    try:
        update_inputstore_from_history(gi, inputstore['datasets'],
                                       input_labels, inputstore['history'])
        history = gi.histories.create_history(name=inputstore['searchname'])
    except:
        self.retry(countdown=60)
    inputstore['history'] = history['id']
    return inputstore


@app.task(queue=config.QUEUE_GALAXY_WORKFLOW, bind=True)
def run_workflow_module(self, inputstore, module_id):
    print('Getting workflow module {}'.format(module_id))
    gi = get_galaxy_instance(inputstore)
    try:
        module = gi.workflows.show_workflow(module_id)
    except:
        self.retry(countdown=60)
    input_labels = get_input_labels(module)
    while not check_inputs_ready(inputstore['datasets'], input_labels,
                                 module['name']):
        try:
            update_inputstore_from_history(gi, inputstore['datasets'],
                                           input_labels,
                                           inputstore['history'])
        except:
            self.retry(countdown=60)
        sleep(10)
    mod_inputs = get_input_map(module, inputstore['datasets'])
    mod_params = get_param_map(module, inputstore)
    print('Invoking workflow {} with id {}'.format(module['name'],
                                                   module['id']))
    try:
        gi.workflows.invoke_workflow(module['id'], inputs=mod_inputs,
                                     params=mod_params,
                                     history_id=inputstore['history'])
    except:
        self.retry(countdown=60)
    print('Workflow invoked')
    return inputstore


def get_input_labels(wf):
    names = []
    for wfinput in wf['inputs'].values():
        names.append(wfinput['label'])
    return names


def check_inputs_ready(inputstore, inputnames, modname):
    print('Checking inputs {} for module {}'.format(inputnames, modname))
    ready, missing = True, []
    for name in inputnames:
        if inputstore[name]['id'] is None:
            missing.append(name)
            ready = False
    if not ready:
        print('Missing inputs for module {}: '
              '{}'.format(modname, ', '.join(missing)))
    else:
        print('All inputs found for module {}'.format(modname))
    return ready


def update_inputstore_from_history(gi, inputstore, input_names, history_id):
    print('Getting history contents')
    his_contents = gi.histories.show_history(history_id, contents=True,
                                             deleted=False)
    for dset in his_contents:
        name = dset['name']
        if name in input_names and inputstore[name]['id'] is None:
            print('found dset {}'.format(name))
            if inputstore[name]['src'] == 'hdca':
                inputstore[name]['id'] = get_collection_id_in_his(his_contents,
                                                                  name, gi)
            elif inputstore[name]['src'] == 'hda':
                inputstore[name]['id'] = dset['id']


def get_input_map(module, inputstore):
    inputmap = {}
    for modinput in module['inputs'].values():
        inputmap[modinput['uuid']] = {
            'id': inputstore[modinput['label']]['id'],
            'src': inputstore[modinput['label']]['src'],
        }
    return inputmap


def get_param_map(module, inputstore):
    parammap = {}
    for modstep in module['steps'].values():
        for input_name, input_val in modstep['tool_inputs'].items():
            try:
                input_val = json.loads(input_val)
            except json.decoder.JSONDecodeError:
                # no json obj, no runtime values
                continue
            print('after', input_val)
            if type(input_val) == dict:
                # FIXME do_dict_stuff()
                print('dict found, values', input_val.values())
                if dict in [type(x) for x in input_val.values()]:
                    print('contains a possible runtime dict')
                    # complex input with repeats/conditional
                    for subname, subval in input_val.items():
                        composed_name = '{}|{}'.format(input_name, subname)
                        if is_runtime_param(subval, composed_name, modstep):
                            fill_runtime_param(parammap, inputstore,
                                               composed_name, modstep,
                                               input_name)
                else:
                    # simple runtime value check and fill with inputstore value
                    # FIXME do_runtime_stuff()
                    print('no dict inside')
                    if is_runtime_param(input_val, input_name, modstep):
                        print('but is a runtimer')
                        fill_runtime_param(parammap, inputstore, input_name,
                                           modstep)
    print(parammap)
    return parammap


def get_collection_id_in_his(his_contents, name, gi):
    print('Trying to find collection ID belonging to dataset {}'.format(name))
    labelfound = False
    for dset in his_contents:
        if dset['name'] == name:
            labelfound = True
        if labelfound and dset['type'] == 'collection':
            dcol = gi.histories.show_dataset_collection(dset['history_id'],
                                                        dset['id'])
            if set([x['object']['name'] for x in dcol['elements']]) == {name}:
                print('Correct, using {} id {}'.format(dset['name'],
                                                       dset['id']))
                return dset['id']
    print('No matching collection in history (yet)')
    return None


def is_runtime_param(val, name, step):
    print('checking', name, val)
    try:
        isruntime = val['__class__'] == 'RuntimeValue'
    except TypeError:
        print('No Runtime at all')
        return False
    except KeyError:
        print('No Runtime at all, but is a dict anyway')
        return False
    else:
        if isruntime and name not in step['input_steps']:
            print('Proper Runtime param, not input step')
            return True
        print('Runtime but also input step so no param')
        return False


def fill_runtime_param(parammap, inputstore, name, step, storename=False):
    if not storename:
        storename = name
    print('filling parammap for tool {}'.format(step['tool_id']))
    print('param name: {}'.format(name))
    print('storename: {}'.format(storename))
    print(inputstore['params'])
    try:
        paramval = inputstore['params'][storename]
    except KeyError:
        print('WARNING! no input param found for name {}'.format(name))
    else:
        parammap[step['tool_id']] = {'param': name, 'value': paramval}


@app.task(queue=config.QUEUE_GALAXY_WORKFLOW, bind=True)
def check_dsets_ok(self, inputstore):
    # FIXME have to check datasets are ok, no history clean bc it doesnt exist
    # yet
    print('Not currently checking dsets are ok... please implement me!')
    return inputstore


@app.task(queue=config.QUEUE_GALAXY_WORKFLOW, bind=True)
def prepare_run(self, inputstore):
    gi = get_galaxy_instance(inputstore)
    print('Creating new history for: {}'.format(inputstore['searchname']))
    try:
        check_modules(gi, inputstore['modules'])
        history = gi.histories.create_history(name=inputstore['searchname'])
    except:
        self.retry(countdown=60)
    inputstore['history'] = history['id']
    if inputstore['rerun_his'] is None:
        try:
            run_prep_tools(gi, inputstore)
        except:
            self.retry(countdown=60)
    return inputstore


def run_prep_tools(gi, inputstore):
    """Runs expdata (to be deprecated) and mslookup spectra. Not in normal WF
    because they need a repeat param setnames passed to them, not yet possible
    to call on WF API"""
    spectra = {'src': 'hdca', 'id': inputstore['datasets']['spectra']['id']}
    expdata_inputs = {'percopoolsize': inputstore['params']['ppoolsize'],
                      'spectra': spectra,
                      'isoquant': inputstore['params']['isobtype']}
    for count, (set_id, set_name) in enumerate(
            zip(inputstore['params']['setpatterns'],
                inputstore['params']['setnames'])):
        expdata_inputs['pools_{}|set_identifier'.format(str(count))] = set_id
        expdata_inputs['pools_{}|set_name'.format(str(count))] = set_name
    print('Running sample pool tool')
    pooltool = gi.tools.get_tools(tool_id='experiment_data')[0]
    expdata = gi.tools.run_tool(inputstore['history'], pooltool['id'],
                                tool_inputs=expdata_inputs)['outputs'][0]
    gi.histories.update_dataset(expdata['history_id'], expdata['id'],
                                name='expdata')
    print('Running lookup spectra tool')
    mslookuptool = gi.tools.get_tools(tool_id='mslookup_spectra')[0]
    speclookup = gi.tools.run_tool(inputstore['history'], mslookuptool['id'],
                                   tool_inputs=expdata_inputs)['outputs'][0]
    gi.histories.update_dataset(speclookup['history_id'], speclookup['id'],
                                name='spectra lookup')


def check_modules(gi, modules):
    deleted_error = False
    galaxy_modules = []
    for mod_id in modules:
        mod_name = {v: k for k, v in galaxydata.wf_modules.items()}[mod_id]
        print('Checking module {}: fetching workflow for {}'.format(mod_name,
                                                                    mod_id))
        try:
            module = gi.workflows.show_workflow(mod_id)
        except KeyError:
            raise RuntimeError('Cannot find module name {} in local module '
                               'collection. Check for spelling error or '
                               'update local collection.'.format(mod_name))
        except galaxy.client.ConnectionError:
            raise RuntimeError('Cannot find module {} with UUID {} on the '
                               'Galaxy server. Check that the correct UUID '
                               'has been passed.'.format(mod_name, mod_id))
        else:
            if module['deleted']:
                deleted_error = True
                print('Workflow module {} with UUID {} has been '
                      'deleted on Galaxy server, please use '
                      'latest UUID'.format(module['name'], mod_id))
            else:
                galaxy_modules.append(module)
    if deleted_error:
        print('Invalid workflow UUIDs have been specified, exiting')
        sys.exit(1)
    return galaxy_modules
