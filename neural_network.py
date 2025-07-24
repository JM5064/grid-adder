import numpy as np
import model.layer as la


class NeuralNetwork:

    def __init__(self):
        print("Initializing network")
        self.l1 = la.Layer(100, weights=self.get_weights(1), biases=np.rot90([self.get_biases(1)], 3))
        self.l2 = la.Layer(100, self.l1, weights=self.get_weights(2), biases=np.rot90([self.get_biases(2)], 3))
        self.l3 = la.Layer(10, self.l2, weights=self.get_weights(3), biases=np.rot90([self.get_biases(3)], 3))
        print("Network initialized")


    def get_weights(self, layer_num):
        if layer_num == 1:
            return np.loadtxt("model/l1weights.txt")
        elif layer_num == 2:
            return np.loadtxt("model/l2weights.txt")
        elif layer_num == 3:
            return np.loadtxt("model/l3weights.txt")


    def get_biases(self, layer_num):
        if layer_num == 1:
            return np.loadtxt("model/l1biases.txt")
        elif layer_num == 2:
            return np.loadtxt("model/l2biases.txt")
        elif layer_num == 3:
            return np.loadtxt("model/l3biases.txt")

    
    def predict(self, image):
        flattened = image.reshape(784, 1)
        
        self.l1.update(flattened)
        self.l2.update()
        self.l3.update()

        maxim = 0
        maxim_index = 0

        for j in range(len(self.l3.matrix)):
            if self.l3.matrix[j, 0] > maxim:
                maxim = self.l3.matrix[j, 0]
                maxim_index = j

        return maxim_index

