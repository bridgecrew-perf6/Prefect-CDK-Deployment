
# Prefect Flow CDK Deployment

The repository explains how to deploy a complete Prefect Orchestration layer using ECS Fargate on Ubuntu 18.04 or Amazon AMI.

## Architecture and Infrastructure 

Starting with ECS Cluster setup and architecuture. Cluster type Fargate is used for this project. The architecture consists of one VPC consisting of 2 public subsnets spread
across two availiablity zones. These public subnets are connected through an application load balancer and can access internet through NAT gateway. Each of the public subnets
are running one Fargate container as a service all times.

Other then the ones mentioned above, two S3 buckets would be required. One for saving flow storages and other for saving results of ELT task. 

The app deploys prefect flow scrapper that scraps top gainers cryptocurrency from coin marketcap. The flow is a classic Extract, Transform and Load - ELT and has three components:
  1. **Extract task:** Here the requests and beautifulSoup libraries are used to scrap relevant data from webpage.
  2. **Transform task:** This tasks transforms currency unit from USD to AUD.
  3. **Load task:** This task saves the transformed dataset into S3 container.

All of these tasks are then configured into a prefect flow. This flow can be found in the [following repository](https://github.com/usamatrq94/Prefect-ECSAgent-Deploy).
Prefect flows and its deployment configuration are wrapped into a Dockerfile, which can also be found in above repository.

The Dockerfile is build into an image and then its pushed to ECR public repository. This can be accessed [here](https://gallery.ecr.aws/s0c5i6w0/prefect-service-image).
This image is used as base container image for ECS task defination. The image is provided to Application Load Balanced Fargate Service in prefect_ecs_stack.py. 

As for ECS Cluster, it will be running two Containers, first will be running as a service, prefect backend Cloud, that will be polling prefect cloud api for workloads,
once the a workload is available, the second container is started for resolving the prefect workload.

## Deployment Procedure

This complete infrastructre can be deployed through following steps:
  1. Installing Node and AWS CDK
  2. Configuring AWS CDK
  3. Installing git and cloning git repository
  4. Activating virtual envoirnment and installing dependencies
  5. Sythesizing AWS Stack
  6. Deploying AWS Stack

Lets start

### 1. Installing Node and AWS CDK

For this project, I'll be using `Node==v16.31.1` and `CDK==2.1.0`.

Installation for Node on windows can be found [here](https://phoenixnap.com/kb/install-node-js-npm-on-windows). 

For installing CDK
```
python -m pip install aws-cdk-lib
```
### 2. Configuring AWS CDK

Now to provide Access Key ID, Secret Access Key and default region to connect to your AWS user. We need to make sure that the provided AWS user has required permissions to create resources
for the stack. We can do this by:
```
aws configure
```
### 3. Installing git and cloning git repository

Run the following code:
```
sudo apt install git-all
git clone https://github.com/usamatrq94/Prefect-CDK-Deployment.git
cd Prefect-CDK-Deployment
```
### 4. Activating virtual envoirnment and installing dependencies

We can start by activating the virtualenv on windows and install requirements by:
```
% .venv\Scripts\activate.bat
pip install -r requirements.txt
```
### 5. Sythesizing AWS Stack

Now we need synthesize the CloudFormation template for this code.
```
cdk synth
```
### 6. Deploying AWS Stack

Once the syntheis is complete, it provides a cloudformation template for all infrastructure. 
Sometimes, CDK reqires you to bootstrap, you can do this using following code below:
```
cdk bootstrap
```
Once this is done, we are ready to deploy our infrastructure as code
```
cdk deploy
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk destroy`     remove all resources and stack


