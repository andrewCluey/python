from pyVim.connect import SmartConnect      # SmartConnect is a function to simplify vCenter(si) connections and is from connect.py (itself a part of pyvmomi/pyVim)
from pyVmomi import vim                     # vim to work with our views
from pyVmomi import vmodl
import ssl                                  # To deal with our SSL things
import requests
import atexit
import argparse
import getpass


# Python program to authenticate and print a friendly encouragement!
s = ssl._create_unverified_context()
s.verify_mode = ssl.CERT_NONE

def get_args():
    # Get command line args from the user.
    
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    # because -h is reserved for 'help'
    #  we use -s for service
    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSphere service to connect to')

    # because we want -p for password, we use -o for port
    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to use when connecting to host')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use when connecting to host')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))
    return args


def main():
    # Simple command-line program for listing the virtual machines on a system.
    args = get_args()

    try:
        service_instance = SmartConnect(host='+host+',
                                                user='+user+',
                                                pwd=args.password,
                                                sslContext=s,
                                                port=int(args.port))

        print("\n")
        print("You are connected")
        # NOTE (hartsock): only a successfully authenticated session has a session key aka session id.
        session_id = service_instance.content.sessionManager.currentSession.key
        session_msg = f'current session id: {session_id}'
        print(session_msg)
        print(service_instance.currentTime())
        print("\n")
        print("https://github.com/vmware/pyvmomi-community-samples")
        print("\n\n")

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0

# Start program
if __name__ == "__main__":
    main()