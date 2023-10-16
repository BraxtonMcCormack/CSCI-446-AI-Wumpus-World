#! /bin/bash
import numpy as np
import sys

def main(cave:str) -> None:
    """
    A function to flip a cave along the horizonal axis. Running this function will
    either reverse the order of the y-axis of the images produced by print-cave.py.
    This function destroys the previous file, so  consider noting the layout before
    running to ensure you know if you have a flipped or unflipped file.
    :param cave: Name of the .cave file to flip.
    """
    print(f"flipping {cave}.")
    ttarget = np.flip([line for line in open(cave, "r")])
    ttarget = np.delete(np.insert(ttarget, 0, ttarget[-1], axis=0), -1)
    target = open(cave, "w")
    for line in ttarget:
        target.write(line)
    target.close()

if __name__ == "__main__":
    main(sys.argv[1])