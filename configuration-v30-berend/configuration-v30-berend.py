import os

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




param_radar = "" # denhelder,herwijnen
param_api_key = "" #
param_start_date = "" # %Y%m%dT%H:%M+TZ; 2019-12-31T23:00+00:00
param_end_date = "" # %Y%m%dT%H:%M+TZ; 2020-01-01T01:00+00:00
conf_herwijnen = ['radar_volume_full_herwijnen',1.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files','NL/HRW'] 
conf_denhelder = ['radar_volume_full_denhelder',2.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files','NL/DHL']
conf_radars = {'herwijnen' : conf_herwijnen,'denhelder' : conf_denhelder}


conf_storage_dir = f'{os.environ.get("HOME")}/data' 
conf_knmi_dir = f'{os.environ.get("HOME")}/data/KNMI'
conf_odim_dir = f'{os.environ.get("HOME")}/data/ODIM'
conf_vp_dir = f'{os.environ.get("HOME")}/data/VP'
conf_conf_dir = f'{os.environ.get("HOME")}/data/conf'

conf_clean_knmi_input = True 

check_dirs = [conf_storage_dir,
              conf_odim_dir,
              conf_vp_dir,
              conf_knmi_dir,
              conf_conf_dir]

for _dir in check_dirs:
    if not os.path.exists(_dir): # If this directory does not exist...
        os.makedirs(_dir) # Create the directory

conf_interval = 5 # minutes, HH:00,HH:05,HH:10,HH:15,HH:20,HH:25,HH:30,HH:35,HH:40,HH:45,HH:50,HH:55 


param_worker_chunk_size = 12 * 24

conf_radar_db = f'{conf_conf_dir}/OPERA_RADARS_DB.json'

config_complete = "Yes" # Cant sent bool

import json
filename = "/tmp/config_complete_" + id + ".json"
file_config_complete = open(filename, "w")
file_config_complete.write(json.dumps(config_complete))
file_config_complete.close()
