#Python version - 3.8
#This script requires requests module installed in python.
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen,Request

url = "	https://sdpondemand.manageengine.com/api/v3/requests/758744"
headers ={"Accept": "application/vnd.manageengine.sdp.v3+json", 
          "Authorization" : "Zoho-oauthtoken 1000.7c1d64c5e8e38f24d88dcf0ab6a38bd6.012c91914195bbf05730838ecc130cbb", 
          "Content-Type" : "application/x-www-form-urlencoded"}
httprequest = Request(url, headers=headers)
try:
    with urlopen(httprequest) as response:
        print(response.read().decode())
except HTTPError as e:
    print(e.read().decode())