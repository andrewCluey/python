import requests
import requests.packages.urllib3
from requests.auth import HTTPBasicAuth
import json
import urllib3
import getpass

api_url = 'https://IP_HostnameOfVCSA/rest'
api_user = 'username'
api_pass = getpass.getpass(prompt='Enter your password')

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

def get_vcenter_health_status():
    resp = get_api_data(f'{api_url}/appliance/health/system')
    j = resp.json()
    print('vCenter Health: {}'.format(j['value']))

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Disable SSL warnings
    get_vcenter_health_status()

main()
