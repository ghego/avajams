import numpy as np
import load_features

meta = [('a', '1.jpg'), ('a', '2.jpg'), ('b', '3.jpg'), ('b', '4.jpg')]

fp = np.zeros((4, 1008))
fp[0, 0] = 1
fp[1, 0] = 1
fp[2, 0] = 1
fp[3, 0] = 3

video_score, video_meta = load_features.score_videos(fp, meta)

assert video_score[0, 0] == 1, 'first one wrong'
assert video_score[1, 0] == 2, 'second one wrong'
