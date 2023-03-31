"""
Module to create and upload logs to S3
"""

from multiprocessing import Process

from .log_generator import continuous_files
from .log_uploader import continuous_uploader

if __name__ == "__main__":
    print("running main")
    continuous_files_proc = Process(target=continuous_files)
    continuous_uploader_proc = Process(target=continuous_uploader)

    continuous_files_proc.start()
    continuous_uploader_proc.start()

    continuous_files_proc.join()
    continuous_uploader_proc.join()
    print("finished main")
