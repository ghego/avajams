"""
Find the most similar image or video from learned features

"""

import numpy as np
from scipy import spatial

def nearest_image(fp, meta, test_softmax):
    min_dist = 1 
    index = 0
    
    for it in range(len(meta)):
        dist = spatial.distance.cosine(fp[it,:], test_softmax)
        if dist < min_dist:
            min_dist = dist
            index = it
    
    return meta[index]

def nearest_video(video_score, video_meta, test_softmax):
    min_dist = 1 
    index = 0
    
    for it in range(len(video_meta)):
        dist = spatial.distance.cosine(video_score[it,:], test_softmax)
        if dist < min_dist:
            min_dist = dist
            index = it
    
    return video_meta[index]

def nearest(fp, meta, video_score, video_meta, test_vec):
    image_match = nearest_image(fp, meta, test_vec)
    video_match = nearest_video(video_score, video_meta, test_vec)
    return image_match, video_match

def main(argv):
    print('\n')
          
if __name__ == '__main__':
    main(sys.argv[1:])