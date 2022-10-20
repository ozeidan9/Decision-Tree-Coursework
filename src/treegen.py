import numpy as np
import matplotlib as plt
from collections import deque


class tree:
    def __init__(self, attribute, val=0, left=None, right=None):
        # Creates leaf node by default
        self.node = {'attribute': attribute, 'val': val, 'left': left, 'right': right}   

class tree_gen:
    def __init__(self, depth=0) -> None:
    
        clean_filepath = "test/clean_dataset.txt"
        noisy_filepath = "test/noisy_dataset.txt"
        
        self.clean_data = np.loadtxt(clean_filepath, dtype=float)
        self.noisy_data = np.loadtxt(noisy_filepath, dtype=float)

        self.depth = depth

    def generate_decision_tree(self, training_dataset, depth):
        """
        Generate a decision tree from the given data
        :param training_dataset: 2000x8 matrix of training data
        :param depth: used to compute maximal depth of tree - for plotting purposes
        :return: decision tree
        """
        # if all samples have same label, return a leaf node with this value and depth
        if len(np.unique(training_dataset[:, -1])) == 1:
            attribute = np.unique(training_dataset[:,7])
            leaf_node = tree(attribute=int(attribute))
            return (leaf_node, depth)
        
        # else, find the best split and return a node with the best split and depth
        else:
            attribute, value = self.find_split(training_dataset)
            l =np.where(training_dataset[:, attribute-1] <= value)
            r =np.where(training_dataset[:, attribute-1] > value)
            left_dataset = training_dataset[l]
            right_dataset = training_dataset[r]
            left_branch, left_depth = self.generate_decision_tree(left_dataset, depth+1)
            right_branch, right_depth = self.generate_decision_tree(right_dataset, depth+1)
            node = tree(attribute=attribute, val=value, left=left_branch, right=right_branch)
            return (node, max(left_depth, right_depth))
            
    def find_split(self, training_dataset):
        """
        Find the best split for the given data
        :param training_dataset: 2000x8 matrix of training data
        :return: best split
        """
        best_split = [None, None]
        best_entropy = 0
        #Calculate the maximum entropy for splitting 
        for row in range(training_dataset.shape[0]):
            #Calculate entropy for every column
            for column in range(training_dataset.shape[1]-1):
                #Split array into top and bottom, and add
                topEntropy = self.compute_entropy(training_dataset[0:row, column])
                bottomEntropy = self.compute_entropy(training_dataset[row:training_dataset.shape[0], column])
                totalEntropy = bottomEntropy + topEntropy 
                if totalEntropy < best_entropy:
                    best_entropy = totalEntropy
                    best_split = [row, column]
        return best_split
        
    
    def compute_entropy(training_dataset):
        """
        Calculate the best splitpoint in the given column
        """
        entropy = 0
        #Need elements as a histogram
        elements, count = np.unique(training_dataset, return_counts=True)
        for i in range(len(elements)):
            elementProb = count[i]/len(count)
            entropy -= elementProb * np.log2(elementProb)
        return entropy
    
    def visualize_tree(self, root, xmin, xmax, ymin, ymax) -> None:
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
            atri = node['atribute']
            val = node['value']
            text = '['+str(atri)+']:'+str(val)
            #---------------------
            center = xmin+(xmax-xmin)/2.0
            d = (center-xmin)/2.0
            
            if node['left'] != None and node['right'] != None:
                an1 = ax.annotate(0, xy=(center, ymax), xycoords="data",
                va="bottom", ha="center",
                bbox=dict(boxstyle="round", fc="w"))
                
            elif node['left'] != None:
                queue.append((node['left'], xmin, center, ymin, ymax-gap))
                ax.annotate(text, xy=(center-d, ymax-gap), xytext=(center, ymax),
                            arrowprops=dict(facecolor='grey', shrink=10),
                            )
                
            elif node['right'] != None:
                queue.append((node['right'], center, xmax, ymin, ymax-gap))
                ax.annotate(text, xy=(center+d, ymax-gap), xytext=(center, ymax),
                            arrowprops=dict(facecolor='grey', shrink=10),
                            )            
            else:
                continue
                
tree_gen = tree_gen()

# Setps to visualise:
root, depth = tree_gen.generate_decision_tree(tree_gen.clean_data, 0)
fig, ax = plt.subplots(figsize=(18, 10))
gap = 1.0/depth
tree_gen.visualize_tree(root, 0.0, 1.0, 0.0, 1.0)
fig.subplots_adjust(top=0.83)
plt.show()

