import requests

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--config_complete', action='store', type=str, required='True', dest='config_complete')

arg_parser.add_argument('--param_api_key', action='store', type=str, required='True', dest='param_api_key')
arg_parser.add_argument('--param_end_date', action='store', type=str, required='True', dest='param_end_date')
arg_parser.add_argument('--param_radar', action='store', type=str, required='True', dest='param_radar')
arg_parser.add_argument('--param_start_date', action='store', type=str, required='True', dest='param_start_date')
arg_parser.add_argument('--param_worker_chunk_size', action='store', type=int, required='True', dest='param_worker_chunk_size')

args = arg_parser.parse_args()
print(args)

id = args.id

config_complete = args.config_complete

param_api_key = args.param_api_key
param_end_date = args.param_end_date
param_radar = args.param_radar
param_start_date = args.param_start_date
param_worker_chunk_size = args.param_worker_chunk_size

conf_interval = 5 # minutes, HH:00,HH:05,HH:10,HH:15,HH:20,HH:25,HH:30,HH:35,HH:40,HH:45,HH:50,HH:55
conf_radars = {'herwijnen' :  ['radar_volume_full_herwijnen',1.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files','NL/HRW'],'denhelder' :  ['radar_volume_full_denhelder',2.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files','NL/DHL']}

conf_interval = 5 # minutes, HH:00,HH:05,HH:10,HH:15,HH:20,HH:25,HH:30,HH:35,HH:40,HH:45,HH:50,HH:55
conf_radars = {'herwijnen' :  ['radar_volume_full_herwijnen',1.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_full_herwijnen/versions/1.0/files','NL/HRW'],'denhelder' :  ['radar_volume_full_denhelder',2.0,'https://api.dataplatform.knmi.nl/open-data/v1/datasets/radar_volume_denhelder/versions/2.0/files','NL/DHL']}
if config_complete == "Yes":
    print("Workflow configuration succesfull")
    # Notes:
    # Timestamps in iso8601
    # 2020-01-01T00:00+00:00
    # Libraries
    import requests
    # configure 
    start_ts = param_start_date
    end_ts = param_end_date
    datasetName, datasetVersion, api_url, _ = conf_radars.get(param_radar)
    params = {'datasetName' : datasetName,
              'datasetVersion' : datasetVersion,
              'maxKeys' : 10,
              'sorting' : "asc",
              'orderBy' : "created",
              'begin' : start_ts,
              'end' : end_ts,
             }
    # Request a response from the KNMI severs
    # Try the next page tokens
    dataset_files = []
    while True:
        list_files_response = requests.get(url = api_url,
                                headers={"Authorization": param_api_key},
                                params = params)
        list_files = list_files_response.json()
        dset_files = list_files.get("files")
        dset_files = [list(dset_file.values()) for dset_file in dset_files]
        dataset_files += dset_files
        nextPageToken = list_files.get("nextPageToken")
        if not nextPageToken:
            break
        else:
            params.update({'nextPageToken' : nextPageToken})
    # Rewrote this section to pull information from the dict (contained in the main list)
    # we cant pass anything but primitives around between Cells, so we rewrite it into a nested list of strings
    # note:
    # idx0 = filename, idx1 = size, idx2 = lastModified, idx3 = created
    # Subset to a different interval

    # KNMI outputs per 5 minutes, per 15 is less of a heavy hit on downloads and processing
    # Quick and dirty way to only keep the 15 minute measurements. 
    # Check API if we can filter for this on their end. If not fine
    filtered_list = []
    interval_list = list(range(0,60,conf_interval))
    for dataset_file in dataset_files:
        minute = int(dataset_file[0].split('_')[-1].split('.')[0][-2:])
        if minute in interval_list:
            filtered_list.append(dataset_file)

    dataset_files = filtered_list
    print(f"Found {len(dataset_files)} files")
    print(dataset_files)
    
    # Now rewrite into a nested list to control parallelization
    while dataset_files:
        _.append(dataset_files[:param_worker_chunk_size])
        dataset_files = dataset_files[param_worker_chunk_size:]
    dataset_files = _
        
else:
    pass

import json
filename = "/tmp/dataset_files_" + id + ".json"
file_dataset_files = open(filename, "w")
file_dataset_files.write(json.dumps(dataset_files))
file_dataset_files.close()
