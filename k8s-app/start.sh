kubectl apply -f 01-mysql-deployment.yaml
kubectl apply -f 02-k8s-mysql-service.yaml
kubectl apply -f 03-memcached-deployment-and-service.yaml
kubectl apply -f 04-app-deployment-minikube.yaml
kubectl apply -f 04-app-service-and-ingress.yaml
kubectl apply -f webapp.yaml
kubectl scale deployment memcache-deployment --replicas=2
kubectl scale deployment my-super-app-deployment --replicas=2
