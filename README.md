# ibft-keys-generator
Generate set of validators and observers keys for IBFT:
- account password
- for each validator and observer: `private key`, `public key`, `address`

## External Dependencies
- docker 18.09.2  
- kube-apiserver v1.11.8

Data will be added to existing secrets and ConfigMaps:


| type      | name                  | keys                     |
|-----------|-----------------------|--------------------------|
| secret    | account-pwd           | `account.pwd`            |
| secret    | validators, observers | `*.private_key`          | 
| ConfigMap | validators, observers | `*.pub_key`, `*.address` | 


# Build
```
docker build -t ibft-keys-generator .
```

# Usage

Run and connect to remote kubernetes cluster using default local kube config
```
./cm_writer/main.py -k remote -n test --validators 4 --observers 1
```

Run and connect to kube-apiserver from internal pod (inside kubernetes cluster)
```
docker run -ti clearmatics/ibft-keys-generator
```

# Options
```
usage: main.py [-h] [-k {pod,remote}] [-n NAMESPACE] [--validators VALIDATORS]
               [--observers OBSERVERS]

Generate set of keys for initialising the network and deploy it to kubernetes
etcd

optional arguments:
  -h, --help            show this help message and exit
  -k {pod,remote}       Type of connection to kube-apiserver: pod or remote
                        (default: pod)
  -n NAMESPACE          Kubernetes namespace.
  --validators VALIDATORS
                        number of validators. Should be more than 4 for ibft
                        (default: 4)
  --observers OBSERVERS
                        number of observers minimum 1 (default: 1)
```


# Get secret from ConfigMap

```bash
NAMESPACE=test
kubectl -n $NAMESPACE get secrets account-pwd -o 'go-template={{index .data "account.pwd"}}' | base64 --decode; echo ""
```
Get private key of first observer (id == 0)

```bash
NAMESPACE=test
kubectl -n $NAMESPACE get secrets observers -o 'go-template={{index .data "0.private_key"}}' | base64 --decode; echo ""
```

Get list of addresses for each validator
```bash
NAMESPACE=test
kubectl -n $NAMESPACE get configmap validators -o yaml |grep .address

```
