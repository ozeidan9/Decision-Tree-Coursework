import numpy as np

class Evaluation:
    def __init__(self,data):
        self.root = None
        self.data = data
        self.test_set ={}
        self.training_set = {}

        #for metrics
        self.rooms_actual = {1:0,2:0,3:0,4:0}
        self.true_positives = {1:0,2:0,3:0,4:0}
        self.false_positives = {1:0,2:0,3:0,4:0}
        self.precision = {1:0,2:0,3:0,4:0}
        self.recall = {1:0,2:0,3:0,4:0}
        self.f1 ={1:0,2:0,3:0,4:0}

    def get_metrics(self):
        for room in range(1,5):
            self.precision[room] = self.true_positives[room]/(self.true_positives[room]+self.false_positives[room])
            self.recall[room] = self.true_positives[room]/self.rooms_actual[room]
            self.f1[room] = (2*self.precision[room]*self.recall[room])/(self.precision[room]+self.recall[room])
        
    def randomise(self): #randomises the input data
        np.random.shuffle(self.data)

    def cross_val(self,k=10): #k-fold cross validation

        split = len(self.data)//k
        for i in range(k): #splits data into training:testing
            self.test_set[i] = self.data[i*split:(i*split)+split]
            self.training_set[i] = np.delete(self.data,slice(i*split,(i*split)+split),axis = 0)

    def evaluate(self,test_set_index=0):
        correct = 0
        total = 0
        for row in self.test_set[test_set_index]: #loops through each test case
            total+=1
            self.rooms_actual[row[-1]]+=1 # for metrics
            prediction = self.eval_tree(self.root,row)
            if prediction == row[-1]:
                correct+=1
                self.true_positives[prediction]+=1
            else:
                self.false_positives[prediction]+=1
        return (correct/total)            


    def eval_tree(self, root, input):
        """ DFS traversal through decision tree and prins leaf nodes

        Input: root node (type: tree)
        return an integer
        """
        # leaf node
        if not root.node['left'] and not root.node['right']: 
            return root.node['attribute']
        
        attr = root.node['attribute']
        if input[attr] <= root.node['val']:
            return self.eval_tree(root.node['left'], input)
        else:    
            return self.eval_tree(root.node['right'], input)    

if __name__ == "__main__":
    clean_data = np.loadtxt("test/sample_set.txt", dtype=float)
    Evaluation(clean_data)