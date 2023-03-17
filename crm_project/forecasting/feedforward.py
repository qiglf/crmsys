import random
import math
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'th_project.settings')
import django
django.setup()
from crm_project.models import Member, Work

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.weights_ih = self.initialize_weights(self.input_nodes, self.hidden_nodes)
        self.weights_ho = self.initialize_weights(self.hidden_nodes, self.output_nodes)

        self.bias_h = self.initialize_weights(1, self.hidden_nodes)
        self.bias_o = self.initialize_weights(1, self.output_nodes)

    def transpose(self, matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    def initialize_weights(self, rows, cols):
        return [[random.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def matrix_multiply(self, a, b):
        if len(a[0]) != len(b):
            raise ValueError(
                f"Number of columns in matrix 'a' should match the number of rows in matrix 'b'. Got {len(a[0])} columns in 'a' and {len(b)} rows in 'b'.")

        result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def matrix_add(self, a, b):
        result = [[0 for _ in range(len(a[0]))] for _ in range(len(a))]
        for i in range(len(a)):
            for j in range(len(a[0])):
                result[i][j] = a[i][j] + b[i][j]
        return result

    def elementwise_apply(self, matrix, func):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = func(matrix[i][j])
        return matrix

    def train(self, input_data, target_data, learning_rate=0.1):

        # Forward pass
        hidden_inputs = self.matrix_multiply(input_data, self.weights_ih)
        hidden_outputs = self.elementwise_apply(hidden_inputs, self.sigmoid)

        final_inputs = self.matrix_multiply(hidden_outputs, self.weights_ho)
        final_outputs = self.elementwise_apply(final_inputs, self.sigmoid)

        # Backpropagation
        output_errors = [[target_data[i] - final_outputs[i][0]] for i in range(len(target_data))]
        output_gradients = self.elementwise_apply(final_outputs, self.sigmoid_derivative)

        for i in range(len(output_gradients)):
            output_gradients[i][0] *= output_errors[i][0] * learning_rate

        hidden_errors = self.matrix_multiply(output_errors, [row[::-1] for row in zip(*self.weights_ho)])
        hidden_gradients = self.elementwise_apply(hidden_outputs, self.sigmoid_derivative)

        for i in range(len(hidden_gradients)):
            hidden_gradients[i][0] *= hidden_errors[i][0] * learning_rate

            # Update weights and biases
            self.weights_ho = self.matrix_add(self.weights_ho,
                                              self.matrix_multiply(self.transpose(hidden_outputs), output_gradients))
            self.weights_ih = self.matrix_add(self.weights_ih,
                                              self.matrix_multiply(self.transpose(input_data), hidden_gradients))

            self.bias_o = self.matrix_add(self.bias_o, output_gradients)
            self.bias_h = self.matrix_add(self.bias_h, hidden_gradients)

    def predict(self, input_data):

        hidden_inputs = self.matrix_multiply(input_data, self.weights_ih)
        hidden_outputs = self.elementwise_apply(hidden_inputs, self.sigmoid)
        final_inputs = self.matrix_multiply(hidden_outputs, self.weights_ho)
        final_outputs = self.elementwise_apply(final_inputs, self.sigmoid)

        return final_outputs


def normalize_data(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def run():
    input_data = []
    target_data = []

    members_data = Member.objects.all() # Get data from your Member model

    for member in members_data:
        input_data.append([
            normalize_data(member.total_years_of_exp, 0, 20),   # Assuming max experience is 20 years
            normalize_data(member.amount_of_workplaces, 0, 10),    # Assuming max workplaces is 10

            # Add more features here
        ])
        target_data.append([member.hire_success])

    nn = NeuralNetwork(input_nodes=2, hidden_nodes=5, output_nodes=1)  # Set input_nodes to 2

    # Train the neural network
    epochs = 1000
    for epoch in range(epochs):
        for i in range(len(input_data)):
            input_matrix = [input_data[i]]  # Convert input_data[i] to a matrix
            nn.train(input_matrix, target_data[i])

    # Make predictions
    for i in range(len(input_data)):
        input_matrix = [input_data[i]]  # Convert input_data[i] to a matrix
        prediction = nn.predict(input_matrix)
        print(f"Prediction for member {i}: {prediction}")

run()