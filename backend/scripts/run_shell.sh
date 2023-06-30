#!/bin/bash
rancher kubectl exec -it `rancher kubectl get pods -o json --insecure-skip-tls-verify --namespace=[NAMESPACE] | jq '[ .items[] | select(.spec.containers[0].name == "[NAME]")] | .[0] | .metadata.name' | tr -d '"'` /bin/bash  --insecure-skip-tls-verify --namespace=[NAMESPACE]
