# Serving part of the deployment phase

## About

- This phase of the MLOps process focuses on deploying models to Kubernetes API Server using the [python Kubernetes client library](https://github.com/kubernetes-client/python) functions.
- The aim is to deploy models to production through the automated creation of Kubernetes resources.

## Main Functionalities
1. Creating a deployment & cluster ip together and adding the model path to the ingress rules.
2. Deleting a deployment & cluster ip together and removing the model path from the ingress rules.
3. Updating ingress is for re-population of the ingress paths list when the server stops.


### Inner Functionalities
1. Creating Deployments
2. Creating Cluster IPs
3. Creating Ingress
4. Creating secrets for the deployments

- The above 3 functions provide an abstraction for the configuration done at the background to make it easier to use the code. 
    - We could say this application is a user friendly version of **kubectl** for deploying models.

## Usage
- The entry point to the application is through the invoking of one of the 3 available functions 
    1. deploy 
    2. delete 
    3. update-ingress
    ```bash
    deploy <project_id> <deployment_type> <champion_model_id> <challenger_model_id>
    delete <project>
    update_ingress [<project_id1>,<project_id2>,...]
    ```
### To integrate with the wrapper
- Deployment type should take a value of "single" or "champion/challenger"
    - If not specified default is "single"
- Challenger model id (second model id) may not be passed if the deployment is a single type.

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
