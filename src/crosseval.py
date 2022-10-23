
class eval():
    def __init__(self):
        self.leaf_nodes = []
    
    def eval_tree(self, root):
        """ DFS traversal through decision tree and prins leaf nodes

        Input: root node (type: tree)
        """
        if not root.node['left'] and not root.node['right']: # leaf node
            self.leaf_nodes.append(root.node['attribute'])
            return

        self.eval_tree(root.node['left'])
        self.eval_tree(root.node['right'])
        return self.leaf_nodes
    
    
    
        
        
        
        