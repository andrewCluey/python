import requests
import requests.packages.urllib3
from requests.auth import HTTPBasicAuth
import json
import urllib3
import getpass

api_url = 'https://VCSA-IP/rest'
api_user = 'ac@.vspherelocal'
api_pass = getpass.getpass(prompt='Enter your password:')
hostname = "HOST-IP"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth_vcenter(username,password):
    print(f'Authenticating to vCenter, user: {api_user}')
    resp = requests.post(f'{api_url}/com/vmware/cis/session',auth=(api_user,api_pass),verify=False)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp.json()['value']

# connect to vCenter, authenticate and 'GET' whatever is defined in URL argument (URL is set from other functions)
def get_api_data(req_url):
    sid = auth_vcenter(api_user,api_pass)
    print('Requesting Page: {}'.format(req_url))
    resp = requests.get(req_url,verify=False,headers={'vmware-api-session-id':sid})
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp

# get list of all VMs filtered by host. prints to screen and to 'vms.json' file.
def getvm(hostid):
    resp = get_api_data(f'{api_url}/vcenter/vm?filter.hosts={hostid}') # URL, lookup using https://VCSA/apiexplorer/
    j = resp.json()
    data = json.dumps(j)
    print(data)
    with open("vms.json", "w") as write_file:
        json.dump(j, write_file)
    
# get the specified hosts 'id'
def get_vmbyHost():
    resp = get_api_data(f'{api_url}/vcenter/host?filter.names={hostname}')
    jhosts = resp.json()
    y = jhosts['value']
    hostid = y[0]['host']
    print(f'ID of host is {hostid}')
    getvm(hostid)

def main():
    get_vmbyHost()

main()

