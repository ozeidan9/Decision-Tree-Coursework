import numpy as np
# self.rooms_actual = {1:0,2:0,3:0,4:0}
# self.rooms_predicted = {1:0,2:0,3:0,4:0}
# self.root = None
# self.data = data
# self.test_set ={}
# self.training_set = {}


def cross_val(data,k=10): #k-fold cross validation
    test_set = {1: 0, 2:0, 3:0, 4:0}
    training_set = {1: 0, 2:0, 3:0, 4:0}
    split = len(data)//k
    for i in range(k): #splits data into training:testing
        test_set[i] = data[i*split:(i*split)+split]
        training_set[i] = np.delete(data,slice(i*split,(i*split)+split),axis = 0)
    return test_set,training_set

def evaluate(root,test_set,test_set_index=0):
    correct = 0
    total = 0
    rooms_actual, rooms_predicted = {1: 0, 2:0, 3:0, 4:0}, {1: 0, 2:0, 3:0, 4:0}

    for row in test_set[test_set_index]: #loops through each test case
        total+=1
        rooms_actual[row[-1]]+=1 # for confusion matrix
        prediction = eval_tree(root,row)
        rooms_predicted[prediction]+=1
        if prediction == row[-1]:
            correct+=1
    return (correct/total)            
    

def eval_tree(root, input):
    """ DFS traversal through decision tree and prins leaf nodes

    Input: root node (type: tree)
    return an integer
    """
    
    if not root.node['left'] and not root.node['right']: 
        return root.node['attribute']
    
    attr = root.node['attribute']
    if input[attr] <= root.node['val']:
        return eval_tree(root.node['left'], input)
    else:    
        return eval_tree(root.node['right'], input)    
