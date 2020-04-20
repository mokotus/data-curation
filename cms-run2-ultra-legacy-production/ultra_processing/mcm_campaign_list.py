import os, sys, time
import string

# os.system('cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess')

from mcm.rest import McM

def query_for_key_values(campaign_name):
  # mcm = McM(dev=False, debug=True)
  mcm = McM(dev=False)
  page = 0
  res = mcm.get('requests',query='member_of_campaign=' + campaign_name, page=page)
  print("Total datasets in page: " + str(len(res)))

  all_datasets = []

  while len(res) !=0:
    for r in res:
      dataset = dict()

      # for k in r.keys():
      #   print k, " - ", r[k]

      dataset['output_dataset'] = r['output_dataset']
      dataset['prep_id'] = str(r['prepid'])
      dataset['config_id'] = str(r['config_id'][0])
      dataset['generator_parameters'] = r['generator_parameters']

      all_datasets.append(dataset)

    # Go to next page, and repeat procedure of extraction
    page += 1
    res = mcm.get('requests', query=campaign_name, page=page)
  return all_datasets

def query_for_config_files(configs):
  mcm = McM(dev=False)
  
  r_configs = []
  for config_id in configs:
    r_configs.append(mcm.get_raw(config_id, web=True))

  return r_configs

 
def query_for_cms_driver_scripts(prep_ids):
  # mcm = McM(dev=False, debug=True)
  mcm = McM(dev=False)

  r_scripts = []
  for prep_id in prep_ids:
    r_scripts.append(mcm.get_cms_driver_script(prep_id))
  
  return r_scripts

