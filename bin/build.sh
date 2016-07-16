PROJECT_ROOT="$(cd $(dirname "$(dirname "$BASH_SOURCE")") && pwd)"
echo "Setting project root to: "$PROJECT_ROOT

virtualenv $PROJECT_ROOT/avajams-env

export PROJECT_ROOT
export PYTHONPATH=$PYTHONPATH:$PATH:$PROJECT_ROOT

source $PROJECT_ROOT/avajams-env/bin/activate
pip install -r requirements.txt
