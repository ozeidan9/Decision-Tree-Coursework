import numpy as np

class Evaluation:
    def __init__(self,data):
        self.data = data
        self.test_set ={}
        self.training_set = {}
        #self.filter() #not need to remove answer from array right now
        self.randomise()
        self.cross_val()
        #print(self.data)
        # for i in range(10):
        #     print("TEST SET: ")
        #     print(self.test_set[i])
        #     print("TRAING SET: ")
        #     print(self.training_set[i])
        
    def randomise(self): #randomises the input data
        np.random.shuffle(self.data)

    def filter(self):
        self.data = np.delete(self.data,7,axis = 1) #deletes the room number (final column) from the data

    def cross_val(self,k=10): #k-fold cross validation

        split = len(self.data)//k
        for i in range(k): #splits data into training:testing
            self.test_set[i] = self.data[i*split:(i*split)+split]
            self.training_set[i] = np.delete(self.data,slice(i*split,(i*split)+split),axis = 0)


if __name__ == "__main__":
    clean_data = np.loadtxt("test/sample_set.txt", dtype=float)
    Evaluation(clean_data)