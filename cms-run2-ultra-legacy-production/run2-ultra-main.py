#!/usr/bin/env python

""" A helper script which finds all related datasets for one specified campaign

Extracts all important provenance metadata, which later gets stored on DPOA
storage like cmsdriver scripts, configuration files, cross section and lastly
(but hopefully not the least one) edmProvDump.py and edmLHCHeader.py output.

"""

import click
import json
from ultra_processing.mcm_campaign_list import *
from ultra_processing.dataset_locator import *

@click.command()
@click.option('--campaign', '-c', required=True,
              help='Specify campaign name for metadata extraction')
@click.argument('output_dir_path', type=click.Path(exists=True))
def main(campaign, output_dir_path):
    """Downloads from McM and stores all metadata information on DPOA
    Steps it takes sequentially:
    1) Downloads for each parent dataset from McM service metadata like: 
    cmsdriver scripts, configuration files, cross section.
    2) Stores all this metada information on DPOA storage.
    3) If root files are available on DAS service, finds location using global
    locator and runs scripts: edmDumpProv.py and if exists LHC also 
    edmLHCheader.py
    """

    # 1) === DOWNLOAD DATASETS ===

    # - 1.1) Get metadata of datasets  
    datasets = query_for_key_values(campaign)

    # - 1.2) Get dataset configs
    print "Getting configs..."
    config_ids = [ds['config_id'] for ds in datasets]
    configs = query_for_config_files(config_ids)

    # - 1.3) Get dataset cms driver scripts
    print "Getting cms driver scripts..."
    prep_ids = [ds['prep_id'] for ds in datasets]
    scripts = query_for_cms_driver_scripts(prep_ids)

    # 2) === STORE DATA ===
    print "Storing data..."

    # - 2.1) Store configs
    os.mkdir(os.path.join(output_dir_path, "configs"))
    for i, config_id in enumerate(config_ids):
        f = open(os.path.join(output_dir_path, "configs", config_id + ""), 'w')
        f.write(configs[i])
        f.close()

    # - 2.2) Store cms driver scripts
    os.mkdir(os.path.join(output_dir_path, "scripts"))
    for i, prep_id in enumerate(prep_ids):
        f = open(os.path.join(output_dir_path, "scripts", prep_id + ".sh"), 'w')
        f.write(scripts[i])
        f.close()

    # 3) === DUMP PROV ===
    print "Dumping provenance..."
    dump_provenance_lhc(datasets[0]["output_dataset"], output_dir_path) #Testing with one prov file

    # for ds in datasets:
    #     dump_provenance_lhc(ds["output_dataset"], output_dir_path)

if __name__ == '__main__':
    main()
