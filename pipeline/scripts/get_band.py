from __future__ import print_function
import boto.utils
import boto.ec2

region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
iid = boto.utils.get_instance_metadata()['instance-id']

conn = boto.ec2.connect_to_region(region)

instances = conn.get_only_instances()
for instance in instances:
    if instance.id == iid:
        print(instance.tags.get("band", None))