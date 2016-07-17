# Documentation

## Project Goal
Find the best matching music for a video clip.

## Methodology

* Extract an image for every second of the video.  The extracted image is in JPG format with a size of 100 x 100.
* Use TensorFlow's Inception to associate the images with 1,000 classifications
* Find the best matching music of these images based on similiary matrix



## Future Improvements
Need to get 10,000 videos to train 


## Video and Music Data Sources
http://www.eecs.qmul.ac.uk/mmv/datasets/deap/readme.html#vid_list
http://fmusictv.com
http://www.youtube.com


## References

Inception
https://github.com/tensorflow/models/tree/master/inception

How to Classify Images with TensorFlow
https://research.googleblog.com/2015/12/how-to-classify-images-with-tensorflow.html

https://github.com/tensorflow/magenta

