```python
# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
import torch.optim as optim

# Define a function to generate random data for demonstration
def generate_random_data(size: int) -> tuple:
    """
    Generate random data for demonstration.

    Args:
    size (int): The size of the data.

    Returns:
    tuple: A tuple containing the input data and the corresponding output data.
    """
    # Generate random input data
    X = np.random.rand(size, 1)
    # Generate random output data
    y = 3 * X + 2 + np.random.randn(size, 1) / 1.5  # Adding some noise to the data
    return X, y

# Define a function to train a linear regression model
def train_linear_regression(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    """
    Train a linear regression model.

    Args:
    X (np.ndarray): The input data.
    y (np.ndarray): The corresponding output data.

    Returns:
    LinearRegression: The trained linear regression model.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Create a linear regression model
    model = LinearRegression()
    # Train the model
    model.fit(X_train, y_train)
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
    return model

# Define a simple neural network using PyTorch
class SimpleNeuralNetwork(nn.Module):
    """
    A simple neural network.
    """
    def __init__(self):
        super(SimpleNeuralNetwork, self).__init__()
        # Define the layers of the neural network
        self.fc1 = nn.Linear(1, 10)  # Input layer with 1 neuron and hidden layer with 10 neurons
        self.fc2 = nn.Linear(10, 1)  # Hidden layer with 10 neurons and output layer with 1 neuron

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the neural network.

        Args:
        x (torch.Tensor): The input data.

        Returns:
        torch.Tensor: The output of the neural network.
        """
        # Apply the activation function to the output of the first layer
        x = torch.relu(self.fc1(x))
        # Apply the activation function to the output of the second layer
        x = self.fc2(x)
        return x

# Define a function to train the neural network
def train_neural_network(X: np.ndarray, y: np.ndarray) -> SimpleNeuralNetwork:
    """
    Train the neural network.

    Args:
    X (np.ndarray): The input data.
    y (np.ndarray): The corresponding output data.

    Returns:
    SimpleNeuralNetwork: The trained neural network.
    """
    # Convert the data to PyTorch tensors
    X_tensor = torch.from_numpy(X.astype(np.float32))
    y_tensor = torch.from_numpy(y.astype(np.float32))
    # Create the neural network
    model = SimpleNeuralNetwork()
    # Define the loss function and the optimizer
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    # Train the model
    for epoch in range(1000):
        # Forward pass
        outputs = model(X_tensor)
        # Calculate the loss
        loss = criterion(outputs, y_tensor)
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        # Update the model parameters
        optimizer.step()
        # Print the loss at each 100th epoch
        if epoch % 100 == 0:
            print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
    return model

if __name__ == "__main__":
    # Generate random data
    X, y = generate_random_data(100)
    # Train a linear regression model
    linear_regression_model = train_linear_regression(X, y)
    # Train the neural network
    neural_network_model = train_neural_network(X, y)
```