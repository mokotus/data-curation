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
@click.option('--skip', '-s', required=False, type=click.IntRange(1, 3), multiple=True, help='Skips a step by its number (1, 2 or 3)')
@click.argument('output_dir_path', type=click.Path(exists=True))
def main(campaign, skip, output_dir_path):
    """Downloads from McM and stores all metadata information on DPOA.
    Steps it takes sequentially:\n
    1) Downloads configuration files to output_dir_path/configs/\n
    2) Downloads cmsdriver scripts to output_dir_path/scripts/\n
    3) If root files are available on DAS service, finds location using global
    locator and runs scripts: edmDumpProv.py and if LHC exists, 
    edmLHCheader.py. Saves providence dump to output_dir_path/prov/\n
    If you wish to skip any of these steps, please see the '--skip' option below.
    """

    # Get metadata of datasets in campaign 
    datasets = query_for_key_values(campaign)

    # === STEP 1) CONFIG FILES ===
    if 1 in skip:
        print "(Skipping configs step 1)"
    else:
        print "Saving configs..."
        config_ids = [ds['config_id'] for ds in datasets]
        configs = query_for_config_files(config_ids)

        # - Save configs to output directory
        os.mkdir(os.path.join(output_dir_path, "configs"))
        for i, config_id in enumerate(config_ids):
            f = open(os.path.join(output_dir_path, "configs", config_id + ""), 'w')
            f.write(configs[i])
            f.close()

    # === STEP 2) CMS DRIVER SCRIPTS ===
    if 2 in skip:
        print "(Skipping CMS driver scripts step 2)"
    else:
        print "Saving CMS driver scripts..."
        prep_ids = [ds['prep_id'] for ds in datasets]
        scripts = query_for_cms_driver_scripts(prep_ids)

        # - Save cms driver scripts to output directory
        os.mkdir(os.path.join(output_dir_path, "scripts"))
        for i, prep_id in enumerate(prep_ids):
            f = open(os.path.join(output_dir_path, "scripts", prep_id + ".sh"), 'w')
            f.write(scripts[i])
            f.close()

    # 3) === STEP 3) PROV DUMP ===
    if 3 in skip:
        print "(Skipping prov dump step 3)"
    else:
        print "Dumping provenance info..."
        dump_provenance_lhc(datasets[0]["output_dataset"], output_dir_path) #Testing with one prov file
        # Enable this for all prov files (takes a long time):
        # for ds in datasets:
        #     dump_provenance_lhc(ds["output_dataset"], output_dir_path)

if __name__ == '__main__':
    main()
