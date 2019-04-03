#!/usr/bin/env python

from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint

def write_to_cm_pass():
    api_instance = client.CoreV1Api()

    sec = client.V1Secret()
    sec.type = "Opaque"
    sec.data = {"username": "TestUser", "password": "TestPass"}
    name = 'account-pwd'
    namespace = 'testnewautonity'
    body = sec
    try:
        api_response = api_instance.patch_namespaced_secret(name, namespace, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when write to secret: %s\n" % e)

def main():

    # it works only if this script is run by K8s as a POD
    config.load_incluster_config()
    write_to_cm_pass()


if __name__ == '__main__':
    main()
