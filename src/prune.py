#Recursively traverses the tree and prunes it by evaluating the accuracy


def pruning(head, root, depth):
    """
    return depth
    """
    # Split the dataset according the tree attributes and values
    # Classify the majority element in such a dataset split

    # Recurse along with smaller training data until till leafs are found

    # Prune if validation is greater than based on a validation evaluation function 
    # Replace pruned node with majority class label


    #evaluation_du.accuracy_validation(root)

    if(root.node['val'] == None):
        return (root, 0)

    left, ldepth = pruning(head, root.node["left"], depth)
    right, rdepth = pruning(head, root.node["right"], depth)

    root.node["left"] = left
    root.node["right"] = right

    is_pruned = False;


    if(root.node["left"]["left"] == None and root.node["left"]["right"] == None and root.node["right"]["left"] == None and root.node["right"]["right"] == None):
        
        reference_accuracy = Evaluation(head)
        
        left_subtree = dict(root.node["left"])
        left_class = root.node["left"]["attribute"]
        right_subtree = dict(root.node["right"])
        right_class = root.node["right"]["attribute"]
        curr_val = root.node["val"]

        root.node["left"] = None
        root.node["right"] = None
        root.node["val"] = None

        #Repace with left
        root.node["attribute"] = left_class
        left_acc = Evaluation(head)

        #Repace with right
        root.node["attribute"] = right_class
        right_acc = Evaluation(head)

        if(left_acc >= reference_accuracy):
            if(left_acc > right_acc):
                is_pruned = True
                root.node["attribute"] = left_class
         
        elif(right_acc >= reference_accuracy):
            is_pruned = True
            root.node["attribute"] = right_class

        else:
            root.node["val"] = curr_val
            root.node["left"] = left_subtree
            root.node["right"] = right_subtree


    if(is_pruned):
        return (root, 0)


    return (root, 1 + max(ldepth, rdepth))
    






