#!/bin/bash

# set -o errexit
set -o pipefail


function startMinikube() {
    # Start up minikube
    minikube start
    # Change the docker environment to docker
    eval $(minikube docker-env)
    # Build Backend Image
    docker-compose -f docker/dev/docker-compose.yml build
}

function createKubernetes() {
    kubectl create -f minikube/secrets.yaml
    kubectl create -f minikube/deployments.yaml
    kubectl create -f minikube/services.yaml
    kubectl create -f minikube/ingress.yaml
}

function migrateDatabase() {
    until [[ "$(kubectl get pods --selector="app=soc-backend" --use-openapi-print-columns | grep sandbox-soc-backend --max-count=1 |  awk '{print $1;}')" =~ "sandbox-soc-backend" ]]; do
        echo "Waiting for backend to initialize"
        sleep 1
    done
    until [[ "$(kubectl get pods --selector="app=soc-backend" | grep sandbox-soc-backend --max-count=1 | awk '{print $2;}')" =~ "1/1" ]]; do
        echo "Waiting for backend to be ready"
        sleep 10
    done
    echo "Backend is up and ready"
    sandbox_pod=$(kubectl get pods --selector="app=soc-backend" --use-openapi-print-columns | grep sandbox-soc-backend --max-count=1 |  awk '{print $1;}')
    kubectl exec  "${sandbox_pod}" -- psql-h sandbox-soc-database
	kubectl exec "${sandbox_pod}" -- python manage.py db upgrade -d prod-stag-migrations
}

function seedDatabase() {
    sandbox_pod=$(kubectl get pods --selector="app=soc-backend" --use-openapi-print-columns | grep sandbox-soc-backend --max-count=1 |  awk '{print $1;}')
    if [[ "${sandbox_pod}" =~ "sandbox-soc-backend" ]]; then
        kubectl exec "${sandbox_pod}" -- python manage.py seed
    else
        echo "The backend application is not up. Maybe it has not yet been set up"
    fi 
}

function deployBackend() {
    echo "ASdfasdfadsf"
}
function tearDown(){
    if [[ -n "$(minikube status | grep "minikube: Running")" ]]; then
       echo "Tearing down minikube" 
       minikube delete
    fi
}


function main {
    startMinikube
    createKubernetes
    migrateDatabase
}

"$@"
