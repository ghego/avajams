VIDEO=$1
FOLDER=${2:-"${VIDEO/\.[a-z]*/}"}
mkdir -p $FOLDER
time for i in {0..200} ; do ffmpeg -y -accurate_seek -ss `echo $i*1.0 | bc` -i $VIDEO  -frames:v 1 -vf scale=320:240 $FOLDER/$i.bmp ; done
