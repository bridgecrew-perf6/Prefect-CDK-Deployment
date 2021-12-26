from aws_cdk import (
    Stack,
    aws_ecs,
    aws_ecs_patterns,
    aws_ec2,
    aws_iam
)
from aws_cdk.aws_autoscaling import CpuUtilizationScalingProps
from constructs import Construct

class PrefectEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code below deploys infrastructure as code. The core infrastructure consists of a
        # VPC, with two public subnets across two availabilty zones in region ap-southeast-2 aka 
        # Sydney connected through a load balancer. The ECS cluster with launch type Fargate
        # is used with Service that runs Prefect polling agent which polls Prefect cloud for any
        # executable flows. 

        # This code automatically deploys underlyling infrastructure like VPC's, subnets, IAM roles,
        # policies, security groups etc.

        # For this code, I am using predefined VPC and execution roles. There is nothing special about 
        # these resources, I am just using them to avoid slow creating and deployment times again and
        # again. Everthing can be created from scratch by removing vpc and execution roles below. The 
        # code automatically creates necessary resources. 

        vpc = aws_ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-087c289437e81ba1c")
        execution_role = aws_iam.Role.from_role_arn(
            self, "ecsTaskExecutionRole", 
            role_arn="arn:aws:iam::776883799019:role/ecsTaskExecutionRole"
            )

        # Start my creating an ECS Cluster named Fargate Cluster. The cluster will continuously run a service
        # across 2 subnets in 2 availability zones. The service will continuously poll prefect cloud for flows,
        # if any flow is received, the execution role spins another Task in the cluster to execute the flow and 
        # terminates itself once it is completed. 

        ecs_cluster = aws_ecs.Cluster(self, id="FargateCluster", cluster_name="FargateCluster", vpc=vpc)
        
        # The code below creates a Fargate based Load balanaced ECS service. We have to specify details for launch
        # type fargate. We want one task to be running across each availabilty zone.  
        # The container image for this instance is fetched from ECR public repository. The full repository and 
        # dockerfile for the image can be found at https://github.com/usamatrq94/Prefect-ECSAgent-Deploy
        # The repository has prefect flow registration and execution settings.

        self.prefect_service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Prefect-Service-Cluster",
            cluster=ecs_cluster,
            desired_count=1,
            cpu=512,
            memory_limit_mib=1024,
            task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_ecs.ContainerImage.from_registry("public.ecr.aws/s0c5i6w0/prefect-service-image:production"),
                execution_role=execution_role
            )
        )

