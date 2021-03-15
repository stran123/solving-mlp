from utils import *
import paraphraser

"""
Question: I has length {len_I} and F has length {len_F}
            what is the length of the result of applying F to I
Expression: {len_I}-{len_F}+1

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for i in [[1, 2, 3, 4, 5], [1, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0], [1, 1, 1], [  1, 0,   1], [0, 1,   1], [0,   1, 1,   1, 0], [0, 2, 3, 4], [  1,   1, 1,   1,   1]]:
        for f in [[0.25, 0.5], [0, 3, 1], [2, 2, 0], [1, 0, 2], [3], [1, 1, 1], [2], [2, 1], [0, 1, 0], [9, 0, 5], [0.3, 3], [0.5], [0, 1, 2], [3, 3], [0, 2, 0], [2, 2], [2, 0], [0, 0, 0], [0], [9, 5], [2, 0, 1], [0, 0, 1], [3, 2], [1, 1, 0], [0, 1, 1], [1, 2, 0], [7, 0.5, 0.5], [2, 0, 0], [1, 2, 1], [2, 0, 2], [2, 1, 1], [4], [1, 1], [0.1, 3], [1, 1, 2], [1, 2, 2], [2, 2, 2], [0.3, 0.2], [2, 1, 0], [2, 1, 2], [0, 2, 1], [1, 0, 1], [0.1, 2], [0.3, 2], [1], [1, 0, 0], [0, 1], [0, 2, 2], [2, 2, 1], [0, 0, 2]]:
            answer = len(i)-len(f)+1

            #make sure there are no spaces in the formula
            formula = "{len_I}-{len_F}+1"
            formula = formula.format(len_I = len(i), len_F = len(f))
            questions = ["I has length {len_I} and F has length {len_F}, what is the length of the result of applying F to I?",
                         "I is length {len_I} and F is length {len_F}. What is the length of the result from applying F to I?",
                         "If F has length {len_F} and I has length {len_I}, what is the length of the result from applying F to I?",
                         "What is the length of the result from applying F to I if F has length {len_F} and I has length {len_I}?",
                         "If I is length {len_I} and F is length {len_F}, compute the length of the output from applying F to I?"]
            for question in questions:
                question = question.format(I = format_list(i), F = format_list(f), len_I = len(i), len_F = len(f))

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
    print("cnn.py: ", count)
    return train_data, test_data, test_answers

# print(return_data(0, 0))