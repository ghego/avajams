#!/bin/bash

PROJECT_ROOT="$(cd $(dirname "$(dirname "$BASH_SOURCE")") && pwd)"

echo "Setting project root to: "$PROJECT_ROOT

export PROJECT_ROOT
export PYTHONPATH=$PYTHONPATH:$PATH:$PROJECT_ROOT
source $PROJECT_ROOT/avajams-env/bin/activate

echo "Make sure you place the file classify_image_graph_def.pb in the 'features' folder."
echo "Take it from the tar file here: http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz"
