#!/bin/sh
kubectl apply -f postgres/postgres-configmap.yaml
kubectl apply -f postgres/postgres-pvc.yaml
kubectl apply -f postgres/postgres-deployment.yaml
kubectl apply -f postgres/postgres-service.yaml

kubectl apply -f backend/backend-deployment.yaml
kubectl apply -f backend/backend-service.yaml

kubectl apply -f fpl-app/frontend-deployment.yaml
kubectl apply -f fpl-app/frontend-service.yaml

kubectl apply -f cronjob/pushpreds-cronjob.yaml

kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml