from utils import *
import paraphraser


"""
Question: Consider a very simple RNN, defined by the following equation:
            s_t = w*s_t-1 + x_t. Given s_0 = 0 and w=1 and x = [1,1,1],
            what is s_3?
Expression: w*s_t-1 + x_t (recursively)

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []

    for s0 in [0,1,2,3,1.5]:
        for w in [0, .5, 1, 1.5, .1]:
            for x in [[0.25, 0.5], [0, 3, 1], [2, 2, 0], [1, 0, 2], [1, 1, 1], [2, 1], [0, 1, 0], [9, 0, 5], [0.3, 3], [0, 1, 2], [3, 3], [0, 2, 0], [2, 2], [2, 0], [0, 0, 0], [9, 5], [2, 0, 1], [0, 0, 1], [3, 2], [1, 1, 0]]:
                ans = get_rnn_answer(s0, w, x)
                expression = get_rnn_expression(s0, w, x)
                len_x = len(x)
                questions = ["Consider a very simple RNN, defined by the following equation: s_t = w*s_t-1 + x_t. Given s_0 = {s0}, w = {w}, and x = {x}, what is s_{len_x}?",
                          "An RNN is defined as s_t = w*s_t-1 + x_t. If s_0 is {s0}, w is {w}, and x is {x}, what is s_{len_x}?",
                          "What is the RNN result s_{len_x} if s_0 is {s0}, w is {w}, and x is {x} if we let s_t = w*s_t-1 + x_t?",
                          "We define an RNN as s_t = w*s_t-1 + x_t. What is s_{len_x} if s_0 is {s0}, w is {w}, and x is {x}?",
                          "Let s_0 be {s0}, w be {w}, and x be {x}. Compute s_{len_x} if s_t is w*s_t-1 + x_t."]
                for question in questions:
                    question = question.format(len_x = len_x, s0 = s0, w = w, x = format_list(x))

                    if use_paraphraser:
                        paraphrased_questions = paraphraser.paraphrase(question) # up to 10 
                        for paraphrased_question in paraphrased_questions:
                            quant_cell_positions = get_quant_cells(paraphrased_question)
                            train_dict = {"expression": expression, "quant_cell_positions": quant_cell_positions, "processed_question": paraphrased_question, "raw_question": paraphrased_question, "is_quadratic": False, "Id": train_id, "Expected": answer}
                            train_data.append(train_dict)
                            train_id += 1
                            count += 1

                    quant_cells = get_quant_cells(question)
                    train_dict = {"expression": expression, "quant_cell_positions": quant_cells, "processed_question": question, "raw_question": question, "is_quadratic": False, "Id": train_id, "Expected": ans}
                    train_data.append(train_dict)
                    train_id += 1
                    count += 1
    print("rnn.py: ", count)
    return train_data, test_data, test_answers

# print(return_data(0, 0))
