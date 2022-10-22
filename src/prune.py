#pruning the decision tree that's passed into the function
def pruning (tree, node, test_data):
    if not tree or (not tree['right'] and not tree['left']):
        return tree
    

    
    