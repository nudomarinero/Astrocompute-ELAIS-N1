from __future__ import print_function
import boto.utils
import boto.ec2

def get_tag(tag_name):
    """
    Get the content of a tag for the current instance.
    """
    region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
    iid = boto.utils.get_instance_metadata()['instance-id']

    conn = boto.ec2.connect_to_region(region)

    instances = conn.get_only_instances()
    for instance in instances:
        if instance.id == iid:
            return instance.tags.get(tag_name, None)

def get_band():
    """
    Get the band number for the current instance.
    The band number should be stored in a tag called "band"
    """
    return get_tag("band")
   
if __name__ == "__main__":
    band = get_band()
    print(band)
    