import numpy as np
from .losses import Losses
from .optimizers import Optimizers

class Spark(object):
    def __init__(self, inputs, outputs, learningRate=0.01, loss="Mean Squared", optimizer="Vanilla", layers=[]):
        # Inputs
        self.X = inputs

        # Outputs
        self.y = outputs

        # Loss
        self.loss, self.lossPrime = Losses(loss)

        # Layers
        self.layers = layers

        # Optimizers
        optimizer = Optimizers(optimizer)
        for layer in layers:
            layer.addOptimizer(learningRate, optimizer)

    def run(self, epochs=10):
        inputs = self.X
        outputs = self.y
        loss = self.loss
        lossPrime = self.lossPrime
        layers = self.layers

        for epoch in range(epochs):
            lastInput = inputs

            # Forward Propagate Layers
            for layer in layers:
                lastInput = layer.forward(lastInput)

            # Backward Propagate Layers
            gradient = lossPrime(lastInput, outputs)

            for layer in reversed(layers):
                gradient = layer.backward(gradient, loss, outputs)

            print("Epoch: " + str(epoch))
            print("Loss: " + str(loss(lastInput, outputs)))
            print()

    def predict(self, y):
        for layer in self.layers:
            y = layer.forward(y)

        return y
