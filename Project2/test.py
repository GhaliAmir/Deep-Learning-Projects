# -*- coding: utf-8 -*-
"""test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DojJ0N1hxDEw7ceaFUg_VETbn15Er7Wl
"""

import torch
import random
import helpers as h
import modules as m
import matplotlib.pyplot as plt

#Setting a random seed and generating the data

torch.manual_seed(1)
inputs, targets = h.generate_disc_data(n=1000)

'''
#Plot the distribution of the generated data, to see how it looks like

plt.scatter(inputs[:,0].tolist(), inputs[:,1].tolist(), c = targets.tolist(), cmap = 'cividis')
#plt.savefig('data.png')
plt.xlabel("X coordinate")
plt.ylabel("Y coordinate")
plt.title("Distribution of data points")
plt.show()
'''

#Split the data into train, validation and test sets
train_data, train_targets,\
  validation_data, validation_targets, test_data, test_targets = h.split_data(inputs, targets, 0.7, 0.1, 0.2)

#Data normalization
mean, std = inputs.mean(), inputs.std()

train_data.sub_(mean).div_(std)
validation_data.sub_(mean).div_(std)
test_data.sub_(mean).div_(std)

#Instantiate the model

Input_Units = 2
Output_Units = 2
Hidden_Units = 25

model = m.Sequential(m.Linear(Input_Units,Hidden_Units),
                     m.ReLU(),
                     m.Linear(Hidden_Units,Hidden_Units),
                     m.ReLU(),
                     m.Linear(Hidden_Units,Hidden_Units),
                     m.Tanh(),
                     m.Linear(Hidden_Units,Output_Units),
                     m.Tanh()
                     )

#Instantiate the optimizer
lr = 0.00095
sgd = m.SGD(params = model.param(), lr = lr)

#Train the model
EPOCHS = 150

model, train_error, validation_error = h.train_model(train_data, train_targets,\
                                        validation_data, validation_targets, model, sgd, nb_epochs = EPOCHS)

'''
#Plot both train and validation errors wrt the number of epochs

fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot(111)
ax.set_title('Evolution of the training and validation errors w.r.t the epoch number.')
plt.plot(validation_error,color='red')
plt.plot(train_error,color='blue')
plt.legend(['Training Error', 'Validation Error'])
ax.set_xlabel('Epochs')
ax.set_ylabel(' % of Error')
#plt.savefig('Error_results.png')
plt.grid()
plt.show()
'''

h.test_model(model, test_data, test_targets)



