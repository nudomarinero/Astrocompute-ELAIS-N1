from __future__ import print_function
import os
import boto.utils
import boto.ec2
import sh
from sh import sudo
from glob import glob
from get_band import get_tag
import boto.sns
import logging
import traceback
import ConfigParser

#logging.basicConfig(
    #filename="pipeline.log", 
    #level=logging.DEBUG)
    ## Logger configuration
if os.path.exists("/home/ubuntu/logging.conf"):
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
else:
    # Start
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)   
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # Log to STDOUT
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # Log to file
    file_name = "pipeline_prefactor.log"
    fh = logging.FileHandler(file_name) 
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.info('\n')


# General configuration
config = ConfigParser.ConfigParser()
config.read('/home/ubuntu/.sns_conf')
topicarn = config.get("arn", "topicarn")

# General information
region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
iid = boto.utils.get_instance_metadata()['instance-id']
band = get_tag("band")
dataset = get_tag("dataset")


## Auxiliary functions
def notify(message, subject=None):
    """
    Notify the user using SNS
    """
    snsc = boto.sns.connect_to_region(region)
    if subject is None:
        subject = "Notification LOFAR AWS" 
    publication = snsc.publish(topicarn, message, subject=subject)

def launch(step):
    """
    Launch one of the steps but notify the user if there is an error
    """
    fname = step.__name__
    logging.info("Start step {}".format(fname))
    try:
        step()
    except:
        logging.error("Exception in step {}".format(fname))
        error_message = traceback.format_exc()
        message = ("Exception in LOFAR AWS prefactor pipeline\n"+
            "Dataset: {}\n".format(dataset)+
            "Band:    {}\n".format(band)+
            "Step:    {}\n".format(fname)+
            "Error:\n"+
            error_message
            )
        notify(message, 
               subject="Exception LOFAR AWS prefactor; step: {}".format(fname))
        raise
    logging.info("Finish step {}".format(fname))   
    
    
## Steps
def download_cal_data():
    """
    Download the cal data using the script created
    """
    # TODO: Initial checks and cleaning
    cal_list = glob("/mnt/scratch/data/cal/pre_facet_prefactor/*.npy")
    if len(cal_list) < 8:
        download = sh.Command("/home/ubuntu/download_data_cal.sh")
        for line in download(_iter=True):
            print(line)
    else:
        print("Skip download_cal_data")
    # TODO: Final checks and notification

def download_data(n_mss=30):
    """
    Download the data
    """
    ms_list = glob("/mnt/scratch/data/raw/L*_SAP???_SB???_uv.MS.dppp")
    if len(ms_list) < n_mss: # TODO: check number
        params = "/home/ubuntu/astrocompute/pipeline/data/{}/target-BAND{}.txt".format(dataset, band)
        download = sh.Command("/home/ubuntu/astrocompute/pipeline/scripts/parallel_download.sh")
        for line in download(params, _iter=True):
            print(line)
    else:
        print("Skip download_data")

def unselect():
    """
    Unselect bad subbands
    """
    from unselect_subbands import unselect_subbands
    unselect_subbands("/mnt/scratch/data/raw/")

def correct_data():
    """
    Correct the data using the check_frequencies script
    """
    correct = sh.Command("/home/ubuntu/astrocompute/pipeline/scripts/correct_data_prefactor.sh")
    for line in correct("/mnt/scratch/data/raw",
                        _iter=True):
        print(line)

def run_pipeline():
    """
    Run the generic pipeline and send notification in case of error
    """
    pipeline = sh.Command("/opt/LofIm/bin/genericpipeline.py")
    for line in pipeline("-c",
                          "/home/ubuntu/astrocompute/pipeline/generic_pipeline/pipeline.cfg",
                          "/home/ubuntu/astrocompute/pipeline/generic_pipeline/pre_facet_prefactor.parset",
                         _iter=True):
        print(line)

def rename():
    """
    Rename bands before upload
    """
    from rename_subtract import rename_directory
    rename_directory("/mnt/scratch/data/process")

def upload_data():
    """
    Upload the computed data
    """
    upload = sh.Command("/home/ubuntu/upload_data_prefactor.sh")
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
    logging.info("Prefactor pipeline started")
    launch(download_cal_data)
    launch(download_data)
    launch(unselect)
    launch(correct_data)
    launch(run_pipeline)
    launch(rename)
    launch(upload_data) 
    #launch(umount_and_remove_disk) # Not implemented yet
    message = "Prefactor pipeline on band {} successfully finished".format(band)
    notify(message, subject=message)
    logging.info("Prefactor pipeline finished; prepared to terminate")
    launch(terminate_instance)
    

