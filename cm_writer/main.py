#!/usr/bin/env python

import base64
import argparse
import secrets
import string
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint


def write_account_pass(namespace):
    # Generate password for account and write it to k8s secret

    api_instance = client.CoreV1Api()

    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(30))  # for a 30-character password

    sec = client.V1Secret()
    sec.type = 'Opaque'
    sec.data = {'account.pwd': base64.b64encode(password.encode()).decode()}
    name = 'account-pwd'
    body = sec
    try:
        api_response = api_instance.patch_namespaced_secret(name, namespace, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when write to secret: %s\n" % e)


def main():
    parser = argparse.ArgumentParser(description='Generate set of keys for initialisation networks and deploy it to kubernetes secrets')
    parser.add_argument('-k',
                        dest='kubeconf_type',
                        default='pod',
                        choices=['pod', 'remote'],
                        help='Type of connection to kube-apiserver: pod or remote (default: %(default)s)'
                        )
    parser.add_argument('-n',
                        dest='namespace',
                        default='default',
                        help='Kubernetes namespace.'
                        )
    args = parser.parse_args()
    pprint(vars(args))

    if args.kubeconf_type == 'pod':
        config.load_incluster_config()
        f = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r")
        namespace = f.readline()
        f.close()
    elif args.kubeconf_type == 'remote':
        config.load_kube_config()
        namespace = args.namespace

    write_account_pass(namespace)

if __name__ == '__main__':
    main()
