# Decision Tree Coursework Usage
The decision tree algorithm is demonstrated in the Jupyter notebook file 'Main.ipynb' - there is a written description of all cells. Run all of them to generate the tree on the clean dataset.

The 'src' folder contains all helper functions, and the 'test' folder contains the dataset.

The Juypter notebook demonstrates the following:

1. The decision tree is generated based on the given dataset. The datasets are located in 'test' subdirectory and can be changed by changing the  filepath given to the 'data' paramater in the notebook in section 'Loading a Specified Dataset'.

2. The dataset is then split and then evaluated using 10-fold cross validation. The trees are also pruned during this stage.

3. As the trees are being generated, the tree visualiser saves images of the pre-pruned and post-pruned trees in the 'tree' subdictory, but also displays a pair in the notebook itself.

4. The final performance metrics are printed after the trees are done generating.

5. At the end, there is a section of code that allows a datapoint to be evaluated on the pruned tree.