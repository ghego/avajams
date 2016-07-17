"""
Loading softmax.np and meta.p data from features.extract

"""

import numpy as np
import pickle
from collections import defaultdict

SOFTMAX_SIZE = 1008
VIDEO_SIZE = 1000
            
def load_meta(file_path):
    meta = pickle.load(open(file_path + 'meta.p', 'r'))
    return meta

def load_softmax(file_path, samples):
    fp = np.memmap(file_path + 'softmax.np', dtype='float32', mode='r', shape=(samples, SOFTMAX_SIZE))
    return fp

def load_from_image(fp, meta, index):
    print('Image: ', meta[index], sum(fp[index,:]))    
    return

def load_from_video(vs, vmeta, index):
    print('Video: ', vmeta[index], sum(vs[index,:]))    
    return

def combine_vectors(vecs):
    return np.sum(vecs, axis=0)/vecs.shape[0]

def video_score_avg(fp, meta):
    video_to_index = defaultdict(list)
    for idx, (video, filename) in enumerate(meta):
        video_to_index[video].append(idx)

    video_meta = video_to_index.keys()
    video_score = np.zeros((len(video_meta), SOFTMAX_SIZE))
    for i, video in enumerate(video_meta):
        combined_vec = combine_vectors(fp[video_to_index[video]])
        video_score[i] = combined_vec

    return video_score, video_meta

# def video_score_avg(fp, meta):
#     video_score = np.zeros((VIDEO_SIZE, SOFTMAX_SIZE))
#     video_meta = []
    
#     image_count = 0
#     video_index = 0
#     video_name = ''
#     score = np.zeros((1, SOFTMAX_SIZE))
    
#     for it in range(len(meta)):
#         file_dir, _ = meta[it]
#         score[0,:] = score[0,:] + fp[it,:]
#         image_count = image_count + 1
        
#         if file_dir != video_name:
#             print score[0,:]
#             video_score[video_index,:] = score[0,:]/image_count
#             video_meta.append(file_dir)
            
#             image_count = 0
#             video_index = video_index + 1
#             video_name = file_dir
                
#     return video_score, video_meta

def main(argv):
        
    file_path = '../features/output/' 
    
    # Loading meta.p and softmax.np
    print('Loading meta.p...')
    meta = load_meta(file_path)
        
    print('Loading softmax.np...')
    fp = load_softmax(file_path, len(meta))
    
    print('Loading sample data') 
    load_from_data(fp, meta, 1200)

    # Compute average video score
    video_score, video_meta = video_score_avg(fp, meta)     
    
if __name__ == '__main__':
    main(sys.argv[1:])