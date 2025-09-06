tree = {
    "root_node": {
        "parent": None,
        "children": ["node_a", "node_b"]
    },
    "node_a": {
        "parent": "root_node",
        "children": []
    },
    "node_b": {
        "parent": "root_node",
        "children": ["node_c"]
    },
    "node_c": {
        "parent": "node_b",
        "children": []
    }
}

source = "node_a"
target = "node_c"

def get_path_to_root(tree, node: str) -> list[str]:
    # make sure the node is a key in the tree
    assert node in tree

    if tree[node]["parent"] == None:
        return [node]
    return [node] + get_path_to_root(tree, tree[node]["parent"])

source_path = get_path_to_root(tree, source)
target_path = get_path_to_root(tree, target)

while (
        len(source_path) > 0 and 
        len(target_path) > 0 and
        source_path[-1] == target_path[-1]
    ):  
    common_node = source_path.pop()
    target_path.pop()

target_path.reverse()
path = source_path + target_path

print(path)