# ibft-keys-generator
Generate set of validators keys for IBFT

Build
```
docker build -t ibft-keys-generator .
```
Run and connect to remote kubernetes cluster using default local kube config
```
./cm_writer/main.py -k remote
```

Run and connect to kube-apiserver from internal pod
```
docker run -ti ibft-keys-generator
```

Get secret from configmap
```bash
NAMESPACE=testnewautonity
kubectl -n $NAMESPACE get secret account-pwd -o json | jq -r .data.account.pwd | base64 --decode
```