# Extracted from https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/image/imagenet/classify_image.py
#
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os.path
import inspect
import tensorflow as tf


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    current_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    with tf.gfile.FastGFile(current_folder + '/classify_image_graph_def.pb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def image_to_vector(image):
    """Runs inference on an image.
    Make sure to run create_graph before calling this function!

    Args:
    image: Image file name.

    Returns:
    1D numpy vector representing image
    """
    image_data = tf.gfile.FastGFile(image, 'rb').read()

    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        fully_connected_layer = sess.graph.get_tensor_by_name('pool_3:0')
        softmax_layer = sess.graph.get_tensor_by_name('softmax:0')
        return sess.run(
            [fully_connected_layer, softmax_layer],
            {'DecodeJpeg/contents:0': image_data})


if __name__ == "__main__":
    create_graph()
    import numpy as np
    outvec = np.squeeze(image_to_vector('/Users/sep/Downloads/sombrero.jpeg'))
    print outvec
    # top_indexes = outvec.argsort()[-5:]
    # print outvec[top_indexes]
