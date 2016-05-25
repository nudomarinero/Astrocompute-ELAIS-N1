from __future__ import print_function
import boto.utils
import boto.ec2
import sh
from sh import sudo
from get_band import get_tag
import boto.sns
import logging
import traceback
import ConfigParser


#logging.basicConfig(
    #filename="pipeline.log", 
    #level=logging.DEBUG)

# General configuration
config = ConfigParser.ConfigParser()
config.read('/home/ubuntu/.sns_conf')
topicarn = config.get("arn", "topicarn")

# General information
region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
iid = boto.utils.get_instance_metadata()['instance-id']
band = get_tag("band")
dataset = get_tag("dataset")


# Auxiliary functions
def notify(message, subject=None):
    """
    Notify the user using sns
    """
    snsc = boto.sns.connect_to_region(region)
    if subject is None:
        subject = "Notification LOFAR AWS" 
    publication = snsc.publish(topicarn, message, subject=subject)

def launch(step):
    """
    Launch one of the steps but notify the user if there is an error
    """
    try:
        step()
    except:
        fname = step.__name__
        error_message = traceback.format_exc()
        message = ("Exception in LOFAR AWS subtract pipeline\n"+
            "Dataset: {}\n".format(dataset)+
            "Band:    {}\n".format(band)+
            "Step:    {}\n".format(fname)+
            "Error:\n"+
            error_message
            )
        notify(message, 
               subject="Exception LOFAR AWS subtract; step: {}; band: {}".format(fname, band))
        raise
    
    
## Steps
def download_data():
    """
    Download the pretarget data using the script created
    """
    # TODO: Initial checks and cleaning
    download = sh.Command("/home/ubuntu/download_data_pretarget.sh")
    for line in download(_iter=True):
        print(line)
    # TODO: Final checks and notification

def run_pipeline():
    """
    Run the generic pipeline and send notification in case of error
    """
    pipeline = sh.Command("/opt/LofIm/bin/genericpipeline.py",
                          "-c",
                          "/home/ubuntu/astrocompute/pipeline/generic_pipeline/pipeline.cfg")
    for line in pipeline("/home/ubuntu/astrocompute/pipeline/generic_pipeline/pre_facet_subtract.parset",
                         _iter=True):
        print(line)

def upload_data():
    """
    Upload the computed data
    """
    upload = sh.Command("/home/ubuntu/upload_data_subtract.sh")
    for line in upload(_iter=True):
        print(line)

def umount_and_remove_disk(remove=False):
    """
    Umount the scratch area and remove the volume
    """
    pass
   
def terminate_instance():
    """
    Terminate the instance
    """
    conn = boto.ec2.connect_to_region(region)
    conn.terminate_instances(instance_ids=[iid])


if __name__ == "__main__":
    launch(download_data)
    launch(run_pipeline)
    launch(upload_data)
    #launch(umount_and_remove_disk) # Not implemented yet
    launch(terminate_instance)

