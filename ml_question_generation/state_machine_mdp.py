from utils import *
import paraphraser

"""
Question: Let a state machine be described with the equations s_t = f(s_(t-1), x_t) and y_t = g(s_t), where x_t is the input. If s_0 is {s_0}, f(s_(t-1), x_t) = (s_(t-1))m(x_t), and g(s_t) = {c}*s_t, what is the output y_3 after the inputs [{x_1}, {x_2}, {x_3}]?
Expression: c*(max(max(max(s_0, x_1), x_2), x_3))

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for c in range(4):
        for x_1 in range(5, 10):
            for x_2 in range(4, 9):
                for x_3 in range(3, 8):
                    for s_0 in range(2, 7):
                        answer = c*(max(max(max(s_0, x_1), x_2), x_3))
                        #make sure there are no spaces in the formula
                        formula = "{c}*((({s_0}m{x_1})m{x_2})m{x_3})"
                        formula = formula.format(c = c, s_0 = s_0, x_1 = x_1, x_2 = x_2, x_3 = x_3)
                        question = "Let a state machine be described with the equations s_t = f(s_(t-1), x_t) and y_t = g(s_t), where x_t is the input. If s_0 is {s_0}, f(s_(t-1), x_t) = (s_(t-1))m(x_t), and g(s_t) = {c}*s_t, what is the output y_3 after the inputs [{x_1}, {x_2}, {x_3}]?"
                        question = question.format(c = c, s_0 = s_0, x_1 = x_1, x_2 = x_2, x_3 = x_3)

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
    print("state_machine_mdp.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))