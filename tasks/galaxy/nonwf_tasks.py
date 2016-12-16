from tasks.galaxy import tasks as runtasks


tasks = {'@pout2mzid': {'task': runtasks.run_pout2mzid_on_sets,
                        'inputs': ['perco recalc target',
                                   'perco recalc decoy',
                                   'msgf target',
                                   'msgf decoy'],
                        'params': ['perco_ids'],
                        'outputs': ['pout2mzid target',
                                    'pout2mzid decoy']
                        },
         '@mergepercolator': {'task': runtasks.merge_percobatches_to_sets,
                              'inputs': ['perco batch target',
                                         'perco batch decoy', ],
                              'params': ['perco_ids',
                                         'ppoolsize'],
                              'outputs': ['percolator pretarget',
                                         'percolator predecoy'],
                              },
         '@metafiles2pin': {'task': runtasks.run_metafiles2pin,
                            'inputs': ['msgf target',
                                       'msgf decoy'],
                            'params': ['perco_ids',
                                       'ppoolsize'],
                            'outputs': ['percometa target',
                                        'percometa decoy'],
                            },
         '@mslookup_spectra': {'task': runtasks.run_mslookup_spectra,
                               'inputs': ['spectra'],
                               'params': ['setpatterns',
                                          'setnames'],
                               'outputs': ['spectra lookup'],
                               },
         '@collect_source_spectra': {'task': runtasks.tmp_put_files_in_collection,
                                     'inputs': ['sourcehis'],
                                     'params': [],
                                     'outputs': ['spectra'],
                                     },
         }


# FIXME
# put in collection- sourcehis is now in datasets/inputstore, other_names, fix workflow parser/starter/dset init
