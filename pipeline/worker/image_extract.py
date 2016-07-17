# http://ffmpeg.org/ffmpeg.html#Video-Options
# https://trac.ffmpeg.org/wiki/Scaling%20(resizing)%20with%20ffmpeg
import subprocess
import logging
import re
import os
import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('avajams.image_extract')


NIMAGES = 20
SCALE = 100

def extract_images(video_file_name):
    logger.info("extracting: %s", video_file_name)
    output_path = video_file_name.replace('.mp4', '')
    for i in xrange(1, NIMAGES+1):
        command = """ffmpeg -y -accurate_seek -ss `echo {i}*1.0 | \
                     bc` -i {video} -frames:v 1 -vf "crop=in_h,scale={scale}:-1" \
                     {folder}/{i}.jpg""".format(i=i,
                                                scale=SCALE,
                                                video=video_file_name,
                                                folder=output_path)
        subprocess.call(command, shell=True)

    command = """ffmpeg -y -i {video} -b:a 192K -vn {folder}/audio.mp3""".format(i=i,
                                               video=video_file_name,
                                               folder=output_path)
    subprocess.call(command, shell=True)
    logger.info("done!")

if __name__ == '__main__':
    from sys import argv

    if len(argv) < 2:
        print "Usage: python image_extract.py video_file_name.txt [output_folder_name]"
        exit(0)

    with open(argv[1]) as fin:
        lines = fin.readlines()

    for line in lines:
        extract_images(line)
