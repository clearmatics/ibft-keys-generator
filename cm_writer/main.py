#!/usr/bin/env python

import base64
import argparse
import secrets
import string
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint


def write_to_cm_pass():
    api_instance = client.CoreV1Api()

    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(30))  # for a 30-character password
    print('Password:' + password)
    print('Base64:' + base64.b64encode(password.encode()).decode())

    sec = client.V1Secret()
    sec.type = 'Opaque'
    sec.data = {'account.pwd': base64.b64encode(password.encode()).decode()}
    name = 'account-pwd'
    namespace = 'testnewautonity'
    body = sec
    try:
        api_response = api_instance.patch_namespaced_secret(name, namespace, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when write to secret: %s\n" % e)


def main():
    parser = argparse.ArgumentParser(description='Generate set of keys for initialisation networks and deploy it to kubernetes secrets')
    parser.add_argument('-k','--kube-config',
                        dest='kubeconf_type',
                        default='pod',
                        choices=['pod', 'remote'],
                        help='Type of connection to kube-apiserver: pod or remote (default: %(default)s)'
                        )
    args = parser.parse_args()
    pprint(vars(args))

    if args.kubeconf_type == 'pod':
        config.load_incluster_config()
    elif args.kubeconf_type == 'remote':
        config.load_kube_config()


    write_to_cm_pass()

if __name__ == '__main__':
    main()



kubectl get pods -o json | jq


# Get ExternalIPs of all nodes
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'\

                              

                              '.items[].spec.containers[].env[]?.valueFrom.secretKeyRef.name'