# Solving Machine Learning Problems

https://stran123.github.io/solving-mlp/

## Code Navigation

### ml_question_generation/

Contains files which generates the dataset. To generate the dataset, run:
```
python ml_question_generation/generate_questions.py
```

### data/

Contains the data for training the model. `question-to-topic-cleaned.json` contains a mapping from each question to its topic from the course. 

### ml_model_trainer.ipynb

Contains the code for training the model. This trains on the data located in `/data/train-cleaned.json`. Trained models are saved in `models/`. 


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