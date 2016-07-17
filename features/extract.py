import sys
import os
import numpy as np
import inception
import pickle

FULLY_CONNECTED_VECTOR_SIZE = 2048
SOFTMAX_VECTOR_SIZE = 1008
INPUT_FOLDER = sys.argv[1] if len(sys.argv) >= 2 else 'images/'
OUTPUT_FOLDER= sys.argv[2] if len(sys.argv) == 3 else 'output/'
PROCESSING_BATCH_SIZE = 10
WRITE_TO_DISK_EVERY_X = 100


def list_files(rootfolder):
    """Find all jpg and jpeg files in the rootfolder, and output
    them as a list of tuples

    input: location of root folder, str
    output: a list of tuples containing (folder, filename)
    """
    folders = next(os.walk(rootfolder))[1]
    out = []
    for folder in folders:
        files = next(os.walk(rootfolder + '/' + folder))[2]
        for file in files:
            if file[-3:] in ['jpg', 'peg']:
                out.append((folder, file))

    return out


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def vectorize_files(rootfolder,
                    files,
                    fully_connected_path='{}/fully_connected.np'.format(OUTPUT_FOLDER),
                    softmax_path='{}/softmax.np'.format(OUTPUT_FOLDER),
                    meta_path='{}/meta.p'.format(OUTPUT_FOLDER)):
    """Create batches of files and run them through inception v3
    input:
        rootfolder: root of all folder and files
        files: list of tuples with (folder, filename)
        fully_connected_path: location of numpy memmap for fully
            connected output
        softmax_path: location of numpy memmap for softmax layer
    output:
        Nothing.
    """

    # Write the metadata to disk using pickle
    pickle.dump(files, open(meta_path, "wb"))

    fully_connected = np.memmap(
        fully_connected_path, dtype='float32', mode='w+',
        shape=(len(files), FULLY_CONNECTED_VECTOR_SIZE))

    softmax = np.memmap(
        softmax_path, dtype='float32', mode='w+',
        shape=(len(files), SOFTMAX_VECTOR_SIZE))

    for i, (folder, file) in enumerate(files):
        print i, folder, file
        path = "%s/%s/%s" % (rootfolder, folder, file)
        fully_connected_layer, softmax_layer = inception.image_to_vector(path)
        fully_connected[i, :] = np.squeeze(fully_connected_layer)
        softmax[i, :] = np.squeeze(softmax_layer)

        if i % WRITE_TO_DISK_EVERY_X == 0:
            print "Saving memmap to disk"
            fully_connected.flush()
            softmax.flush()

    print "Final save to disk"
    fully_connected.flush()
    softmax.flush()
    print "Vectorization completed!"


if __name__ == "__main__":
    files = list_files(INPUT_FOLDER)
    inception.create_graph()
    vectorize_files(INPUT_FOLDER, files)
