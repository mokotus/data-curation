# Ultra-Legacy Production Scripts
Repository for extracting provenance information from specified campaign.

## Setup
Login to lxplus, choose a folder and clone the branch: `git clone -b run2-ultra-legacy https://github.com/mokotus/data-curation.git`

## Usage steps (done every time after login to lxplus)
1. Go to this folder(cms-run2-ultra-legacy-production) with `cd`
2. Enable cms environment: `cmsenv`
3. Generate CERN SSO cookie from credentials. Type `cern-get-sso-cookie --help` for help or see [McM-folder readme](ultra_processing/mcm/README.md#cern-sso-cookie) for examples
4. Enable voms proxy by typing: `voms-proxy-init --voms cms --rfc --valid 190:00`
5. Find an empty folder or create one for outputs, for example: `mkdir outputs`
6. run `run2-ultra-main.py` with proper parameters(see `python2 run2-ultra-main.py --help` for help), example: `python2 run2-ultra-main.py -c RunIIFall15MiniAODv2 ./outputs`

### Additional information and links
* Tested with `Python 2.7.5` on `lxplus.cern.ch`
* For most actions you will NEED to have a valid CERN SSO cookie
* Public APIs do not require a cookie. Index of public API: https://cms-pdmv.cern.ch/mcm/public/restapi/
* Link to McM: https://cms-pdmv.cern.ch/mcm/
* McM Rest API: https://cms-pdmv.cern.ch/mcm/restapi

### Diagram representing algorithm worklow
* Found diagram hard to read? Feel free to edit and update, this will save someones time reading actual code.
* You can edit diagram on https://www.draw.io/, by importing final-ultra.xml
  file under diagram directory.
![alt text](./diagram/legacy.jpg)

### Things so far implemented
* Extracting cmsdriver scripts, configuration files, cross section information
  from MCM.
* Locating datasets on disk via global locator and dumping provenance
  information.

### Todo
* Making sure the provenance information is in correct format (MiniAOD)
* Add LHCheader related code to dataset_locator.dump_provenance_lhc
* Nice to have features? (progress, error handling...)