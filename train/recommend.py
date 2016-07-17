"""
Recommend most similar image or video from repository
"""

import sys
import numpy as np
import pickle
import load_features
import similarity
import os
# sys.path.insert(0, '../features')
# import inception as ts
from features import inception as ts
            
def main(argv):

    print os.environ['PROJECT_ROOT']
    file_path = os.path.join(os.environ['PROJECT_ROOT'],'features/output/' )
    
    """
    Loading meta.p and softmax.np
    """
    print('Loading meta.p...')
    meta = load_features.load_meta(file_path)
        
    print('Loading softmax.np...')
    fp = load_features.load_softmax(file_path, len(meta))
    
    print('Averaging video scores...')
    video_score, video_meta = load_features.video_score_avg(fp, meta)     

    #Debug: load_features
    print('Loading sample data') 
    load_features.load_from_image(fp, meta, 1200)
    load_features.load_from_video(video_score, video_meta, 2)
    print('\n')
    
    """
    Data Valiation
    """
    image_match = -1
    video_match = []

    if argv:
        path = argv
        print('Comparing to image...', path)
        
        # Perform inception classification on input image
        ts.create_graph()
        skip, img_vec = ts.image_to_vector(path)
        
        image_match, video_match = similarity.nearest(fp, meta, video_score, video_meta, img_vec)
        print('nearest_image_match', image_match)
        print('nearest_video_match', video_match)   
        return image_match, video_match
    
    else:
        test_idx = 900;
        print('Comparing to default test image:', meta[test_idx])

        image_match, video_match = similarity.nearest(fp, meta, video_score, video_meta, fp[test_idx,:])
        print('nearest_image_match', image_match)
        print('nearest_video_match', video_match)
        
    print('\n')
        
if __name__ == '__main__':
    main(sys.argv[1:])