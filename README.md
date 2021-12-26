
# Prefect Flow CDK Deployment

The repository explains how to deploy a complete Prefect Orchestration layer using ECS Fargate.

## Architecture and Infrastructure 

Starting with ECS Cluster setup and architecuture. Cluster type Fargate is used for this project. The architecture consists of one VPC consisting of 2 public subsnets spread
across two availiablity zones. These public subnets are connected through an application load balancer and can access internet through NAT gateway. Each of the public subnets
are running one Fargate container as a service all times.

The app deploys prefect flow scrapper that scraps top gainers cryptocurrency from coin marketcap. The flow has three components:
  1. **Extract task:** Here the requests and beautifulSoup libraries are used to scrap relevant data from webpage.
  2. **Transform task:** This tasks transforms currency unit from USD to AUD.
  3. **Load task:** This task saves the transformed dataset into S3 container.

All of these tasks are then configured into a prefect flow. This flow can be found in the [following repository](https://github.com/usamatrq94/Prefect-ECSAgent-Deploy).
Prefect flows and its deployment configuration are wrapped into a Dockerfile, which can also be found in above repository.

The Dockerfile is build into an image and then its pushed to ECR public repository. This can be accessed [here](https://gallery.ecr.aws/s0c5i6w0/prefect-service-image).
This image is used as base container image for ECS task defination. The image is provided to Application Load Balanced Fargate Service in prefect_ecs_stack.py. 

## Deployment Procedure

This project is set up like a standard Python project.  The initialization process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3` (or `python` for Windows) executable in your path with access to the `venv`
package. 

You can start by activating the virtualenv on windows like this:

```
% .venv\Scripts\activate.bat
```
Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```
At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```
Once the syntheis is complete, it provides a cloudformation template for all infrastructure. Sometimes, CDK reqires you to bootstrap, you can do this using following code below:
```
$ cdk bootstrap
```
Once this is done, we are ready to deploy our infrastructure as code
```
$ cdk deploy
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk destroy`     remove all resources and stack


