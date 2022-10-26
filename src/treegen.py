import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self, depth=0):
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
    
    def visualize_tree(self, root, maxdepth, file):
        """ Visualize the decision tree using matplotlib and a recurisive dfs function and save it to a file

        :param root: the root node of the tree
        :param maxdepth: the maximum depth of the tree
        :param file: the file name to save the tree figure to
        :return: None
        """
        plt.figure(figsize=(min(2**maxdepth, 2**5), maxdepth), dpi=80)  # intialize matplotlib figure
       
        def dfs_tree_plotter(root, x, y, depth):
            """
            Visualize the given decision tree by performing deapth first search and using matplotlib
            :param tree: current tree node
            :param x: x coordinate of current node
            :param y: y coordinate of each level
            :depth: current depth of tree
            :return: None
            """
            if not root.node['left'] and not root.node['right']: 
                # leaf node:
                plt.text(x, y, str(root.node['attribute']), size='smaller', rotation=0, ha="center", va="center",
                        bbox=dict(boxstyle="round", ec=(0., 0., 0.), fc=(1., 1., 1.)))
                return
            
            # at least one child node:
            plt.text(x, y, str("x" + str(root.node['attribute'])) + " <= " + str(root.node['val']), size='smaller', rotation=0,
                    ha="center", va="center", bbox=dict(boxstyle="round", ec=(0., 0., 0.), fc=(1., 1., 1.)))
            
            # dy: proportional to 1/(2^depth), since  every level has a max of 2**depth nodes. 
            # dx: divided into 2^depth parts
            xleft = x - 2/(2**depth)
            xright = x + 2/(2**depth)
            ychild = y - 5  # equal heigh for child nodes
            
            # plot left and right edges using the same color
            x_val = [xleft, x, xright]
            y_val = [ychild, y, ychild]
            plt.plot(x_val, y_val)
            
            dfs_tree_plotter(root.node['left'], xleft, ychild, depth+1)     # left child recurisve call
            dfs_tree_plotter(root.node['right'], xright, ychild, depth+1)   # right child recursive call
            return
        
        dfs_tree_plotter(root, x=0, y=50, depth=0)
        plt.axis('off') # Remove axes from plot
        plt.savefig(file) 
        plt.close()
        return
    

if __name__ == "__main__":
    treeNode = tree_gen()
    # Steps to visualise:
    # Train  tree on the clean dataset and plot tree
    root, depth = treeNode.generateTree(treeNode.sample_data, depth=0)
    treeNode.visualize_tree(root, depth, "sample_data.png") # CHANGE TO CLEAN_DATA LATER
    
    # cross_eval = eval()
    # print(cross_eval.eval_tree(root))


