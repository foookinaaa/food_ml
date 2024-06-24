# Kubernetes research
```commandline
minikube start

kubectl apply -f src/kubernetes/configmap.yaml
kubectl apply -f src/kubernetes/deployment.yaml
kubectl apply -f src/kubernetes/service.yaml
kubectl apply -f src/kubernetes/ingress.yaml
```

```commandline
minikube ip
```
ans: 192.168.49.2
```commandline
sudo nano /etc/hosts
```
add to hosts line:
192.168.49.2 mynginx.local

check access:
```commandline
 minikube service nginx-service
```
fix m1 error access in k3d:
```commandline
kubectl -n kube-system port-forward service/traefik 1800:80
```
access on: http://mynginx.local:1800
```commandline
 minikube stop
```
