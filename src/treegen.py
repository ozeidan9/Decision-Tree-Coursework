import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax

class treeNode:
    def __init__(self, attribute, val=None, left=None, right=None):
        #Node attributes
        self.node = {'attribute': attribute, 'val': val, 'left': left, 'right': right} 

    #For debugging purposes
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
        
    def visualizeTree(self, maxdepth, file, displayTree=False):
        """
        Visualize the decision tree using matplotlib and a recurisive dfs function and save it to a file
        :param root: the root node of the tree
        :param maxdepth: the maximum depth of the tree
        :param file: the file name to save the tree figure to
        :return: None
        """
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
            bbox_style = dict(boxstyle="square", ec=(0., 0., 0.), fc=(1., 1., 1.))
            plt.text(x, y, str("x" + str(root.node['attribute'])) + " <= " + str(root.node['val']), size='smaller', rotation=0,
                    ha="center", va="center", bbox=bbox_style)
            
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
        plt.figure(figsize=(min(2**maxdepth, 2**5), maxdepth), dpi=80)  # intialize matplotlib figure
        dfs_tree_plotter(self, x=0, y=50, depth=0)
        plt.axis('off') # Remove axes from plot
        plt.savefig(file) 
        plt.close()
        return


class treeGen:
    def __init__(self, data=None, depth=0) -> None:
        self.dataset = data
        self.depth = depth

    def generateTree(self, trainingDataset=None, depth=0):
        """
        Generate a decision tree from the given data
        :param training_dataset: 2000x8 matrix of training data
        :param depth: used to compute maximal depth of tree - for plotting purposes
        :return: decision tree
        """
        if trainingDataset is None:
            trainingDataset = self.dataset
        # if all samples have same label, return a leaf node with this value and depth
        # ie if all the remaining samples are of the same sample (your dataset correspondes to only one room)
        if len(np.unique(trainingDataset[:, -1])) <= 1:
            #print("Node completed")
            attribute = np.unique(trainingDataset[:, -1])
            leaf_node = treeNode(attribute=int(attribute))
            return (leaf_node, depth)
        # else, find the best split and return a node with the best split and depth
        else:
            topSet, bottomSet, splitAttrib, value = self.splitSet(trainingDataset)
            leftBranch, leftDepth = self.generateTree(topSet, depth+1)
            rightBranch, rightDepth = self.generateTree(bottomSet, depth+1)
            node = treeNode(attribute=splitAttrib, val=value, left=leftBranch, right=rightBranch)
            return (node, max(leftDepth, rightDepth))

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
                value = trainingSet[row, column]
                topSet = trainingSet[np.where(trainingSet[:, column] <= value)]
                bottomSet = trainingSet[np.where(trainingSet[:, column] > value)]
                topEntropy = self.calculateEntropy(topSet)
                bottomEntropy = self.calculateEntropy(bottomSet)
                totalEntropy = bottomEntropy + topEntropy 
                #Record best entropy so far
                if totalEntropy < bestEntropy:
                    bestEntropy = totalEntropy
                    bestSplit = (topSet, bottomSet, column, value)
        return bestSplit
    
    def calculateEntropy(self, training_dataset):
        """
        Calculate the best splitpoint in the given column
        """
        entropy = 0
        #Need elements as a histogram
        elements, count = np.unique(training_dataset, return_counts=True)
        total = sum(count)
        for i in range(len(elements)):
            elementProb = count[i]/total
            entropy -= elementProb * np.log2(elementProb)
        return entropy * training_dataset.size

#Testing
if __name__ == "__main__":
    from evaluation import*
    from prune import pruning
    import numpy as np

    clean_filepath = "test/clean_dataset.txt"
    noisy_filepath = "test/noisy_dataset.txt"
    sample_filepath = "test/sample_set.txt"
    data = np.loadtxt(noisy_filepath, dtype=float)
    np.random.shuffle(data) #randomises rows
    test_set,training_set,validation_set = cross_val(data)
    accuracy,precision,recall,f1 = 0,{1:0,2:0,3:0,4:0},{1:0,2:0,3:0,4:0},{1:0,2:0,3:0,4:0}
    pruned_accuracy,pruned_precision,pruned_recall,pruned_f1 = 0,{1:0,2:0,3:0,4:0},{1:0,2:0,3:0,4:0},{1:0,2:0,3:0,4:0}
    print(len(data))
    for i in range(10):
        print(i,": ")
        print("length: ", len(test_set[i]),len(validation_set[i]),len(training_set[i]))
    #macro_avg_f1= 0
    for i in range(10):
        print("Generating Tree: ",i+1)
        initNode = treeGen(training_set[i])
        root, depth = initNode.generateTree()
        print("Depth: ",depth)
        root.visualizeTree(depth, "src/tree_diagram.png")
        #print("Before Pruning: ")
        accuracy,precision,recall,f1 = calc_avg_metrics(root,test_set[i],accuracy,precision,recall,f1)
        
        tree,depth = pruning(root,root,validation_set[i])
        pruned_accuracy,pruned_precision,pruned_recall,pruned_f1 = calc_avg_metrics(tree, test_set[i],pruned_accuracy,pruned_precision,pruned_recall,pruned_f1)
        #print("After Pruning: ")
        tree.visualizeTree(depth, f"src/tree_diagramPRUNED{i}.png") # CHANGE TO CLEAN_DATA

    '''initNode = treeGen(data)
    root, depth = initNode.generateTree()
    print("Depth: ",depth)
    root.visualizeTree(depth, "src/tree_diagramAll_data.png")
    #print("Before Pruning: ")
    tree,depth = pruning(root,root,data)
    #print("After Pruning: ")
    tree.visualizeTree(depth, f"src/tree_diagramPRUNED_All_Data.png") # CHANGE TO CLEAN_DATA'''

    print("PRE-PRUNE: ",accuracy,precision,recall,f1)
    print("\n")
    print("POST-PRUNE: ",pruned_accuracy,pruned_precision,pruned_recall,pruned_f1 )
     