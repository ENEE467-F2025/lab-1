from spatialmath import *
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import yaml

# constants
UP: int = -1
DOWN: int = 1

class TFTree:
    """A class for computing relative transformation matrices
    given a transfer frame tree.

    ...
    """

    def __init__(self):
        """Initialize a TFTree object.

        """

        self.tf_tree: dict = {}
    
    @classmethod
    def load_from_yaml(cls: "TFTree", path: str) -> "TFTree":
        """Load a TF tree from a YAML file.

        Args:
            path (str): relative path of the YAML file
        
        Returns:
            A TFTree object.
        """

        with open(path) as file:
            try:
                tree: dict = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        
        root = False
        for branch in tree.values():
            if "children" not in branch:
                # is this necessary?
                branch["children"] = []
            
            # root, can only be one!
            if "parent" not in branch:
                if root:
                    raise Exception("There can only be one root per tree!")
                branch["parent"] = None
                root = True
            
            # compute the frame given xyzrpy
            T = SE3.Trans(branch["xyzrpy"][:3])*SE3.RPY(branch["xyzrpy"][3:])
            branch["frame"] = T
        
        rtn = cls()
        rtn.tf_tree = tree

        return rtn
    
    @property
    def root(self) -> str:
        """Get the root frame.

        Returns:
            the name of the root frame (str).

        """

        for frame_name, branch in self.tf_tree.items():
            if branch["parent"] is None:
                return frame_name
        else:
            raise Exception("No parent frame found in the tree!")
    
    def _get_path_to_root(self, node: str, dir: int=DOWN) -> list:
        """Get a directed path to the root node from node.

        Args:
            node (str): the name of the source node.
            dir (int): the direction of tree traversal (UP = -1, DOWN = 1)
        
        Returns:
            A directed path from node to root
        
        Note:
            The dir arguement is intended for use when computing the
            relative transformation. I.e. when computing the path
            from the source node, dir = UP = -1. Whe computing the
            path from the target node, dir = DOWN = 1.

            Why this is the case is because the up path inverts the
            transformations between nodes, hence T^(-1) whereas the
            down path does not invert the transformations, hence T^(1).
        """

        assert node in self.tf_tree

        if self.tf_tree[node]["parent"] == None:
            return [(node, dir)]
        return [(node, dir)] + self._get_path_to_root(self.tf_tree[node]["parent"], dir=dir)
    
    def get_transform(self, source: str, target: str) -> SE3:
        """Return the relative transformation matrix from
        source to target.

        """

        assert source in self.tf_tree and target in self.tf_tree

        # TODO: Complete this method
        up_path = self._get_path_to_root(source, dir=UP)
        down_path = self._get_path_to_root(target, dir=DOWN)

        # find shortest path by pruning common nodes
        # 
        # then compute the relative transformation
        #
        # T_rel = SE3()
        # for node in shortest_directed_path:
        #     dir = node[1]
        #     frame_name = node[0]
        #     T = self.tf_tree[frame_name]["frame"]
        #
        #     if dir = UP:
        #         T_rel = T_rel * T.inv()
        #     elif dir = DOWN
        #         T_rel = T_rel * T
        #
        # return T_rel

# end TFTree


def main():
    
    tf = TFTree.load_from_yaml("tree.yaml")
    
    SE3().plot(frame="0", color="black")
    T = tf.get_transform("world", "robotiq_hande_end")
    print(T)
    T.plot(frame="1")
    
    plt.show()

if __name__ == "__main__":
    main()