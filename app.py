#!/usr/bin/env python3
import os

import aws_cdk as cdk

from enhance_fan_out.enhance_fan_out_stack import EnhanceFanOutStack


app = cdk.App()
EnhanceFanOutStack(app, "EnhanceFanOutStack",
    env=cdk.Environment(account=os.environ['AWS_ACCOUNT_ID'], region=os.environ['AWS_REGION']),
    )

app.synth()