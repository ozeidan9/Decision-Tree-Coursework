#Recursively traverses the tree and prunes it by evaluating the accuracy
from evaluation import*

def pruning(head, root, depth,test_set):
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

    left, ldepth = pruning(head, root.node["left"], depth,test_set)
    right, rdepth = pruning(head, root.node["right"], depth,test_set)

    root.node["left"] = left
    root.node["right"] = right

    is_pruned = False;


    if(root.node["left"].node["left"] == None and root.node["left"].node["right"] == None and root.node["right"].node["left"] == None and root.node["right"].node["right"] == None):
        
        reference_accuracy = evaluate(head,test_set)
        
        left_subtree = root.node["left"]
        left_class = root.node["left"].node["attribute"]
        right_subtree = root.node["right"]
        right_class = root.node["right"].node["attribute"]
        curr_val = root.node["val"]

        root.node["left"] = None
        root.node["right"] = None
        root.node["val"] = None

        #Repace with left
        root.node["attribute"] = left_class
        left_acc = evaluate(head,test_set)

        #Repace with right
        root.node["attribute"] = right_class
        right_acc = evaluate(head,test_set)

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
    






