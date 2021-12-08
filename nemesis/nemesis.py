#!/bin/python
import time
import datetime
import os
import glob
from sql_driver import Nemesis_Db

nemesis_db = Nemesis_Db()

def process_line(line, map):
    words = line.split("\"")
    if "killed" in line:
        row =  ( datetime.date.today().strftime(f"%Y-%m-%d"), 
                 words[1].strip().split("<")[2].strip(">"),
                 words[3].strip().split("<")[2].strip(">"),
                 map,
                 1)
        nemesis_db.add(row)
         

def get_latest_file(folder):
    list_of_files = glob.glob(folder + "/*.log") 
    return max(list_of_files, key=os.path.getmtime) 

def follow(folder):
    '''generator function that yields new lines in a file
    '''
    latest_file = get_latest_file(folder)
    thefile = open(latest_file)
    # seek the end of the file
    #thefile.seek(0, os.SEEK_END)
    print(latest_file) 
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            if latest_file != get_latest_file(folder):
                thefile.close()
                latest_file = get_latest_file(folder) 
                thefile = open(latest_file)
            continue

        yield line

if __name__ == '__main__':
    pause_flag = True
    map = "" 
    loglines = follow("/serverlogs")
    # iterate over the generator
    for line in loglines:
        if "*** [NEMESIS START] ***" in line:
            pause_flag = False
            
        elif "*** [NEMESIS STOP] ***" in line: 
            pause_flag = True
        elif "Loading map" in line:
            map = line.split("\"")[1].strip("\"")

        elif not pause_flag:
            process_line(line,map)