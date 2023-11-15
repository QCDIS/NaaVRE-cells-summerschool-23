import requests
from pathlib import Path
import os

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--dataset_files', action='store', type=str, required=True, dest='dataset_files')

arg_parser.add_argument('--param_api_key', action='store', type=str, required='True', dest='param_api_key')
arg_parser.add_argument('--param_radar', action='store', type=str, required='True', dest='param_radar')

args = arg_parser.parse_args()
print(args)

id = args.id

import json
dataset_files = json.loads(args.dataset_files)

param_api_key = args.param_api_key
param_radar = args.param_radar

conf_knmi_dir = f'{os.environ.get("HOME")}/data/KNMI'
conf_radars = {'herwijnen' :  ['radar_volume_full_herwijnen',1.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files','NL/HRW'],'denhelder' :  ['radar_volume_full_denhelder',2.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files','NL/DHL']}

conf_knmi_dir = f'{os.environ.get("HOME")}/data/KNMI'
conf_radars = {'herwijnen' :  ['radar_volume_full_herwijnen',1.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files','NL/HRW'],'denhelder' :  ['radar_volume_full_denhelder',2.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files','NL/DHL']}
_, _, api_url, radar_code = conf_radars.get(param_radar)
knmi_pvol_paths = []
n_files = len(dataset_files)
print(f"Starting download of {n_files} files.")
idx = 1
for dataset_file in dataset_files:
    print(f"Downloading file {idx}/{n_files}")
    filename = dataset_file[0]
    endpoint = f"{api_url}/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": param_api_key})
    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)
    fname_parts = filename.split('_')
    fname_date_part = fname_parts[-1].split('.')[0]
    year = fname_date_part[0:4]
    month = fname_date_part[4:6]
    day = fname_date_part[6:8]
    p = Path(f"{conf_knmi_dir}/{year}/{month}/{day}/{filename}")
    knmi_pvol_paths.append('{}'.format(str(p)))
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(dataset_file_response.content)
    idx += 1
print(knmi_pvol_paths)

import json
filename = "/tmp/knmi_pvol_paths_" + id + ".json"
file_knmi_pvol_paths = open(filename, "w")
file_knmi_pvol_paths.write(json.dumps(knmi_pvol_paths))
file_knmi_pvol_paths.close()
