import requests
import os
import sys
import zipfile
import io

DATA_DIR = 'data'

FILE_LOCATIONS = {
   "cejst": {
       "longname": "Climate and Economic Justice Screening Tool Data",
       "url": "https://static-data-screeningtool.geoplatform.gov/data-versions/1.0/data/score/downloadable/1.0-communities.csv"
   },
   "ppc": {
       "longname": "Persistent Poverty Counties",
       "url": "https://www.ers.usda.gov/webdocs/DataFiles/48652/2015CountyTypologyCodes.csv"
   },
   "brownfields": {
       "longname": "Brownfields",
       "url": "https://ordsext.epa.gov/FLA/www3/acres_frs.kmz"
   },
   "coal_tracts": {
       "longname": "Census Tracts Affected by Coal Closures",
       "url": "https://edx.netl.doe.gov/resource/28a8eb09-619e-49e5-8ae3-6ddd3969e845/download?authorized=True",
       "ext": "zip",
       "file": "IRA_Coal_Closure_Energy_Comm_2023v2/Coal_Closure_Energy_Communities_2023v2.csv"
   },
   "employment_msas": {
       "longname": "Areas with energy economies or high unemployment.",
       "url": "https://edx.netl.doe.gov/resource/b736a14f-12a7-4b9f-8f6d-236aa3a84867/download?authorized=True",
       "ext": "zip",
       "file": "MSA_NMSA_FEE_EC_Status_2023v2/MSA_NMSA_FFE_EC_2023v2.csv"
   }
}

def download_files(files = FILE_LOCATIONS, path = DATA_DIR):
    for source, props in files.items():
        ext = os.path.splitext(props['url'])[1]
        if (len(ext) == 0):
            try:
                ext = '.' + props['ext']
            except:
                print("Could not obtain file extension.")
                sys.exit()
        print(f"Downloading {props['longname']} as {source}{ext}. 🚀")
        r = requests.get(props['url'], stream=True)
        if ext == ".zip":
            with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                for info in zf.infolist():
                    if info.filename == props['file']:
                        info.filename = f"{source}{os.path.splitext(props['file'])[1]}"
                        zf.extract(info, path)
        else:
            with open(os.path.join(path, f'{source}{ext}'), 'wb') as f:
                f.write(r.content)
        print(f"Done. ✔️")

if __name__ == "__main__":
    download_files()