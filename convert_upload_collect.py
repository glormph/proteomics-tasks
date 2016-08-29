import os
import sys
import argparse
from getpass import getpass
from celery import chain
import ftplib
from paramiko import rsakey

from tasks import config
from tasks.storage import tasks
from tasks.galaxy import tasks as galaxytasks


def main():
    inputstore = {'winshare': config.WIN_STORAGESHARE,
                  'storageshare': config.STORAGESHARE,
                  'galaxy_url': config.GALAXY_URL,
                  'rawfiles': [],
                  'mzmls': [],
                  'g_import_celerytasks': [],
                  }
    parse_commandline(inputstore)
    inputstore['apikey'] = config.USERS[inputstore['user']][1]
    ftpuser = config.USERS[inputstore['user']][0]
    ftppass = getpass('Galaxy password for FTP:')
    test_ftp(config.FTPSERVER, config.FTPPORT, ftpuser, ftppass)
    scpkey = rsakey.RSAKey()
    scpkey.from_private_key_file(config.SCPKEYFILE)
    for directory in inputstore['storage_directories']:
        in_directory = os.path.join(config.STORAGESHARE, directory)
        rawfiles = get_files_directory(in_directory, 'raw')
        for fn in rawfiles:
            inputstore['rawfiles'].append(os.path.join(in_directory, fn))
            win_rawfile = os.path.join(config.WINSHARE, directory, fn)
            res = chain(tasks.convert_to_mzml.s(win_rawfile, inputstore),
                        tasks.scp_storage.s(inputstore, config.SCP_URL,
                                            config.SCP_LOGIN, scpkey),
                        tasks.ftp_transfer.s(config.FTPSERVER, config.FTPPORT,
                                             ftpuser, ftppass,
                                             inputstore['ftpdir']),
                        galaxytasks.import_file_to_history.s(inputstore)
                        )()
            inputstore['g_import_celerytasks'].append(res.task_id)
    print('Queued', len(inputstore['rawfiles']), 'files for conversion')
    res = chain(tasks.wait_for_imported.s(),
                galaxytasks.put_files_in_collection.s())()
    print('Queued waiting and collecting mzmls to galaxy, task_id is:')
    print(res.id)


def get_files_directory(directory, extension):
    rawfiles = []
    if not os.path.exists(directory):
        raise RuntimeError('Cannot find directory {0}'.format(directory))
    for fn in sorted(os.listdir(directory)):
        if os.path.splitext(fn)[-1] == '.{}'.format(extension):
            rawfiles.append(fn)
        else:
            print('Skipping non-raw file {0}'.format(fn))
    return rawfiles


def parse_commandline(inputstore):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-u', dest='user')
    parser.add_argument('--rawdirs', dest='rawdirs', nargs='+')
    parser.add_argument('--ftpdir', dest='ftpdir')
    args = parser.parse_args(sys.argv[1:])
    inputstore['user'] = args.user
    inputstore['storage_directories'] = args.rawdirs
    inputstore['ftpdir'] = args.ftpdir


def test_ftp(server, port, ftpuser, ftppass):
    print('Testing FTP connection')
    ftpcon = ftplib.FTP()
    try:
        ftpcon.connect(server, port)
    except:
        print('Could not connect to FTP server. Exiting')
        sys.exit(1)
    try:
        ftpcon.login(ftpuser, ftppass)
    except:
        print('Connected to FTP but cannot login. Exiting.')
        sys.exit(1)
    print('FTP server ok')


if __name__ == '__main__':
    main()
#    inputstore = {'params': {},
#                  }
#    inputs = {name: {'src': 'hda', 'id': None} for name in
#              get_flatfile_names_inputstore()}
#    inputs.update({name: {'src': 'hdca', 'id': None} for name in
#                   get_collection_names_inputstore()})
#    inputstore['datasets'] = inputs
#    parse_commandline(inputstore)
#    gi = util.get_galaxy_instance(inputstore)
#    if inputstore['run'] == 'show':
#        for num, wf in enumerate(get_workflows()):
#            modules = get_modules_for_workflow(wf['modules'])
#            tasks.check_modules(gi, modules)
#            print('{}  -  {}'.format(num, wf['name']))
#    else:
#        output_dset_names = get_output_dsets()
#        download_dsets = {name: inputs[name] for name in output_dset_names}
#        for name, dl_dset in download_dsets.items():
#            outname = '{}'.format(output_dset_names[name])
#            dl_dset['download_state'] = False
#            dl_dset['download_dest'] = os.path.join(inputstore['outshare'],
#                                                    inputstore['outpath'],
#                                                    outname)
#        inputstore['output_dsets'] = download_dsets
#        inputstore['wf'] = [get_workflows()[num]
#                            for num in inputstore['wf_num']]
#        run_workflow(inputstore)