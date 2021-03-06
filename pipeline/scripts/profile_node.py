from __future__ import print_function
import psutil
import os
import numpy as np
import time
import socket
import logging

INTERVAL = 60 # in seconds
disk = "/mnt"
username = "ubuntu"
host = socket.gethostname()
logtofile = True

if logtofile: #log to file
    #THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    #log_path = os.path.abspath(os.path.join(THIS_DIR, '..', 'log'))
    file_name = "profile.log"


def get_user_pdata(user="ubuntu"):
    """
    Get robustly the data
    """
    while True:
        try:
            data = np.array([[p.cpu_percent(), 
                              p.memory_info()[0]/1073741824., 
                              p.memory_info()[1]/1073741824., 
                              p.memory_percent()] 
                             for p in psutil.process_iter() if p.username() == user]
                            )
        except psutil.NoSuchProcess:
            pass
        else:
            break
    return data

def get_data(user="ubuntu"):
    statvfs = os.statvfs(disk)
    disk_total = statvfs.f_frsize * statvfs.f_blocks
    disk_avail = statvfs.f_frsize * statvfs.f_bavail
    
    data = get_user_pdata(user=user)
            
    timestamp = time.time()
    cpu_percent, mem, memvirt, memory_percent = data.sum(axis=0)
   
    return (host, 
            timestamp, 
            cpu_percent, 
            mem, 
            memvirt, 
            memory_percent, 
            disk_total/1073741824.,
            (disk_total-disk_avail)/1073741824.,
            (disk_total-disk_avail)/float(disk_total)*100.
            )
                      

def run():
    if logtofile:
        f = open(file_name, "wb")
        f.write("node,timestamp,cpu_percent,memory,memory_percent,disk,disk_percent\n")
    try:
        while True:
            #print(get_data())
            print("{0} - {1:f} {2:6.2f} {3:7.3f} {5:6.2f} {7:7.3f} {8:6.2f}".format(*get_data(user=username)))
            if logtofile:
                f.write("{0},{1:f},{2:6.2f},{3:7.3f},{5:6.2f},{7:7.3f},{8:6.2f}\n".format(*get_data(user=username)))
                f.flush()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        if logtofile:
            f.close()


if __name__ == '__main__':
    run()
