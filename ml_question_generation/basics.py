from utils import *
import paraphraser

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
    for x in range(1, 6):
        for y in range(6, 11):
            for z in range(0, 20):
                answer = ((x**2)+(y**2)+(z**2))**0.5
                #make sure there are no spaces in the formula
                formula = "(({x}^2)+({y}^2)+({z}^2))^0.5"
                formula = formula.format(x = x, y = y, z = z)
                questions = ["What is the magnitude of the vector [{x} {y} {z}]?",
                             "Let an input vector be [{x} {y} {z}]. What is its magnitude?",
                             "If x = [{x} {y} {z}], what is ||x||?",
                             "Compute the magnitude of [{x} {y} {z}].",
                             "Find the Euclidian length of [{x} {y} {z}]."]
                for question in questions:
                    question = question.format(x = x, y = y, z = z)

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
    print("basics.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))