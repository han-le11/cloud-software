The goal is to implement and dockerize a web-based service leveraging FastAPI and MongoDB, then later deploy it to a Kubernetes cluster with the help of Kind.

Repo structure:
```
fastapi-k8s
└── src
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py

└── manifests
    ├── persistent-volume.yaml
    ├── mongo.yaml
    ├── fastapi.yaml

└── manifests.zip 
```

The manifest files can be applied by using the following command:
```
kubectl apply -f <FILENAME>
```

In this application, the manifest files are applied in the order below:
```
kubectl apply -f persistent-volume.yaml
kubectl apply -f mongo.yaml
kubectl apply -f fastapi.yaml
```

To interact with deployed services, you can use port-forwarding. For instance, to interact with the FastAPI application, you can run:
```
kubectl port-forward service/fast-api-service 5000:5000
```

similarly, to interact with the MongoDB database:
```
kubectl port-forward service/mongo 31048:27017
```