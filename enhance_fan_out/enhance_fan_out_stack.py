from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_kinesis as kinesis,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_lambda_event_sources as lambda_events,
)
from constructs import Construct


class EnhanceFanOutStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Kinesis Data Stream
        stream = kinesis.Stream(self, "IngestKinesisStream",
            stream_name="ingest-kinesis-stream",
            shard_count=5,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create DynamoDB Table
        table = dynamodb.Table(self, "IngestDynamoDBTable",
            table_name="ingest-dynamodb-table",
            partition_key=dynamodb.Attribute(name="sensorId", type=dynamodb.AttributeType.NUMBER),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create Lambda function
        consumer_lambda = lambda_.Function(self, "ConsumerLambda",
            runtime=lambda_.Runtime.PYTHON_3_10,
            function_name="ingest-consumer-lambda",
            memory_size=256,
            timeout=Duration.seconds(90),
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("assets/"),
            environment={
                "STREAM_NAME": stream.stream_name,
                "TABLE_NAME": table.table_name
            }
        )

        # Grant read permissions to the Lambda function
        stream.grant_read(consumer_lambda)

        # Grant read/write permissions to the Lambda function for DynamoDB
        table.grant_read_write_data(consumer_lambda)

        # Create enhanced fan-out consumer
        enhanced_consumer = kinesis.CfnStreamConsumer(self, "EnhancedConsumer",
            consumer_name="ingest-enhanced-consumer",
            stream_arn=stream.stream_arn
        )

        # Add Kinesis event source to Lambda with enhanced fan-out
        consumer_lambda.add_event_source(lambda_events.KinesisEventSource(stream,
            starting_position=lambda_.StartingPosition.LATEST,
            batch_size=100,
            parallelization_factor=5
        ))