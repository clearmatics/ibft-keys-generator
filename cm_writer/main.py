#!/usr/bin/env python

import base64
import argparse
import secrets
import string
import sha3
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint
from ecdsa import SigningKey, SECP256k1


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


def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out


def generate_keys():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    return {'private_key': priv.to_string().hex(), 'pub_key': pub.hex(), 'address': checksum_encode(address)}


def write_keys(peers, kind, namespace):
    api_instance = client.CoreV1Api()
    sec = client.V1Secret()
    sec.type = 'Opaque'
    payload = {}
    for peer in peers:
        payload[peer['id']] = base64.b64encode(peer['private_key'].encode()).decode()
    sec.data = payload
    try:
        api_response = api_instance.patch_namespaced_secret(kind, namespace, sec)
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
    parser.add_argument('--validators',
                        dest='validators',
                        default=4,
                        type=int,
                        help='number of validators. Should be more than 4 for ibft (default: %(default)s)'
                        )
    parser.add_argument('--observers',
                        dest='observers',
                        default=1,
                        type=int,
                        help='number of observers minimum 1 (default: %(default)s)'
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

    validators = []
    for i in range(args.validators):
        validator = generate_keys()
        validator['id'] = i
        validators.append(validator)
        print(validator)
    write_keys(validators, 'validators', namespace)

    observers = []
    for i in range(args.observers):
        observer = generate_keys()
        observer['id'] = i
        observers.append(observer)
        print(observer)
    write_keys(observers, 'observers', namespace)


if __name__ == '__main__':
    main()
