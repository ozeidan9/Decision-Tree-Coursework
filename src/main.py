import numpy as np

class readData:
    def __init__(self, filepath, noisy=False):
        self.x = np.loadtxt(filepath, dtype=float, usecols=(1,2,3,4,5,6,7))
        print(self.x.shape)
        # x = []
        # y_labels = []
        # for line in open(filepath):
        #     if line.strip() != "": # handle empty rows in file
        #         row = line.strip().replace("\t", " ").split(" ")
        #         if noisy:
        #             x.append(list(map(float, row)))
        #             y_labels.append(0)
        #         else:
        #             x.append(list(map(float, row[:-1]))) 
        #             y_labels.append(row[-1])
        # y = np.unique(y_labels)
        # self.x = np.array(x)
        # self.y = np.array(y)
    
    def getXData(self):
        return self.x
    
    def getYData(self):
        return self.y

    def printDataSet(self):
        print("X dataset:")
        print(self.x.shape)
        for i in self.x:
            print(i)
        print("Y dataset:")
        print(self.y.shape)
        for i in self.y:
            print(i)

# dataset = readData("src/test/noisy_dataset.txt", True)
# dataset.printDataSet()