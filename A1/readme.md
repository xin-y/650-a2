
In this problem, you will implement the backpropagation algorithm and train your first multi-layer perceptron
to distinguid between 4 classes. You should implement everything on your own without using existing libraries
like Tensorflow, Keras, or PyTorch.

You are provided with two files “train data.csv“ and “train labels.csv“ The dataset contains 24754 samples, each
with 784 features divided into 4 classes (0,1,2,3). You should divide this into training, and validation sets (a
validation set is used to make sure your network did not overfit). You will then provide your model which will
be tested with an unseen test set.

Use one input layer, one hidden layer, and one output layer in your implementation. The labels are one-hot
encoded. For example, class 0 has a label of [1, 0, 0, 0] and class 2 has a label of [0,0,1,0]. Make sure you use the
appropriate activation function in the output layer. You are free to use any number of nodes in the hidden layer.
You need to provide one single function that allows us to use the network to predict the test set. This function
should output the labels one-hot encoded in a numpy array.
