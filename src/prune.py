#Recursively traverses the tree and prunes it by evaluating the accuracy
def pruning (tree,root):

    #returns tree if either the tree is Null or both leaf nodes are Null
    if not tree or (not tree["right"] and not tree["left"]):
        return tree
    

    right_copy = tree["right"]
    left_copy = tree["left"]

    left = pruning(tree["left"],root)
    right = pruning(tree["right"],root)

#Hello Indraneel, you're in charge of this now good luck :)  
#put this function inside the tree class so u can pass the decision tree straight into here