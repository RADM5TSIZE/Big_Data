kubectl apply -f db_mysql.yaml
sleep 60
kubectl apply -f memcached.yaml
sleep 60
kubectl apply -f webapp.yaml

