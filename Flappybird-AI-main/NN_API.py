import numpy as np


class LayerDense:
  def __init__(self, n_inputs, n_neurons):
      self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
      self.biases = np.zeros((1, n_neurons))

  def forward(self, inputs):
      self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:
  def forward(self, inputs):
    self.output = np.maximum(0, inputs)

class Activation_Inverse_Tan:
  def forward(self, inputs):
    self.output = np.arctan(inputs)

class Activation_Softmax:
  def forward(self, inputs):
    exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
    probabilities = exp_values/np.sum(exp_values, axis=1, keepdims=True)
    self.output = probabilities


class Loss:
  def calculate(self, output, y):
    sample_losses = self.forward(output, y)
    data_loss = np.mean(sample_losses)
    return data_loss

class Loss_CategoricalCrossentropy(Loss):
  def forward(self, y_pred, y_true):
    samples = len(y_pred)
    y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

    if len(y_true.shape) == 1:
      correct_confidences = y_pred_clipped[range(samples), y_true]
    elif len(y_true.shape) == 2:
      correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)

    negative_log_likelihoods = -np.log(correct_confidences)
    return negative_log_likelihoods



class Neural_Network:
  def __init__(self, format: list, activationFunc) -> None:
      self.ActivationFunc = activationFunc
      self.format = format

      self.layers = []
      for i in range(len(format)-1):
          self.layers.append(LayerDense(self.format[i], self.format[i+1]))

  def forward(self, inputs: list) -> None:
      self.output = inputs
      for layer in self.layers:
          layer.forward(self.output)
          self.ActivationFunc.forward(layer.output)
          self.output = self.ActivationFunc.output

  def YoN(self) -> bool:
      return (self.output >= 0)

  def shift_weights(self, range: float) -> None:
      for layer in self.layers:
          for weight in layer.weights:
              weight += range * np.random.randn()

  def shift_biases(self, range) -> None:
      for layer in self.layers:
          for bias in layer.biases:
              bias += range * np.random.randn()

  def clone(self):
      new_network = Neural_Network(self.format, self.ActivationFunc)
      for newLayer, oldLayer in zip(new_network.layers, self.layers):
          weights = oldLayer.weights
          biases = oldLayer.biases

          weights_copy = np.array(weights.tolist())
          biases_copy = np.array(biases.tolist())

          newLayer.weights = weights_copy
          newLayer.biases = biases_copy
      return new_network
