
class eval():
    def __init__(self):
        pass
    
    
    def eval_tree(self, root):
        """ DFS traversal through decision tree and prins leaf nodes

        Input: root node (type: tree)
        return an integer
        """
        if not root.node['left'] and not root.node['right']: # leaf node
            return root.node['attribute']

        if root.node['val']<=root.node['attribute']:
            return self.eval_tree(root.node['left'])
        else:    
            return self.eval_tree(root.node['right'])
    
    
    
        
        
        
        