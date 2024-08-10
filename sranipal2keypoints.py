import argparse
from tqdm import tqdm
from blender_interface import EMBlender
import numpy as np

def read_file(path):
    data = np.loadtxt(path, delimiter=",")
    return data

def main(args):
    filename = args.path
    data = read_file(filename)
    emb = EMBlender()
    # plotter = init_visualizer()
    for lipshape in tqdm(data, leave=False):
        ob = emb.set_key_shapes(lipshape)
        keypoints = emb.get_keypoints(ob)
        lip = emb.get_lip(keypoints)
        emb.set_key_shapes(lipshape)
        # visualize_keypoints(plotter['all'],keypoints)
        # visualize_keypoints(plotter['lip'],lip)
        emb.update_visualizer(lipshape)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='path')
    args = parser.parse_args()

    main(args)