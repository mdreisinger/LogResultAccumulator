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
    print(files)
    if count >= 10:
        [S3.Bucket(BUCKET).upload_file(log_file, log_file) for
         log_file in files]

    [os.remove(log_file) for log_file in files]

if __name__ == "__main__":
    while True:
        upload_files()
        time.sleep(300) # check every 5 minutes
