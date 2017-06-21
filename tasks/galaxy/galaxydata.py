workflows = [
    # FIXME runtime params cannot be checked before running,
    # because not-connected datasets
    # are also runtime vars and cannot be distinguished. Therefore, be very
    # careful and do a dry run so you will see WARNINGs when not filling in
    # params (and meaningless warnings for eg martmap in varDB search)
    {
        'name': 'New test IPG, ENSEMBL', 'modules': [
            ('base_search', '0.1', 'proteingenes'),
        ],
        'searchtype': 'standard',
        'dbtype': 'ensembl',
        'quanttype': 'isobaric',
        'required_params': ['multiplextype', 'denominators',
                            'instrument', 'modifications',
                            'setpatterns', 'setnames',
                            'fr_matcher', 'strips', 'strippatterns',
                            'perco_ids', 'ppoolsize'],
        'required_dsets': [],
        'not_used_tool_inputs': ['mzidnormalize'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'decoy db', 'modifications', 'biomart map',
                       'knownpep predpi tabular'],
        'other_inputs': ['sourcehis', 'strips'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table', 'protein table', 'gene table',
                    'symbol table'],
    },
    {
        'name': 'New test IPG, uniprot', 'modules': [
            ('@collect_source_spectra', 0.0),
            ('base_search', '0.1', 'proteingenes'),
        ],
        'searchtype': 'standard',
        'dbtype': 'uniprot',
        'quanttype': 'isobaric',
        'required_params': ['multiplextype', 'denominators',
                            'instrument', 'modifications',
                            'setpatterns', 'setnames',
                            'fr_matcher', 'strips', 'strippatterns',
                            'perco_ids', 'ppoolsize'],
        'required_dsets': ['sourcehis'],
        'not_used_tool_inputs': ['mzidnormalize'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'decoy db', 'modifications', 'biomart map',
                       'knownpep predpi tabular'],
        'other_inputs': ['sourcehis', 'strips'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table', 'protein table', 'gene table',
                    'symbol table'],
    },
    {
        'name': 'New test IPG, varDB isobaric', 'modules': [
            ('@collect_source_spectra', 0.0),
            ('vardb_base', '0.1', 'peptides noncentric'),
        ],
        'searchtype': 'vardb',
        'dbtype': 'vardb',
        'quanttype': 'isobaric',
        'required_params': ['multiplextype', 'denominators',
                            'instrument', 'modifications',
                            'setpatterns', 'setnames',
                            'fr_matcher', 'strips', 'strippatterns',
                            'perco_ids', 'ppoolsize'],
        'required_dsets': ['sourcehis'],
        'not_used_tool_inputs': ['mzidnormalize'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'decoy db', 'modifications', 'biomart map',
                       'knownpep predpi tabular'],
        'other_inputs': ['sourcehis', 'strips'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table'],
    },
    {
        'name': 'New test IPG, varDB labelfree', 'modules': [
            ('@collect_source_spectra', 0.0),
            ('vardb_base', '0.1', 'peptides noncentric'),
        ],
        'searchtype': 'vardb',
        'dbtype': 'vardb',
        'quanttype': 'labelfree',
        'required_params': ['instrument', 'modifications',
                            'setpatterns', 'setnames',
                            'fr_matcher', 'strips', 'strippatterns',
                            'perco_ids', 'ppoolsize'],
        'required_dsets': ['sourcehis'],
        'not_used_tool_inputs': ['mzidnormalize'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'decoy db', 'modifications', 'biomart map',
                       'knownpep predpi tabular'],
        'other_inputs': ['sourcehis', 'strips'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table'],
    },
    # FIXME new 6RF JSON is fractionated_db_peptide_v0.1.json
    {
        'name': 'IPG, tmt10, ENSEMBL, QE', 'modules': [
            '@collect_source_spectra', '@mslookup_spectra',
            'quant iso', 'msgf tmt qe', '@metafiles2pin', 'percolator',
            '@mergepercolator', 'percolator recalc', '@pout2mzid',
            'percolator postprocess',
            'psm preproc isobaric ensembl', 'psm proteingroup',
            'psm add deltapi', 'psm post isobaric',
            'peptide protein isobaric', 'gene isobaric',
            'protein isobaric', 'symbol isobaric'],
        'searchtype': 'standard',
        # FIXME only have required inputs, do param parsing before, so have setnames
        # as required but let start_wf decide what they are from filesassets/setnames
        'required_params': ['multiplextype', 'denominators',
                            'setpatterns', 'setnames',
                            'intercepts', 'fr_widths', 'strippatterns',
                            'perco_ids', 'ppoolsize'],
        'required_dsets': ['sourcehis'],
        'not_used_tool_inputs': ['mzidnormalize'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'modifications', 'biomart map',
                       'pipeptides known db'],
        # param inputs probably deprecate
        'param_inputs': ['setnames', 'setpatterns', 'filesassets', 'perco_ids',
                         'ppoolsize', 'fastadelim', 'genefield',
                         'multiplextype', 'denominators', 'pipatterns'],
        'other_inputs': ['sourcehis', 'strips'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table', 'protein table', 'gene table',
                    'symbol table'],
    },
    {
        'name': 'IPG, labelfree, ENSEMBL, QE', 'modules': [
            '@collect_source_spectra', '@mslookup_spectra',
            'quant labelfree', 'msgf labelfree qe', '@metafiles2pin', 'percolator',
            '@mergepercolator', 'percolator recalc', '@pout2mzid',
            'percolator postprocess',
            'psm preproc labelfree ensembl', 'psm proteingroup',
            # This fails because we have no deltapi for labelfree I think
            'psm add deltapi', 'psm post labelfree',
            'peptide protein labelfree', 'gene labelfree',
            'protein labelfree', 'symbol labelfree'],
        'searchtype': 'standard',
        'required_params': ['setpatterns', 'setnames',
                            'intercepts', 'fr_widths', 'strippatterns',
                            'perco_ids', 'ppoolsize',],
        'required_dsets': ['sourcehis'],
        'not_used_tool_inputs': [],
        'his_inputs': [],
        'lib_inputs': ['target db', 'modifications', 'biomart map',
                       'pipeptides known db'],
        'param_inputs': ['setnames', 'setpatterns', 'filesassets', 'perco_ids',
                         'ppoolsize', 'fastadelim', 'genefield',
                         ],
        'other_inputs': ['sourcehis'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table', 'protein table', 'gene table',
                    'symbol table'],
    },
    {
        'name': 'varDB, tmt10, QE', 'modules': [
            '@collect_source_spectra',
            'msgf tmt qe', '@metafiles2pin', 'percolator filternovel',
            '@mergepercolator', 'percolator recalc vardb', '@pout2mzid',
            'percolator postprocess',
            'psm preproc isobaric vardb',
            'psm add deltapi',
            'psm post isobaric vardb', 'peptide vardb isobaric'],
        'searchtype': 'vardb',
        'required_params': ['setpatterns', 'setnames',
                            'perco_ids', 'ppoolsize',
                            'intercepts', 'fr_widths', 'strippatterns',
                            'multiplextype', 'denominators'],
        'required_dsets': ['PSM table target normalsearch', 'quant lookup',
                           'sourcehis'],
        'not_used_tool_inputs': ['mapfn', 'dbase'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'modifications', 'knownpep db',
                       'knownpep allpep lookup', 'knownpep tryp lookup',
                       'pipeptides known db'],
        'param_inputs': ['setnames', 'setpatterns', 'filesassets', 'perco_ids',
                         'ppoolsize', 'multiplextype', 'denominators'],
        'other_inputs': ['sourcehis'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table'],
    },
    {
        'name': 'varDB, labelfree, QE', 'modules': [
            '@collect_source_spectra',
            'msgf labelfree qe', '@metafiles2pin', 'percolator filternovel',
            '@mergepercolator', 'percolator recalc vardb', '@pout2mzid',
            'percolator postprocess',
            'psm preproc labelfree vardb',
            'psm add deltapi',
            'psm post labelfree', 'peptide vardb labelfree'],
        'searchtype': 'vardb',
        'required_params': ['setpatterns', 'setnames',
                            'intercepts', 'fr_widths', 'strippatterns',
                            'perco_ids', 'ppoolsize',],
        'required_dsets': ['PSM table target normalsearch', 'quant lookup',
                           'sourcehis'],
        'not_used_tool_inputs': ['mapfn', 'dbase'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'modifications', 'knownpep db',
                       'knownpep allpep lookup', 'knownpep tryp lookup',
                       'pipeptides known db'],
        'param_inputs': ['setnames', 'setpatterns', 'filesassets', 'perco_ids',
                         'ppoolsize'],
        'other_inputs': ['sourcehis'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table'],
    },
    {
        'name': '6RF, tmt10, QE', 'modules': [
            '@collect_source_spectra',
            'peptide MS1 shift',
            '@create_6rf_split_dbs', '@create_spectra_db_pairedlist',
            'msgf prefrac tmt qe', '@metafiles2pin', 'percolator filternovel',
            '@mergepercolator', 'percolator recalc', '@pout2mzid',
            'percolator postprocess',
            'psm preproc isobaric vardb',
            'psm add deltapi',
            'psm post isobaric vardb', 'peptide noncentric isobaric'],
        'searchtype': '6rf',
        'required_params': ['setpatterns', 'setnames',
                            'perco_ids', 'ppoolsize',
                            'intercepts', 'fr_widths',
                            'interceptlist', 'fr_widthlist',
                            'fr_amounts', 'pi_tolerances', 'reverses',
                            'strips', 'strippatterns', 'strippatternlist',
                            'code',  # for pattern matching of fractions
                            'multiplextype', 'denominators'],
        'required_dsets': ['PSM table target normalsearch', 'quant lookup',
                           'sourcehis', 'pipeptides db', 'pipeptides known db'],
        'not_used_tool_inputs': ['mapfn', 'dbase'],
        'his_inputs': [],
        'lib_inputs': ['target db', 'modifications', 'knownpep db',
                       'knownpep allpep lookup', 'knownpep tryp lookup',],
        'param_inputs': ['setnames', 'setpatterns', 'filesassets', 'perco_ids',
                         'ppoolsize', 'multiplextype', 'denominators'],
        'other_inputs': ['sourcehis'],
        'outputs': ['pout2mzid target tar', 'PSM table target',
                    'peptide table'],
    },
#    {
#        'name': 'tmt10, ENSEMBL, QE', 'modules': [
#            'quant iso', 'msgf tmt qe', 'percolator',
#            'psm preproc isobaric ensembl', 'psm proteingroup',
#            'psm post isobaric', 'peptide protein isobaric', 'gene isobaric',
#            'protein isobaric', 'symbol isobaric'],
#        'searchtype': 'standard',
#        'not_outputs': [],
#    },
#    {
#        'name': 'tmt10, uni/swissprot, QE', 'modules': [
#            'quant iso', 'msgf tmt qe', 'percolator',
#            'psm preproc isobaric uniswiss', 'psm proteingroup',
#            'psm post isobaric', 'peptide protein isobaric', 'gene isobaric',
#            'protein isobaric'],
#        'searchtype': 'standard',
#        'not_outputs': ['symbol table'],
#    },
#    {
#        'name': 'labelfree ENSEMBL QE', 'modules': [
#            'quant labelfree', 'msgf labelfree qe', 'percolator',
#            'psm preproc lfree ensembl', 'psm proteingroup',
#            'psm post labelfree', 'peptide protein labelfree', 'gene labelfree',
#            'protein labelfree', 'symbol labelfree'],
#        'searchtype': 'standard',
#        'not_outputs': [],
#    },
#    {
#        'name': 'varDB, tmt10, ENSEMBL, QE', 'modules': [
#            'msgf tmt qe', 'percolator vardb', 'psm preproc isobaric vardb',
#            'psm post isobaric vardb', 'peptide noncentric isobaric'],
#        'searchtype': 'vardb',
#        'rerun_rename_labels': {
#            'quant lookup': False,
#            'PSM table target': 'PSM table target normalsearch'},
#        'not_outputs': ['protein table', 'gene table', 'symbol table'],
#    },
#    {
#        'name': 'varDB, labelfree, ENSEMBL, QE', 'modules': [
#            'msgf labelfree qe', 'percolator vardb', 'psm preproc lfree vardb',
#            'psm post labelfree', 'peptide noncentric labelfree'],
#        'searchtype': 'vardb',
#        'rerun_rename_labels': {
#            'quant lookup': False,
#            'PSM table target': 'PSM table target normalsearch'},
#        'not_outputs': ['protein table', 'gene table', 'symbol table'],
#    },
]


wf_modules = {
    'quant iso': 'e6b13c2a-7969-4ccc-bd41-c006bbb84be8',
    'quant labelfree': '6a91e9ab-731b-4617-b356-ae36790be4a0',
    'msgf tmt qe': '17701149-a72a-4452-ad7d-128ea5f276b8',
    'msgf labelfree qe': 'c707d755-a64b-4579-bc72-2fefca741f13',
    'msgf prefrac tmt qe': '3cb2ff21-b299-406c-9861-a42c3cba544a',
    'percolator': '37f66993-4369-4c00-a163-6da78fd3630b',
    'percolator filternovel': '9bed6fae-655a-4baf-96b8-3c10900111b2',
    'percolator recalc': '76110759-bd77-47c3-9a36-1ee48ce97149',
    'percolator postprocess': '42939250-13d7-4771-b351-1570f44a58e1',
    'percolator recalc vardb': '95c66364-3bfa-4856-867c-48a8350f9326',
    'psm preproc isobaric ensembl': 'b914447e-bb66-480c-a399-345f19ec2d7d',
    'psm preproc isobaric uniswiss': '52922669-6a28-42ba-9f98-dc885162c95c',
    'psm preproc labelfree ensembl': '119c5de5-6048-41a0-8b63-5e489b435bf3',
    'psm preproc isobaric vardb': 'beb9cacc-da94-4f55-b025-39a5da8ad4a3',
    'psm preproc labelfree vardb': '40759514-0afc-4e78-be17-92d64a821a7b',
    'psm proteingroup': 'ccb2444c-51a5-4f0a-b853-c42dd019568b',
    'psm post isobaric': '617935b6-d3cc-405c-9732-4054bee7f82b',
    'psm post isobaric vardb': 'eef6f0d2-1b42-4b2d-ade7-29ce0d9ec676',
    'psm post labelfree': 'dd894c0c-1017-4106-aab0-f0548ed09016',
    'psm add deltapi': 'afc13c23-943f-49af-b5c4-36b0ed544b92',
    'peptide protein isobaric': '19b7d181-938e-4209-959e-9f8679a0f9c3',
    'peptide vardb isobaric': '587d6013-d23f-4c21-b8ca-c9b594eba4d3',
    'peptide vardb labelfree': 'd02631ef-edcd-4d87-98b2-99ff7090dfd7',
    'peptide noncentric isobaric': 'e647857a-5a76-4e79-9e99-acaf3bd58e21',
    'peptide protein labelfree': '7bd63e79-e11a-4074-af42-69856a7dd64a',
    'peptide noncentric labelfree': 'f799c811-bab3-4dcd-9c8e-778cb0afd564',
    'peptide MS1 shift': '0698e186-8073-4495-95a4-5d15f64d629a',
    'protein isobaric': '0c85484a-33b8-4d29-ac03-2df2aab3112a',
    'gene isobaric': 'fa5769f8-45a4-471d-8925-7f99d21927a2',
    'symbol isobaric': '2b941732-b05c-4450-a449-ca1903a71287',
    'protein labelfree': '9ce49f2f-7760-4275-b3e1-9e315970a652',
    'gene labelfree': '70dffaf3-a5ce-4ba6-8063-b3255f6255ff',
    'symbol labelfree': 'f134271c-819b-4aff-b3b4-ea00b935b2ed',
}


download_data_names = {'pout2mzid target tar': 'mzidentml.tar.gz',
                       'PSM table target': 'psm_table.txt',
                       'peptide table': 'peptide_table.txt',
                       'protein table': 'protein_table.txt',
                       'gene table': 'gene_table.txt',
                       'symbol table': 'symbol_table.txt',
                       }


other_names = ['sourcehis']


collection_names = ['spectra',
                    'spectra target db',
                    'spectra decoy db',
                    'msgf target',
                    'msgf decoy',
                    'msgf tsv target',
                    'msgf tsv decoy',
                    'percometa target',
                    'percometa decoy',
                    'perco batch target',
                    'perco batch decoy',
                    'perco recalc target',
                    'perco recalc decoy',
                    'pout2mzid target',
                    'pout2mzid decoy',
                    'perco tsv target',
                    'perco tsv decoy',
                    'postprocessed PSMs target',
                    'postprocessed PSMs decoy',
                    'peptides bare target',
                    'peptides bare decoy',
                    'peptable MS1 deltapi',
                    ]

flatfile_names = ['target db',
                  'decoy db',
                  'knownpep predpi tabular',
                  'pipeptides db',
                  'pipeptides known db',
                  'knownpep db',
                  'knownpep tryp lookup',
                  'knownpep allpep lookup',
                  'biomart map',
                  'spectra lookup',
                  'modifications',
                  'quant lookup',
                  'PSM lookup target',
                  'PSM lookup decoy',
                  'preprocessed PSMs target',
                  'preprocessed PSMs decoy',
                  'annotated PSMs target',
                  'annotated PSMs decoy',
                  'pout2mzid target tar',  # output
                  'PSM table target',  # output
                  'PSM table decoy',
                  'proteingroup lookup target',
                  'proteingroup lookup decoy',
                  'peptide table',  # output
                  'protein table',  # output
                  'gene table',  # output
                  'symbol table',  # output
                  ]


# Montezuma
libraries = {'databases': 'a3437b7b0c19ebd1',
             'marts': '86ed203ff9a94938',
             'pipeptides': '128140af13bad45b',
             'knownpeptides': 'e9b47af80022b6ee',
             }


strips = {'37-49': {'fr_width': 0.0174,
                    'pi_tolerance': 0.08,
                    'intercept': 3.5959,
                    'fr_amount': 72,
                    'reverse': False},
          '3-10': {'fr_width': 0.0676,
                   'pi_tolerance': 0.11,
                   'intercept': 3.5478,
                   'fr_amount': 72,
                   'reverse': False},
          '11-6': {'fr_width': -0.0762,
                   'pi_tolerance': 0.11,
                   'intercept': 10.3936,
                   'fr_amount': 60,
                   'reverse': True},
          '6-9': {'fr_width': 0.0336,
                  'pi_tolerance': 0.11,
                  'intercept': 6.1159,
                  'fr_amount': 72,
                  'reverse': False},
          }
strips = {name: {**strips[name], **{'name': name}} for name in strips}
