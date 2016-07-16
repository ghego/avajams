import subprocess
import logging
import re

logger = logging.getLogger('avajams.image_extract')


def extract_images(video_file_name):
    logger.info("extracting: %s", video_file_name)
    subprocess.call("./image_extract.sh ./%s" % video_file_name, shell = True)
    logger.info("done!")

if __name__ == '__main__':
    from sys import argv

    if len(argv) < 2:
        print "Usage: python image_extract.py video_file_name [output_folder_name]"
    else:
        extract_images(argv[1])
    print argv
    
