import numpy as np


def cross_val(data,k=10): #k-fold cross validation
    test_set = {1: 0, 2:0, 3:0, 4:0}
    training_set = {1: 0, 2:0, 3:0, 4:0}
    split = len(data)//k
    for i in range(k): #splits data into training:testing
        test_set[i] = data[i*split:(i*split)+split]
        training_set[i] = np.delete(data,slice(i*split,(i*split)+split),axis = 0)
    return test_set,training_set

def evaluate(root,test_set,is_pruning = 1):

    rooms_actual = {1:0,2:0,3:0,4:0}
    true_positives = {1:0,2:0,3:0,4:0}
    false_positives = {1:0,2:0,3:0,4:0}


    correct = 0
    total = 0

    for row in test_set:#[test_set_index]: #loops through each test case
        total+=1
        rooms_actual[row[-1]]+=1 # for confusion matrix
        prediction = eval_tree(root,row)
        if prediction == row[-1]:
            correct+=1
            true_positives[prediction]+=1
        else:
            false_positives[prediction]+=1
    print()
    accuracy = correct/total
    if is_pruning ==1:
        return accuracy #just returns accuracy if this function is used by pruning
    else:
        return accuracy,rooms_actual,true_positives,false_positives          
    

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

def get_metrics(rooms_actual,true_positives,false_positives):
    precision = {1:0,2:0,3:0,4:0}
    recall = {1:0,2:0,3:0,4:0}
    f1 ={1:0,2:0,3:0,4:0}
    for room in range(1,5):
        precision[room] = true_positives[room]/(true_positives[room]+false_positives[room])
        recall[room] = true_positives[room]/rooms_actual[room]
        f1[room] = (2*precision[room]*recall[room])/(precision[room]+recall[room])

    return ((precision,recall,f1))  
