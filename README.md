# Image of digit to speech web app

Disclaimer: it's study project just FYI


## What that do
Convert image to speech

## How it work
We have 4 microservices and every do separated job. Model trained by project 'tensor'.

### simple-frontend
Simple static html with nginx as base image.

### facade-api
Facade microservice what proxy request to needed microservices and return data to frontend.

### image-to-text
Convert image of digit to text (1, 2, 3, ...). Microservice use model what trained in project 'tensor'.

### translate-api
Get digit and convert it to speech by Google text to speech technology

### tensor
Project where train model for detecting digits from image.


## Installation

#### 
Install Minikube and Docker.

#### Set Minikube to Use the Docker Daemon on Your Local Machine
```bash
minikube config set driver docker
```
#### Run Minikube. For best perfomance you can use all cpus of computer
```bash
minikube start --cpus max
```
#### Use script to deploy all microservices to Minikube
```bash
# Make the deploy file executable
deploy-projects.sh
```

## Using the App

**Frontend:** http://localhost:8080/