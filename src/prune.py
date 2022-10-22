#Recursively traverses the tree and prunes it by evaluating the accuracy
def pruning (tree,root):

    #returns tree if either the tree is Null or both leaf nodes are Null
    if not tree or (not tree["right"] and not tree["left"]):
        return tree
    

    right_copy = tree["right"]
    left_copy = tree["left"]

    left = pruning(tree["left"],root)
    right = pruning(tree["right"],root)

    