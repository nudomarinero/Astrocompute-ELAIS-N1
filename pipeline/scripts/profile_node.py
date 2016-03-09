from __future__ import print_function
import psutil
import numpy as np
import time
import socket
import logging

INTERVAL = 60 # in seconds
host = socket.gethostname()
logtofile = True

if logtofile: #log to file
    #THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    #log_path = os.path.abspath(os.path.join(THIS_DIR, '..', 'log'))
    file_name = "profile.log"


def get_data():
   data = np.array([[p.cpu_percent(), 
                     p.memory_info()[0]/1073741824., 
                     p.memory_info()[1]/1073741824., 
                     p.memory_percent()] 
                    for p in psutil.process_iter() if p.username() == "ubuntu"]
                   )
   timestamp = time.time()
   cpu_percent, mem, memvirt, memory_percent = data.sum(axis=0)
   
   return host, timestamp, cpu_percent, mem, memvirt, memory_percent


def run():
    if logtofile:
        f = open(file_name, "wb")
        f.write("node,timestamp,cpu_percent,memory,memory_percent\n")
    try:
        while True:
            #print(get_data())
            print("{0} - {1:f} {2:6.2f} {3:7.3f} {5:6.2f}".format(*get_data()))
            if logtofile:
                f.write("{0},{1:f},{2:6.2f},{3:7.3f},{5:6.2f}\n".format(*get_data()))
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        if logtofile:
            f.close()


if __name__ == '__main__':
    run()
