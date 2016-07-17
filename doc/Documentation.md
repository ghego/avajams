# Documentation

## Project Goal
Find the best matching video clip from a video clip or an image.

## Methodology

* Extract an image for every second of the video.  The extracted image is in JPG format with a size of 100 x 100.
* Use TensorFlow's Inception to associate the images with 1,000 classifications
* Find the best matching video clip of these images based on cosine similiary matrix
* Bonus Task: Mash-up the matched music with the user provided clip

## Technology Stack

* TensorFlow / Image Recognition
* Dockers
* Python
* Video and Audio editing tools


## Future Improvements
* Train on more videos, at least 10,000 videos to train
* Customize TensorFlow's Inception with new classes
* Better business use cases e.g. better recommender
* Sentiment Analysis based on video/ image color to better match the mood of music a.k.a. style transfer music

## Video and Music Data Sources
* http://fmusictv.com
* http://www.youtube.com


## References

* Inception
https://github.com/tensorflow/models/tree/master/inception

* How to Classify Images with TensorFlow
https://research.googleblog.com/2015/12/how-to-classify-images-with-tensorflow.html

* Initial project: Magenta
https://github.com/tensorflow/magenta

