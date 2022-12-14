from sklearn.datasets import load_iris     #for dataset
import numpy as np               
import matplotlib.pyplot as plt  
import random

iris = load_iris()      #load the dataset
data = iris.data                 #get features  
target = iris.target             #get labels
shape = data.shape               #shape of data

#convert into numpy array
data = np.array(data).reshape(shape[0],shape[1])
target = np.array(target).reshape(shape[0],1)

#print shape
print("Data Shape   = {}".format(data.shape))
print("Target Shape = {}".format(target.shape))
print('Classes : {}'.format(np.unique(target)))

random.seed(3) # My UID ends with '03' hence I use the seed of 3
random.sample( range(0,149),   5)

X_train = data[[60,139,33,94,121]]
print(X_train)
Y_train = target[[60,139,33,94,121]]
print(Y_train)

#HYPERPARAMETERS Initialise

#num of target labels
num_classes = len(np.unique(target))

#define layer_neurons
input_units  = 4   #neurons in input layer
hidden_units = 3   #neurons in hidden layer
output_units = 3   #neurons in output layer

#define hyper-parameters
learning_rate = 0.5

#regularization parameter
beta = 0.00001

#num of iterations
iters = 1000

"""**Dimensions of Parameters  **

Shape of layer1_weights (Wxh) = (4,3)    
Shape of layer1_biasess (Bh) = (3,1)      
Shape of layer2_weights (Why) = (3,3)       
Shape of layer2_biasess (By) = (3,1)     
"""

#PARAMETERS

#initialize parameters i.e weights
def initialize_params():
    np.random.seed(3)
    layer1_weights = np.random.randn(input_units,hidden_units)          
    layer1_biases = np.ones((hidden_units,1))                                       
    layer2_weights = np.random.randn(hidden_units,output_units) 
    layer2_biases = np.ones((output_units,1))
    
    parameters = dict()
    parameters['layer1_weights'] = layer1_weights
    parameters['layer1_biases'] = layer1_biases
    parameters['layer2_weights'] = layer2_weights
    parameters['layer2_biases'] = layer2_biases
    
    return parameters

#activation functions and derivatives
def relu(X):
    X = np.where(X >= 0, X, 0)     
    return X

def der_relu(X):
    X  = np.where(X >= 0, 1, 0) 
    return X

def softmax(X):
    exp_X = np.exp(X)
    exp_X_sum = np.sum(exp_X,axis=1).reshape(-1,1)
    exp_X = (exp_X/exp_X_sum)
    return exp_X

#forward propagation
def forward_prop(train_dataset,parameters,train_labels,i):
    cache = dict()            #to store the intermediate values for backward propagation
    m = len(train_dataset)    #number of training examples
    
    #get the parameters
    layer1_weights = parameters['layer1_weights']
    layer1_biases = parameters['layer1_biases']
    layer2_weights = parameters['layer2_weights']
    layer2_biases = parameters['layer2_biases']
    
    #forward prop
    logits = np.matmul(train_dataset,layer1_weights) + layer1_biases.T
    activation1 = np.array(relu(logits)).reshape(m,hidden_units)
    activation2 = np.array(np.matmul(activation1,layer2_weights) + layer2_biases.T).reshape(m,output_units)
    output = np.array(softmax(activation2)).reshape(m,num_classes)
    
    #fill in the cache
    cache['output'] = output
    cache['activation1'] = activation1
    
    # Calculate Loss
    cr_loss = -(train_labels*np.log(output)).sum()
    print( "\nCross Entropy Loss after iteration {} is {}".format(i+1, cr_loss))
    return cache,output

#backward propagation
def backward_prop(train_dataset,train_labels,parameters,cache):
    derivatives = dict()         #to store the derivatives
    
    #get stuff from cache
    output = cache['output']
    activation1 = cache['activation1']
    
    #get parameters
    layer1_weights = parameters['layer1_weights']
    layer2_weights = parameters['layer2_weights']
    layer1_biases = parameters['layer1_biases']
    layer2_biases = parameters['layer2_biases']
    
    #calculate errors
    error_output = output - train_labels
    error_activation1 = np.matmul(error_output,layer2_weights.T)
    error_activation1 = np.multiply(error_activation1,der_relu(activation1))
    
    #calculate partial derivatives
    partial_derivatives2 = np.matmul(activation1.T,error_output)/len(train_dataset)
    partial_derivatives1 = np.matmul(train_dataset.T,error_activation1)/len(train_dataset)
    partial_derivatives2_bias = np.sum(error_output.T, axis = 1)/len(train_dataset)
    partial_derivatives2_bias  = partial_derivatives2_bias.reshape(-1,1)
    partial_derivatives1_bias = np.sum(error_activation1.T, axis = 1)/len(train_dataset)
    partial_derivatives1_bias  = partial_derivatives1_bias.reshape(-1,1)

    #store the derivatives
    derivatives['partial_derivatives1'] = partial_derivatives1
    derivatives['partial_derivatives2'] = partial_derivatives2
    derivatives['partial_derivatives1_bias'] = partial_derivatives1_bias
    derivatives['partial_derivatives2_bias'] = partial_derivatives2_bias
    
    return derivatives

#update the parameters
def update_params(derivatives,parameters, i):
    #get the parameters
    layer1_weights = parameters['layer1_weights']
    layer2_weights = parameters['layer2_weights']
    layer1_biases = parameters['layer1_biases']
    layer2_biases = parameters['layer2_biases']
    
    #get the derivatives
    partial_derivatives1 = derivatives['partial_derivatives1']
    partial_derivatives2 = derivatives['partial_derivatives2']
    partial_derivatives1_bias = derivatives['partial_derivatives1_bias']
    partial_derivatives2_bias = derivatives['partial_derivatives2_bias']
    
    #update the derivatives
    layer1_weights -= (learning_rate*(partial_derivatives1 + beta*layer1_weights))
    layer2_weights -= (learning_rate*(partial_derivatives2 + beta*layer2_weights))
    layer1_biases = layer1_biases - (learning_rate*(partial_derivatives1_bias + beta*layer1_biases))
    layer2_biases = layer2_biases - (learning_rate*(partial_derivatives2_bias + beta*layer2_biases))

    print("Weights updation after {} iteration from Input neuron to Hidden Layer: {}".format(i+1,layer1_weights))
    print("Weights updation after {} iteration from Hidden Layer to Output Layer: {}".format(i+1,layer2_weights))
    print("Bias updation after {} iteration from Input neuron to Hidden Layer: {}".format(i+1,layer1_biases))
    print("Bias updation after {} iteration from Hidden Layer to Output Layer: {}".format(i+1,layer2_biases))
    
    #update the dict
    parameters['layer1_weights'] = layer1_weights
    parameters['layer2_weights'] = layer2_weights
    parameters['layer1_biases'] = layer1_biases
    parameters['layer2_biases'] = layer2_biases
    
    return parameters

#Implementation of 3 layer Neural Network

#training function
def training(train_dataset,train_labels,iters=1000):
 
    #WEIGHTS
    global layer1_weights
    global layer1_biases
    global layer2_weights
    global layer2_biases
  
    #initialize the parameters
    parameters = initialize_params()
    
    layer1_weights = parameters['layer1_weights']
    layer1_biases = parameters['layer1_biases']
    layer2_weights = parameters['layer2_weights']
    layer2_biases = parameters['layer2_biases']

    print("Initial Randomised weights at Layer 1" ,  layer1_weights )
    print("Initial Randomised weights at Layer 2" ,  layer2_weights )
    #to store final predictons after training
    final_output = []
    
    for i in range(iters):
        
        #forward propagation
        cache,output = forward_prop(train_dataset,parameters,train_labels,i)
        
        #backward propagation
        derivatives = backward_prop(train_dataset,train_labels,parameters,cache)     
        
        #update the parameters
        parameters = update_params(derivatives,parameters,i)
        
        #update final output
        final_output = output
    
    return final_output

train_dataset =  X_train
train_labels = Y_train

#make train_dataset and train_labels
train_dataset = np.array(X_train).reshape(-1,4)
train_labels = np.zeros([train_dataset.shape[0],num_classes])

#one-hot encoding
for i,label in enumerate(Y_train):
    train_labels[i,label] = 1

print(train_labels)

#normalizations
for i in range(input_units):
    mean = train_dataset[:,i].mean()
    std = train_dataset[:,i].std()
    train_dataset[:,i] = (train_dataset[:,i]-mean)/std

#train data
final_output = training(train_dataset,train_labels,iters=2)

print("Softmax Probabilities for 5 training dataset after 2 iterations", final_output)
