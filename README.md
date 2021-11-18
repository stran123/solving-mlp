# Solving Machine Learning Problems

_Sunny Tran, Pranav Krishna, Ishan Pakuwal, Prabhakar Kafle, Nikhil Singh, Jayson Lynch, and Iddo Drori_

[Project Page](https://stran123.github.io/solving-mlp/)

Repository containing the code and dataset for Solving Machine Learning Problems [[arXiv]](https://arxiv.org/abs/2107.01238), presented at ACML 2021. Our work presents a dataset curated from MIT's Introduction to Machine Learning course (6.036) and trains a machine learning model to learn machine learning concepts from the course.

## Requirements

- transformers
- dgl
- torchvision
- sentencepiece==0.1.91

## Code Navigation

### ml_question_generation/

Contains files which generates the dataset. To generate the dataset, run:
```
python ml_question_generation/generate_questions.py
```

### data/

Contains the data for training the model. 

`train-cleaned.json`: contains the dataset in `.json` format.

`question-to-topic-cleaned.json` contains a mapping from each question to its topic from the course. 

### ml_model_trainer.ipynb

Contains the code for training the model. This trains on the data located at `data/train-cleaned.json`. Trained models are saved in `models/`. 

The process to replicate the results in the paper can be found in this notebook.


## BibTeX

```
@inproceedings{tran2021solving,
    title={Solving Machine Learning Problems}, 
    author={Tran, Sunny and Krishna, Pranav and Pakuwal, Ishan and Kafle, Prabhakar and Singh, Nikhil and Lynch, Jayson and Drori, Iddo},
    booktitle={Proceedings of the 13th Asian Conference on Machine Learning},
    month={November},
    year={2021}
  }
```
