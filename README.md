# Solving Machine Learning Problems

## ml_model_trainer.ipynb

Contains the code for training the model. This trains on the data located in `/data` and stores the model in `/models`.

## /data

Contains the data for training the model. Each `.json` file is split for testing (i.e. only a single `.json` file titled `train-cleaned.json` is needed for both training and testing) under each subdirectory of `/data`.

## /models

Stores the model corresponding to the name of the dataset used and the epoch the model was trained for. For a model trained from the dataset `/data/ml_data_12_topics` without using a pretrained T5 Transformer, its checkpoint for epoch 4 is stored in `/models/ml_data_12_topics/epoch-4.path`. The same dataset and epoch checkpoint using a pretrained T5 Transformer is located in `/models/ml_data_12_topics_t5/epoch-4.pth`.
