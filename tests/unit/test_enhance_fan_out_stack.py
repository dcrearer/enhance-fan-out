import aws_cdk as core
import aws_cdk.assertions as assertions

from enhance_fan_out.enhance_fan_out_stack import EnhanceFanOutStack

# example tests. To run these tests, uncomment this file along with the example
# resource in enhance_fan_out/enhance_fan_out_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EnhanceFanOutStack(app, "enhance-fan-out")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
