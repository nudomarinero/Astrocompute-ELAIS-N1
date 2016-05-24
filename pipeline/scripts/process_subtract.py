from __future__ import print_function
import boto.utils
import boto.ec2
import sh
from get_band import get_tag


def download_data():
    """
    Download the pretarget data using the script created
    """
    download = sh.Command("/home/ubuntu/download_data_pretarget.sh")
    download()

def run_pipeline():
    """
    Run the generic pipeline and send notification in case of error
    """
    #pipeline = sh.Command("")
    pass

def upload_data():
    """
    Upload the computed data
    """
    upload = sh.Command("/home/ubuntu/upload_data_subtract.sh")
    upload()

def umount_and_remove_disk(remove=False):
    """
    Umount the scratch area and remove the volume
    """
    pass
   
def terminate_instance():
    """
    Terminate the instance
    """
    region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
    iid = boto.utils.get_instance_metadata()['instance-id']
    conn = boto.ec2.connect_to_region(region)
    conn.terminate_instances(instance_ids=[iid])
          

if __name__ == "__main__":
    download_data()
    # download data
    # run the pipeline
    # upload data
    # umount and remove disk
    # terminate instance
