import requests
import requests.packages.urllib3
from requests.auth import HTTPBasicAuth
import json
import urllib3
import getpass

api_url = 'https://VCSA-IP/rest'
api_user = 'ac@vsphere.local'
api_pass = getpass.getpass(prompt='Enter your password:')
find_vm = "VMNAME"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth_vcenter(username,password):
    print(f'Authenticating to vCenter, user: {api_user}')
    resp = requests.post(f'{api_url}/com/vmware/cis/session',auth=(api_user,api_pass),verify=False)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp.json()['value']

def get_api_data(req_url):
    sid = auth_vcenter(api_user,api_pass)
    print('Requesting Page: {}'.format(req_url))
    resp = requests.get(req_url,verify=False,headers={'vmware-api-session-id':sid})
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp

def getvm():
    resp = get_api_data(f'{api_url}/vcenter/vm/vm-15628/guest/identity') # URL, lookup using https://VCSA/apiexplorer/
    j = resp.json()
    data = json.dumps(j, indent=4)
    print(data)
    with open("vms.json", "w") as write_file:
        json.dump(j, write_file)
    
    #datastore = 'VMs: {j} [VM]'
    #print(datastore['VMs']['VM'])

def main():
    getvm()

main()

