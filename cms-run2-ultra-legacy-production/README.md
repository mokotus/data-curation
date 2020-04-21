# Ultra-Legacy Production Scripts
Repository for extracting provenance information from specified campaign.

## Setup
1. Login to lxplus and [prepare a CMSSW release area](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookSetComputerNode#CreateWork)
2. Under your CMSSW release src-folder, clone the branch: `git clone -b run2-ultra-legacy https://github.com/mokotus/data-curation.git`

## Usage steps (done every time after login to lxplus)
1. Enter this folder(cms-run2-ultra-legacy-production)
2. Enable CMS environment: `cmsenv`
3. Enable voms proxy by typing: `voms-proxy-init --voms cms --rfc --valid 190:00`
4. Find an empty folder or create one for outputs, for example: `mkdir outputs`
5. run `run2-ultra-main.py` with campaign name and output folder as parameters(see `python2 run2-ultra-main.py --help` for full info)
    * Example: `python2 run2-ultra-main.py -c RunIIFall15MiniAODv2 ./outputs`

### Additional information and links
* Tested with `Python 2.7.5` on `lxplus.cern.ch`
* Note that certain steps can be skipped using the `--skip [step_number]` flag. If you wish to alter the process more, start from the [main run file](run2-ultra-main.py).
* For most actions you will NEED to have a valid CERN SSO cookie. The script will try to create the cookie automatically but if it doesn't succeed, you may want to create the cookie manually. There are a few ways to do this (type `cern-get-sso-cookie --help` to see the documentation):
    * Run [getCookie.sh](ultra_processing/mcm/getCookie.sh)
    * Or run: `cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb`
    * If all else fails, create cert and key files by following the instructions [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert), and then run: `mkdir -p ~/private && cern-get-sso-cookie --url https://cms-pdmv.cern.ch/mcm/ --cert ~/.globus/usercert.pem --key ~/.globus/userkey.pem --o ~/private/prod-cookie.txt`
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
* Add LHCheader related code to [dump_provenance_lhc](ultra_processing/dataset_locator.py#L39)
* Nice to have features? (progress, error handling...)