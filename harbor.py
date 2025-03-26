import requests
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === KONFIGURATION ===
HARBOR_URL = "https://server"
USER = "benutzer"
PASSWORD = "passwort"
SOURCE_PROJECT = "ocp"
SOURCE_REPO = "openshift/release"  # Achtung: Kein URL-Encoding hier!
DEST_PROJECT = "openshift"
DEST_REPO = "backup"

# === AUTHENTIFIZIERUNG ===
SESSION = requests.Session()
SESSION.auth = (USER, PASSWORD)
# #SESSION.verify = "harbor-ca.crt"

# # Dummy-GET, um CSRF-Token zu bekommen
# csrf_url = f"{HARBOR_URL}/api/v2.0/projects"
# print("URL :"+csrf_url)
# csrf_response = SESSION.get(csrf_url, verify=False)
# print("RESPONSE :"+str(csrf_response))
# csrf_token = csrf_response.headers.get("X-Harbor-CSRF-Token", "")
# print("TOKEN :"+str(csrf_token))


# === ARTEFAKTE AUSLESEN ===
def get_artifacts():
    page = 1
    artifacts = []
    while True:
        url = f"{HARBOR_URL}/api/v2.0/projects/{SOURCE_PROJECT}/repositories/{urllib.parse.quote(urllib.parse.quote(SOURCE_REPO, safe=''), safe='')}/artifacts?page={page}&page_size=100"
        
        #debug
        print(url)

        response = SESSION.get(url, verify=False)
        
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Artefakte: {response.text}")
            break
        data = response.json()
        if not data:
            break  # Keine weiteren Artefakte
        artifacts.extend(data)
        page += 1
    return artifacts

# === ARTEFAKTE KOPIEREN ===
def copy_artifact(digest):
    encoded_digest = urllib.parse.quote(f"{digest}", safe='')
    print(encoded_digest)
    url = f"{HARBOR_URL}/api/v2.0/projects/{DEST_PROJECT}/repositories/{DEST_REPO}/artifacts?from={SOURCE_PROJECT}%2F{urllib.parse.quote(SOURCE_REPO, safe='')}%40{encoded_digest}"
    
    #Debug
    print(url)
    
#    headers = {"X-Harbor-CSRF-Token": csrf_token}

    #Debug
#    print(headers)  

#    response = SESSION.post(url, headers=headers, verify=False)
    response = requests.post(url, auth=(USER, PASSWORD), verify=False) 

    if response.status_code == 201:
        print(f"✅ Kopiert: {digest}")
    else:
        print(f"❌ Fehler beim Kopieren {digest}: {response.text}")

# === HAUPTLAUF ===
if __name__ == "__main__":
    artifacts = get_artifacts()
    print(f"Gefundene Artefakte: {len(artifacts)}")
    
    for artifact in artifacts:
        digest = artifact.get("digest")
        if digest:
            copy_artifact(digest)
    print("✅ Migration abgeschlossen!")
