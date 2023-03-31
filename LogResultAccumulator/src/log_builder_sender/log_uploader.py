"""
Main module to create logs and send them to the S3 bucket.
"""

import fnmatch
import glob
import os
import pathlib
import time

import boto3


S3 = boto3.resource('s3')
BUCKET = "logresultaccumulator"
CUR_DIR = pathlib.Path(__file__).parent.resolve()

def upload_files():
    """
    Function to upload files in log_files dir once there are 10 files,
    then deletes them from the dir
    """
    #pylint:disable=expression-not-assigned
    dir_path = f"{CUR_DIR}/log_files/"
    count = len(fnmatch.filter(os.listdir(dir_path), '*.*'))
    print('File Count:', count)
    files = glob.glob(f"{CUR_DIR}/log_files/*")
    if count >= 10:
        for log_file_location in files:
            split_up_dirs = log_file_location.split("/")
            log_file = split_up_dirs[-1]
            print(f"Uploading {log_file} to S3")
            S3.Bucket(BUCKET).upload_file(log_file_location, log_file)
            print(f"Removing {log_file}")
            os.remove(log_file_location)

def continuous_uploader():
    """
    Continuously upload files forever
    """
    while True:
        upload_files()
        time.sleep(120) # check every 2 minutes
