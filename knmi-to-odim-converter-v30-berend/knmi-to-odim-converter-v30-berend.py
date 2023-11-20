import subprocess
import pathlib
import h5py
import sys
from webdav3 import client as wc
import shutil
import os
import json

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--knmi_pvol_paths', action='store', type=str, required=True, dest='knmi_pvol_paths')

arg_parser.add_argument('--param_webdav_endpoint', action='store', type=str, required='True', dest='param_webdav_endpoint')
arg_parser.add_argument('--param_webdav_password', action='store', type=str, required='True', dest='param_webdav_password')
arg_parser.add_argument('--param_webdav_user', action='store', type=str, required='True', dest='param_webdav_user')

args = arg_parser.parse_args()
print(args)

id = args.id

import json
knmi_pvol_paths = json.loads(args.knmi_pvol_paths)

param_webdav_endpoint = args.param_webdav_endpoint
param_webdav_password = args.param_webdav_password
param_webdav_user = args.param_webdav_user

conf_local_radar_db = "/tmp/data/conf/OPERA_RADARS_DB.json"
conf_local_odim = "/tmp/data/odim"
conf_clean_knmi_input = True
conf_webdav_output_pvol =  f'/vl-vol2bird/{os.environ.get("JUPYTERHUB_USER")}'+'/pvol' # F'string formatting is breaking the analyser. Concating Str by addition works
conf_upload_results = True
conf_worker_chunk_size = 12 * 24

conf_local_radar_db = "/tmp/data/conf/OPERA_RADARS_DB.json"
conf_local_odim = "/tmp/data/odim"
conf_clean_knmi_input = True
conf_webdav_output_pvol =  f'/vl-vol2bird/{os.environ.get("JUPYTERHUB_USER")}'+'/pvol' # F'string formatting is breaking the analyser. Concating Str by addition works
conf_upload_results = True
conf_worker_chunk_size = 12 * 24

class FileTranslatorFileTypeError(LookupError):
        '''raise this when there's a filetype mismatch derived from h5 file'''  
def load_radar_db(radar_db_path):
    """Load and return the radar database

    Output dict sample (wmo code is used as key):
    {
        11038: {'number': '1209', 'country': 'Austria', 'countryid': 'LOWM41', 'oldcountryid': 'OS41', 'wmocode': '11038', 'odimcode': 'atrau', 'location': 'Wien/Schwechat', 'status': '1', 'latitude': '48.074', 'longitude': '16.536', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1978', 'heightantenna': '224', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.625', 'single_rrr': 'Y', 'composite_rrr': 'Y', 'wrwp': 'Y'},
        11052: {'number': '1210', 'country': 'Austria', 'countryid': 'LOWM43', 'oldcountryid': 'OS43', 'wmocode': '11052', 'odimcode': 'atfel', 'location': 'Salzburg/Feldkirchen', 'status': '1', 'latitude': '48.065', 'longitude': '13.062', 'heightofstation': ' ', 'band': 'C', 'doppler': 'Y', 'polarization': 'D', 'maxrange': '224', 'startyear': '1992', 'heightantenna': '581', 'diametrantenna': ' ', 'beam': ' ', 'gain': ' ', 'frequency': '5.6', 'single_rrr': 'Y', 'composite_rrr': ' ', 'wrwp': ' '},
        ...
    }
    """
    with open(
        radar_db_path, mode="r"
    ) as f:
        radar_db_json = json.load(f)
    radar_db = {}
    # Reorder list to a usable dict with sub dicts which we can search with wmo codes
    for radar_dict in radar_db_json:
        try:
            wmo_code = int(radar_dict.get("wmocode"))
            radar_db.update({wmo_code: radar_dict})
        except Exception:  # Happens when there is for ex. no wmo code.
            pass
    return radar_db
def translate_wmo_odim(radar_db,wmo_code):
    """
    """
    if not isinstance(wmo_code,int):
        raise ValueError("Expecting a wmo_code [int]")
    else:
        pass
    odim_code = radar_db.get(wmo_code).get("odimcode").upper().strip() # Apparently, people sometimes forget to remove whitespace..
    return odim_code
def extract_wmo_code(in_path):
    with h5py.File(in_path, mode="r") as f:
        #DWD Specific
        #Main attributes
        what = f['what'].attrs
        #Source block
        source = what.get('source')
        source = source.decode("utf-8")
        # Determine if we are dealing with a WMO code or with an ODIM code set
        # Example from Germany where source block is set as WMO
        # what/source: "WMO:10103"
        # Example from The Netherlands where source block is set as a combination of ODIM and various codes
        # what/source: RAD:NL52,NOD:nlhrw,PLC:Herwijnen
        source_list = source.split(sep=",")
    wmo_code = [string for string in source_list if "WMO" in string]
    # Determine if we had exactly one WMO hit
    if len(wmo_code) == 1:
        wmo_code = wmo_code[0]
        wmo_code = wmo_code.replace("WMO:","")
    # No wmo code found, most likeley dealing with a dutch radar
    elif len(wmo_code) == 0:
        rad_str = [string for string in source_list if "RAD" in string]

        if len(rad_str) == 1:
                rad_str = rad_str[0]
        else:
            print("Something went wrong with determining the rad_str and it wasnt WMO either, exitting")
            sys.exit(1)
        # Split the rad_str
        rad_str_split = rad_str.split(":")
        # [0] = RAD, [1] = rad code
        rad_code = rad_str_split[1]

        rad_codes = {"NL52" : "6356",
                     "NL51" : "6234",
                     "NL50" : "6260"}

        wmo_code = rad_codes.get(rad_code)
    return int(wmo_code)
def translate_knmi_filename(in_path_h5):
    wmo_code = extract_wmo_code(in_path_h5)
    odim_code = translate_wmo_odim(radar_db,wmo_code)
    with h5py.File(in_path_h5, mode = "r") as f:
        what = f['what'].attrs
        #Date block
        date = what.get('date')
        date = date.decode("utf-8")
        #Time block
        time = what.get('time')
        #time = f['dataset1/what'].attrs['endtime']
        time = time.decode("utf-8")
        hh = time[:2]
        mm = time[2:4]
        ss = time[4:]
        time = time[:-2] # Do not include seconds
        #File type
        filetype = what.get('object')
        filetype = filetype.decode("utf-8")
        if filetype != "PVOL":
            raise FileTranslatorFileTypeError("File type was NOT pvol")
    name = [odim_code,filetype.lower(),date + "T" + time,str(wmo_code) + ".h5"]
    ibed_fname = "_".join(name)
    return ibed_fname
def knmi_to_odim(in_fpath,out_fpath):
    """
    Converter usage:
    Usage: KNMI_vol_h5_to_ODIM_h5 ODIM_file.h5 KNMI_input_file.h5

    Returns out_fpath and returncode
    """
    converter = 'KNMI_vol_h5_to_ODIM_h5'
    command = [converter,
               out_fpath,
               in_fpath]         
    proc = subprocess.run(command,stderr=subprocess.PIPE)
    output = proc.stderr.decode("utf-8")
    returncode = int(proc.returncode)
    return (out_fpath,returncode, output)


check_list = []
for knmi_pvol_path in knmi_pvol_paths:
    if isinstance(knmi_pvol_path,list):
        check_list += knmi_pvol_path
    else:
        check_list.append(knmi_pvol_path)
knmi_pvol_paths = check_list   
odim_pvol_paths = []
radar_db = load_radar_db(conf_local_radar_db)
for knmi_path in knmi_pvol_paths:
    out_path_pvol_odim = pathlib.Path(knmi_path.replace('knmi','odim'))
    if not out_path_pvol_odim.parent.exists():
        out_path_pvol_odim.parent.mkdir(parents=True,exist_ok=False)
    converter_results = knmi_to_odim(in_fpath = str(knmi_path),out_fpath = str(out_path_pvol_odim))
    if conf_clean_knmi_input:
        pathlib.Path(knmi_path).unlink()
        if not any(pathlib.Path(knmi_path).parent.iterdir()):
                   pathlib.Path(knmi_path).parent.rmdir()
    # Determine name for our convention
    ibed_pvol_name = translate_knmi_filename(in_path_h5=out_path_pvol_odim)
    out_path_pvol_odim_tce = pathlib.Path(out_path_pvol_odim).parent.joinpath(ibed_pvol_name)
    shutil.move(src=out_path_pvol_odim,dst=out_path_pvol_odim_tce)
    odim_pvol_paths.append(out_path_pvol_odim_tce)
   
print(odim_pvol_paths)
if conf_upload_results:
    print(f"Uploading results to {conf_webdav_output_pvol}")
    from webdav3 import client as wc
    options = {
     'webdav_hostname': param_webdav_endpoint,
     'webdav_login':    param_webdav_user,
     'webdav_password': param_webdav_password
    }
    client = wc.Client(options)
    for odim_pvol_path in odim_pvol_paths:
        odim_pvol_path = pathlib.Path(odim_pvol_path)
        local_odim_storage = pathlib.Path(conf_local_odim)
        relative_path = odim_pvol_path.relative_to(local_odim_storage)
        remote_pvol_path = f"{conf_webdav_output_pvol}/{str(relative_path)}"
        if not client.check(remote_pvol_path):
            print(f"Uploading {odim_pvol_path} to {remote_pvol_path}")
            # Check if we need to make the directories, we can do it lazy
            if not client.check(f"{conf_webdav_output_pvol}/{relative_path.parent}"):
                print(f"Remote directory {relative_path.parent} does not exist, creating")
                for i in reversed(range(0,len(relative_path.parts)-1)):
                    create_path = f"{conf_webdav_output_pvol}/{str(relative_path.parents[i])}"
                    print(f"Creating: {create_path}")
                    client.mkdir(create_path)
            client.upload_sync(remote_path = remote_pvol_path, local_path = str(odim_pvol_path))
        else:
            print(f"{remote_pvol_path} exists, skipping ")
    print("Finished uploading results")
_ = []
while odim_pvol_paths:
    _.append(odim_pvol_paths[:conf_worker_chunk_size])
    odim_pvol_paths = odim_pvol_paths[conf_worker_chunk_size:]
odim_pvol_paths = _

import json
filename = "/tmp/odim_pvol_paths_" + id + ".json"
file_odim_pvol_paths = open(filename, "w")
file_odim_pvol_paths.write(json.dumps(odim_pvol_paths))
file_odim_pvol_paths.close()
