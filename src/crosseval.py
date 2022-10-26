'''import numpy as np
class Eval:
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
            return self.eval_tree(root.node['right'], input)    '''

#This is the base function, modified version used in evaluation.py. Delete this later :)