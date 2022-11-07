#Recursively traverses the tree and prunes it by evaluating the accuracy
from evaluation import*

def pruning(head, root, test_set):
    """
    Prunes the tree if specific conditions are met 
    :param head a pointer to the root of the tree that stays constant
    :param root a pointer to the current node that moves either left/right based on the recursive call
    :param test_set a test set that is used to evaluate the accuracies

    return pruned tree
    """
  
    # Recurse along with smaller training data until till leafs are found

    # Prune if validation is greater than based on a validation evaluation function 
    # Replace pruned node with majority class label


    #evaluation_du.accuracy_validation(root)

    # Return if node is null
    if(root.node["val"] == None):
        return root

    # Recurse left and right subtrees
    left = pruning(head, root.node["left"], test_set)
    right = pruning(head, root.node["right"], test_set)


    # Reattach the left and right subtrees to the root node
    root.node["left"] = left
    root.node["right"] = right

    # If node is parent of leaf nodes, it can be pruned
    if(root.node["left"].node["left"] == None and root.node["left"].node["right"] == None and root.node["right"].node["left"] == None and root.node["right"].node["right"] == None):
        
        reference_accuracy = evaluate(head,test_set) # Get the accuracy of tree before pruning
        
        # Save left and right subtree and other values
        left_subtree = root.node["left"]
        left_class = root.node["left"].node["attribute"]
        right_subtree = root.node["right"]
        right_class = root.node["right"].node["attribute"]
        curr_val = root.node["val"]

        # Set root and children to null
        root.node["left"] = None
        root.node["right"] = None
        root.node["val"] = None

        #Repace root with left leaf
        root.node["attribute"] = left_class
        left_acc = evaluate(head,test_set)

        #Repace root with right leaf
        root.node["attribute"] = right_class
        right_acc = evaluate(head,test_set)

        # Statements to calculate which accuracy is higher
        if(left_acc >= reference_accuracy):
            if(left_acc > right_acc):
                root.node["attribute"] = left_class
         
        elif(right_acc >= reference_accuracy):
            root.node["attribute"] = right_class

        else:
            root.node["val"] = curr_val
            root.node["left"] = left_subtree
            root.node["right"] = right_subtree


  
    return root


def calculate_depth(tree):
    """
    Calculate the max depth of a tree
    :param tree a pointer to the tree

    return depth of pruned tree
    """
    if(tree.node['val'] == None):
        return 1
    
    left = calculate_depth(tree.node["left"])
    right = calculate_depth(tree.node["right"])

    return 1 + max(left, right)




