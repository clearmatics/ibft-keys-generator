#!/usr/bin/env python

from kubernetes import client, config

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

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()
