from utils import *
import paraphraser
import random
import itertools
"""
Question: What is the magnitude of the vector [x, y, z]?
Expression: ((x^2)+(y^2)+(z^2))^0.5

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    prev2d = 0
    xy_values = sorted([ _ for _ in itertools.product(range(int(2500**0.5)), range(int(2500**0.5)))], key=lambda x: x[0] + x[1], reverse=True)
    for x in range(1, 6):
        for y in range(6, 11):
            for z in range(0, 20):
                if not prev2d:
                    x, y = xy_values.pop()
                answer = {0: ((x**2)+(y**2))**0.5, 1: ((x**2)+(y**2)+(z**2))**0.5}[prev2d]
                #make sure there are no spaces in the formula
                formula = {0: f"(({x}^2)+({y}^2))^0.5", 1: f"(({x}^2)+({y}^2)+({z}^2))^0.5"}[prev2d]
                questions = {0: [f"What is the magnitude of the vector [ {x} {y} ] ?",
                             f"Let an input vector be [ {x} {y} ] . What is its magnitude ?",
                             f"If x = [ {x} {y} ] , what is || x || ?",
                             f"Compute the magnitude of [ {x} {y} ] .",
                             f"Find the Euclidian length of [ {x} {y} ] ."],
                             1: [f"What is the magnitude of the vector [ {x} {y} {z} ] ?",
                             f"Let an input vector be [ {x} {y} {z} ] . What is its magnitude ?",
                             f"If x = [ {x} {y} {z} ], what is || x || ?",
                             f"Compute the magnitude of [ {x} {y} {z} ] .",
                             f"Find the Euclidian length of [ {x} {y} {z} ] ."]}[prev2d]
                for question in questions:
                    if use_paraphraser:
                        paraphrased_questions = paraphraser.paraphrase(question) # up to 10 
                        for paraphrased_question in paraphrased_questions:
                            quant_cell_positions = get_quant_cells(paraphrased_question)
                            train_dict = {"expression": formula, "quant_cell_positions": quant_cell_positions, "processed_question": paraphrased_question, "raw_question": paraphrased_question, "is_quadratic": False, "Id": train_id, "Expected": answer}
                            train_data.append(train_dict)
                            train_id += 1
                            count += 1
                            
                    quant_cell_positions = get_quant_cells(question)
                    train_dict = {"expression": formula, "quant_cell_positions": quant_cell_positions, "processed_question": question, "raw_question": question, "is_quadratic": False, "Id": train_id, "Expected": answer}
                    train_data.append(train_dict)
                    train_id += 1
                    count += 1
                prev2d = 1 - prev2d
    print("basics.py: ", count)
    return train_data, test_data, test_answers