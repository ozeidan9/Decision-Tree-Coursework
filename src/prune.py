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

    if(root['val'] == None):
        return 0

    left = pruning(head, root["left"], depth)
    right = pruning(head, root["right"], depth)

    is_pruned = False;

    if(root["left"]["left"] == None and root["left"]["right"] == None and root["right"]["left"] == None and root["right"]["right"] == None ):
        
        reference_accuracy = Evaluation(head)
        
        left_subtree = dict(root["left"])
        left_class = root["left"]["attribute"]
        right_subtree = dict(root["right"])
        right_class = root["right"]["attribute"]
        curr_val = root["val"]

        root["left"] = None
        root["right"] = None
        root["val"] = None

        #Repace with left
        root["attribute"] = left_class
        left_acc = Evaluation(head)

        #Repace with right
        root["attribute"] = right_class
        right_acc = Evaluation(head)

        if(left_acc >= reference_accuracy):
            if(left_acc > right_acc):
                is_pruned = True
                root["attribute"] = left_class
         
        elif(right_acc >= reference_accuracy):
            is_pruned = True
            root["attribute"] = right_class

        else:
            root["val"] = curr_val
            root["left"] = left_subtree
            root["right"] = right_subtree


    if(is_pruned):
        return 1

    return 1 + max(left, right)
    






