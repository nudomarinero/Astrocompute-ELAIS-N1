from __future__ import print_function
import boto.utils
import boto.ec2

region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
id = boto.utils.get_instance_metadata()['instance-id']

instances = conn.get_only_instances()
for instance in instances:
    if instance.id == id:
        print(instance.tags.get("band", None))