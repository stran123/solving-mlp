from utils import *
import paraphraser
import random
import json
import numpy as np

"""
Question: 1. Complete the function below to return a 2 x 2 numpy array containing any values you wish.
            2. Write the function below that returns the transpose of the 2-dimensional array provided.
            3. 
"""

question1 = [
    "Complete the function below to return a {}x{} numpy array containing any values you wish.",
    "The function below should generate a 2-dimensional numpy array of size {}x{}. Fill in the function."
]

test = """import numpy as np
    output = create_array()
    dims = output.shape
    assert len(dims)==2
    assert dims[0]={} and dims[1]={}"""

def make_questions1():
    train_questions = []
    for row in range(10):
        for column in range(10):
            if random.random() < 0.9:
                continue
            question = random.choice(question1).format(row, column)
            test_case = test.format(row, column)
            train_questions.append({
                'question': question,
                'args': [],
                'func_name': 'create_array',
                'test': test_case
            })
    
    # random.shuffle(train_questions)
    return train_questions

other_questions = [
    {
        'question': "Write a procedure that takes an array and returns the transpose of the array.",
        'test': """import numpy as np
            A=np.array([[1,2],[3,4]])
            expected = np.array([[1,3],[2,4]])
            output = transpose(A)
            assert output == expected
            """,
        'args': ['A'],
        'func_name': 'transpose'
    },
    {
        'question': "Write a procedure that takes a list of numbers and returns a 2D numpy array representing a row vector containing those numbers.",
        'test': """import numpy as np
            A=[1,2,3,4,5]
            expected = np.array([A])
            output = rv(A)
            assert output == expected
            """,
        'args': ['A'],
        'func_name': 'rv'
    },
    {
        'question': "Write a procedure that takes a list of numbers and returns a 2D numpy array representing a column vector containing those numbers.",
        'test': """import numpy as np
            A=[1,2,3,4,5]
            expected = np.array([A]).transpose()
            output = cv(A)
            assert output == expected
            """,
        'args': ['A'],
        'func_name': 'cv'
    },
    {
        'question': "Write a procedure that takes a 2D array and returns the final column as a two dimensional array.",
        'test': """import numpy as np
            A=np.array([[1,2,3,4], [2,3,4,5]])
            expected = np.array([[4],[5]])
            output = index_final_col(A)
            assert output == expected
            """,
        'args': ['A',],
        'func_name': 'index_final_col'
    }
]



def make_questions2():
    questions_list = []
    for question in other_questions:
        questions_list.append(question.copy())
        paraphrased_questions = paraphraser.paraphrase(question['question'])
        for q in paraphrased_questions:
            modified_q = {
                'question': q,
                'test': question['test'],
                'args': question['args'],
                'func_name': question['func_name']
            }
            questions_list.append(modified_q)

    return questions_list

def make_questions():
    questions = make_questions1()
    questions.extend(make_questions2())

    random.shuffle(questions)
    return questions

all_questions = make_questions()
print("total questions", len(all_questions))

with open('coding.json', 'w') as fp:
    json.dump(all_questions, fp)