import numpy as np
import matplotlib as plt
import matplotlib.axes as ax
from collections import deque

class tree:
    def __init__(self, attribute, val=None, left=None, right=None):
        # Creates leaf node by default
        self.node = {'attribute': attribute, 'val': val, 'left': left, 'right': right} 
          
    def printTree(self, node=None, depth=0):
        if node is None:
            node = self.node
        if node['val'] is not None:
            self.printTree(node['left'].node, depth + 1)
            print(' ' * 4 * depth + '-> x' + str(node['attribute']) + ' <= ' + str(node['val']))
            self.printTree(node['right'].node, depth + 1)
        else:
            print(' ' * 4 * depth + '-> x' + str(node['attribute']))
        if depth == 0:
            print("up means true, down means false")

class tree_gen:
    def __init__(self, depth=0) -> None:
        clean_filepath = "test/clean_dataset.txt"
        noisy_filepath = "test/noisy_dataset.txt"
        sample_filepath = "test/sample_set.txt"
        
        self.clean_data = np.loadtxt(clean_filepath, dtype=float)
        self.noisy_data = np.loadtxt(noisy_filepath, dtype=float)
        self.sample_data = np.loadtxt(sample_filepath, dtype=float)
        self.depth = depth

    def generateTree(self, training_dataset, depth):
        # Current issue: tree keeps going, depth has reached 700 before.
        """
        Generate a decision tree from the given data
        :param training_dataset: 2000x8 matrix of training data
        :param depth: used to compute maximal depth of tree - for plotting purposes
        :return: decision tree
        """
        # if all samples have same label, return a leaf node with this value and depth
        # ie if all the remaining samples are of the same sample (your dataset correspondes to only one room)
        if len(np.unique(training_dataset[:, -1])) <= 1:
            print("tree finished")
            attribute = np.unique(training_dataset[:, -1])
            leaf_node = tree(attribute=int(attribute))
            return (leaf_node, depth)
        
        # else, find the best split and return a node with the best split and depth
        else:
            topSet, bottomSet, splitAttrib, value = self.splitSet(training_dataset)
            leftBranch, leftDepth = self.generateTree(topSet, depth+1)
            rightBranch, rightDepth = self.generateTree(bottomSet, depth+1)
            node = tree(attribute=splitAttrib, val=value, left=leftBranch, right=rightBranch)
            return (node, max(leftDepth, rightDepth))
    
    #def splitSet(self, trainingSet, value, attribute):
    #    return trainingSet[np.where(trainingSet[:, attribute+1] <= value)], trainingSet[p.where(trainingSet[:, attribute+1] > value)]
            
    def splitSet(self, trainingSet):
        """
        Find the best split for the given data
        :param training_dataset: 2000x8 matrix of training data
        :return: best split - row and column
        """
        bestSplit = (None, None, 0, 0)
        bestEntropy = np.inf
        #Calculate the maximum entropy for splitting 
        for row in range(trainingSet.shape[0]):
            #Calculate entropy for every column, but ignore last column
            for column in range(trainingSet.shape[1]-1):
                #Split array into top and bottom, and add entropies
                #topEntropy = self.compute_entropy(training_dataset[0:row, column])
                #bottomEntropy = self.compute_entropy(training_dataset[row:training_dataset.shape[0], column])
                value = trainingSet[row, column]
                topSet = trainingSet[np.where(trainingSet[:, column] <= value)]
                bottomSet = trainingSet[np.where(trainingSet[:, column] > value)]
                topEntropy = self.compute_entropy(topSet)
                bottomEntropy = self.compute_entropy(bottomSet)
                totalEntropy = bottomEntropy + topEntropy 
                #print(totalEntropy)
                if totalEntropy < bestEntropy:
                    bestEntropy = totalEntropy
                    bestSplit = (topSet, bottomSet, column, value)
        #print("BE:", best_entropy)
        return bestSplit
    
    def compute_entropy(self, training_dataset):
        """
        Calculate the best splitpoint in the given column
        """
        entropy = 0
        #Need elements as a histogram
        elements, count = np.unique(training_dataset, return_counts=True)
        for i in range(len(elements)):
            elementProb = count[i]/sum(count)
            entropy -= elementProb * np.log2(elementProb)
        return entropy * training_dataset.size
    
def visualize_tree(root, xmin, xmax, ymin, ymax) -> None:
    """
    Visualize the given decision tree using breadth first search to perfrom a level order traversal
    :param tree: decision tree
    :return: None
    """
    queue = deque([(root, xmin, xmax, ymin, ymax)])
    while len(queue) > 0:
        e = queue.popleft()
        node = e[0]
        xmin = e[1]
        xmax = e[2]
        ymin = e[3]
        ymax = e[4]
        node = root.node
        atri = node['attribute']
        val = node['val']
        text = '['+str(atri)+']:'+str(val)
        #---------------------
        center = xmin+(xmax-xmin)/2.0
        d = (center-xmin)/2.0
        
        if node['left'] != None and node['right'] != None:
            an1 = ax.Axes.annotate(0, xy=(center, ymax), xycoords="data",
            va="bottom", ha="center",
            bbox=dict(boxstyle="round", fc="w"))
            
        elif node['left'] != None:
            queue.append((node['left'], xmin, center, ymin, ymax-gap))
            ax.Axes.annotate(text, xy=(center-d, ymax-gap), xytext=(center, ymax),
                        arrowprops=dict(facecolor='grey', shrink=10),
                        )
            
        elif node['right'] != None:
            queue.append((node['right'], center, xmax, ymin, ymax-gap))
            ax.Axes.annotate(text, xy=(center+d, ymax-gap), xytext=(center, ymax),
                        arrowprops=dict(facecolor='grey', shrink=10),
                        )            
        else:
            continue

# if __name__ == "__main__":
#     treeNode = tree_gen()
#     # Steps to visualise:
#     root, depth = treeNode.generateTree(treeNode.sample_data, 0)
#     #fig, ax = plt.subplots(figsize=(18, 10))
#     #gap = 1.0/depth
#     #treeNode.visualize_tree(root, 0.0, 1.0, 0.0, 1.0)
#     #fig.subplots_adjust(top=0.83)
#     #plt.show()
#     cross_eval = eval()
#     print(cross_eval.eval_tree(root))


