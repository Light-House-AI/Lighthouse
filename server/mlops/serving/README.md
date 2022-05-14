# Serving part of the deployment phase

## About

- This phase of the MLOps process focuses on deploying models to Kubernetes API Server using the [python Kubernetes client library](https://github.com/kubernetes-client/python) functions.
- The aim is to deploy models to production through the automated creation of Kubernetes resources.

## Structure
```
|__ init.py
|
|__ .gitignore
|
|__ README.md
|
|__ requirements.txt                <- dependencies to install before running the program
|
├── src                             <- Server code.
│   │
│   ├── main.py                     <- Entry point of the application
│   │
│   ├── k8s_client                  <- Resources classes that call the manipulate the Kubernetes API server
│   │   ├── cluster_ip.py      
│   │   ├── deployment.py 
│   │   ├── helpers.py 
│   │   ├── secret.py 
│   │   └── init.py        
│   │
│   ├── services                    <- Functions responsible for resources management & manipulation
│   │   ├── constants.py    
│   │   ├── helpers.py
│   │   ├── run.py 
│   │   ├── script.py    
│   │   ├── startup.py    
│   │   ├── vars.py  
│   │   └── init.py        
│   │
|_____

```
## Usage
- The entry point to the application is through the invoking of one of the 3 available functions 
    1. deploy 
    2. delete
    3. update-ingress
    ```bash
    deploy model_id
    delete model_id
    update_ingress [model_id,model_id2,...]
    ```
- The above 3 functions provide an abstraction for the configuration done at the background to make it easier to use the code. 
    - We could say this application is a user friendly version of **kubectl** for deploying models.


## Main Functionalities
1. Creating a deployment & cluster ip together and adding the model path to the ingress rules.
2. Deleting a deployment & cluster ip together and removing the model path from the ingress rules.
3. Updating ingress is for re-population of the ingress paths list when the server stops.


### Inner Functionalities
1. Creating Deployments
2. Creating Cluster IPs
3. Creating Ingress
4. Creating secrets for the deployments

