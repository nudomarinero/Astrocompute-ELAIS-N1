"""
Monitors the state of the machine
"""
from __future__ import print_function
import os
import time
import boto.utils
import boto.ec2
import boto.sns
import logging
import traceback
import ConfigParser
import psutil
from get_band import get_tag

#logging.basicConfig(
    #filename="pipeline.log", 
    #level=logging.DEBUG)
    ## Logger configuration
if os.path.exists("/home/ubuntu/logging_monitor.conf"):
    logging.config.fileConfig('/home/ubuntu/logging_monitor.conf')
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
    file_name = "/home/ubuntu/monitor.log"
    fh = logging.FileHandler(file_name) 
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    #logging.info('\n')

# General configuration
INTERVAL = 30 # in seconds
disk = "/mnt"
config = ConfigParser.ConfigParser()
config.read('/home/ubuntu/.sns_conf')
topicarn = config.get("arn", "topicarn")

# General information
region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
iid = boto.utils.get_instance_metadata()['instance-id']
band = get_tag("band")
dataset = get_tag("dataset")
pipeline_type = get_tag("type")

## Auxiliary functions
def notify(message, subject=None):
    """
    Notify the user using SNS
    """
    snsc = boto.sns.connect_to_region(region)
    if subject is None:
        subject = "Notification LOFAR AWS" 
    publication = snsc.publish(topicarn, message, subject=subject)

## Monitor tasks
def check_spot_code():
    """
    Retrieve the status code of the spot instance
    WARNING It only works in spot instances
    """
    conn = boto.ec2.connect_to_region(region)

    instances = conn.get_all_spot_instance_requests()
    for instance in instances:
        if instance.instance_id == iid:
            return instance.status.code

def check_disk_usage(disk):
    """
    Check the fraction of the disk used
    """
    statvfs = os.statvfs(disk)
    disk_total = statvfs.f_frsize * statvfs.f_blocks
    disk_avail = statvfs.f_frsize * statvfs.f_bavail
    return (disk_total-disk_avail)/float(disk_total)
    
def check_factor_running():
    """
    Check if factor is running
    """
    program_dict = {"prefactor":"genericpipeline.py",
                    "factor":"runfactor"}
    pipeline_program = program_dict.get(pipeline_type, "runfactor")
    while True:
        try:
            check = any([pipeline_program in psutil.Process(pid).name() for pid in psutil.pids()])
        except psutil.NoSuchProcess:
            pass
        else:
            break
        
    return check
    
# Notifications
def notify_spot_shutdown(code):
    """
    Notify if the instance is going to shut down
    """
    logging.warning("Instance shutdown issued.")
    message = ("Spot instance shutdown\n"+
        "Dataset: {}\n".format(dataset)+
        "Data id: {}\n".format(band)+
        "Inst id: {}\n".format(iid))
    subject = "Spot instance shutdown"
    notify(message, subject=subject)

def notify_disk_90(fraction):
    """
    Notify if the instance is going to shut down
    """
    logging.warning("Disk almost full. Fraction: {:6.4f}".format(fraction))
    message = ("Disk almost full\n"+
        "Dataset: {}\n".format(dataset)+
        "Data id: {}\n".format(band)+
        "Inst id: {}\n".format(iid))
    subject = "Disk almost full"
    notify(message, subject=subject)

def notify_factor_stoped():
    """
    Notify factor has stoped
    """
    logging.warning("Pipeline stoped")
    message = ("Pipeline stoped\n"+
        "Dataset: {}\n".format(dataset)+
        "Data id: {}\n".format(band)+
        "Type id: {}\n".format(pipeline_type)+
        "Inst id: {}\n".format(iid))
    subject = "Pipeline stoped"
    notify(message, subject=subject)
    init_factor = False

if __name__ == "__main__":
    logging.info("Monitoring started")
    init_factor = False
    notified_disk = False
    pipeline_name = "generic_pipeline"
    try:
        while True:
            # Check spot instance stoping
            code = check_spot_code()
            if code == u"marked-for-termination":
                notify_spot_shutdown(code)
            # Check disk becoming full
            fraction = check_disk_usage(disk)
            if fraction >= 0.9 and not notified_disk:
                notify_disk_90(fraction)
                notified_disk = True
            if fraction < 0.9 and notified_disk: # If space is freed
                notified_disk = False
            # Check factor running
            check = check_factor_running()
            if init_factor and not check:
                notify_factor_stoped()
                init_factor = False
            if (not init_factor) and check:
                init_factor = True
            logging.info("Instance code: {}; Disk usage: {:6.4f}; Pipeline running: {}".format(code, fraction, check))
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        logging.shutdown()
