import boto3
import datetime
import json
from botocore.client import ClientError

region = 'us-west-2'
ec2 = boto3.resource('ec2')
# s3 = boto3.resource('s3', region_name=region)

bucket_name = 'lythchr-isengard'

def handler(event, context):
    filters = [
     {
      'Name': 'instance-state-name',
      'Values': ['*']
     }
    ]
    
    instances = ec2.instances.filter(Filters = filters)
    
    RunningInstances = []
    
    for instance in instances:
        RunningInstances.append(instance.id)
    
    instanceList = json.dumps(RunningInstances)
    ec2.stop_instances(
        InstanceIds=RunningInstances,
        Hibernate=True,
        DryRun=False,
        Force=True
    )
    data = {
        'output': 'Stopped instances',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'instanceList': instanceList
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
