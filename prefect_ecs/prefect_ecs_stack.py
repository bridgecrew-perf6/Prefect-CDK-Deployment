from aws_cdk import (
    # Duration,
    aws_stepfunctions_tasks,
    aws_stepfunctions,
    Stack,
    aws_ecs,
    aws_ecs_patterns,
    aws_ec2,
    aws_iam,
    # aws_sqs as sqs,
)
from aws_cdk.aws_autoscaling import CpuUtilizationScalingProps
from constructs import Construct

class PrefectEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "PrefectEcsQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        vpc = aws_ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-087c289437e81ba1c")
        ecs_cluster = aws_ecs.Cluster(self, id="FargateCluster", cluster_name="FargateCluster", vpc=vpc)
        execution_role = aws_iam.Role.from_role_arn(self, "ecsTaskExecutionRole", role_arn="arn:aws:iam::776883799019:role/ecsTaskExecutionRole")

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

        # task_definition = aws_ecs.TaskDefinition(
        #     self, "Prefect-task-definintion",
        #     memory_mib="1024", cpu="512",
        #     compatibility=aws_ecs.Compatibility.FARGATE,
        #     execution_role=execution_role
        # )

        # container_definition = task_definition.add_container(
        #     "Prefect-ECS-Container",
        #     image=aws_ecs.ContainerImage.from_registry("public.ecr.aws/s0c5i6w0/prefect-service-image:production"),
        #     memory_limit_mib=512
        # )

        # run_task = aws_stepfunctions_tasks.EcsRunTask(
        #     self, "Prefect-polling-agent",
        #     integration_pattern=aws_stepfunctions.IntegrationPattern.RUN_JOB,
        #     cluster=ecs_cluster,
        #     task_definition=task_definition,
        #     container_overrides=[
        #         aws_stepfunctions_tasks.ContainerOverride(
        #             container_definition=container_definition
        #         )
        #     ],
        #     launch_target=aws_stepfunctions_tasks.EcsFargateLaunchTarget(
        #         platform_version=aws_ecs.FargatePlatformVersion.LATEST
        #     )
        # )

        # run_task
