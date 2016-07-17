PROJECT_ROOT="$(cd $(dirname "$(dirname "$BASH_SOURCE")") && pwd)"
echo "Setting project root to: "$PROJECT_ROOT

virtualenv $PROJECT_ROOT/avajams-env

export PROJECT_ROOT
export PYTHONPATH=$PYTHONPATH:$PATH:$PROJECT_ROOT

source $PROJECT_ROOT/avajams-env/bin/activate
pip install -r requirements.txt
pip install https://storage.googleapis.com/tensorflow/mac/tensorflow-0.9.0-py2-none-any.whl

bower update

curl http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz | tar zx


mv classify_image_graph_def.pb features/classify_image_graph_def.pb