import numpy as np
import matplotlib as plt


class tree:
    def __init__(self, attribute, val=0, left=None, right=None):
        # Creates leaf node by default
        self.node = {'attribute': attribute, 'val': val, 'left': left, 'right': right}   

class tree_gen:
    def __init__(self, filepath, depth=0) -> None:
    
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
        res = {'split': None, 'left': None, 'right': None}
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
        res['split'] = best_split
        return res
        # return: {split: , left: , right: }
        
    
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
    
    def visualize_tree(self, tree) -> None:
        """
        Visualize the given decision tree
        :param tree: decision tree
        :return: None
        """
        
        # Use matplotlib to plot tree
        pass
        
# tree_gen = tree_gen()
# print(tree_gen.clean_data)
