from utils import *
import paraphraser
import random

"""
Question: Let a state machine be described with the equations s_t = f(s_(t-1), x_t) and y_t = g(s_t), where x_t is the input. If s_0 is {s_0}, f(s_(t-1), x_t) = (s_(t-1))m(x_t), and g(s_t) = {c}*s_t, what is the output y_3 after the inputs [{x_1}, {x_2}, {x_3}]?
Expression: c*(max(max(max(s_0, x_1), x_2), x_3))

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    def get_solution(c, s_0, x):
        return c * max(s_0, *x)
    def get_formula(x):
        builder = "{s_0}m" + str(x[0])
        for d in range(1, len(x)):
            builder = "(" + builder + ")m" + str(x[d])
        return "{c}*(" + builder + ")"
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for _ in range(500):
        for c in range(5):
            seq_len = int(random.random()*4)+3
            x = [int(random.random()*20) for _ in range(seq_len)]
            s_0 = int(random.random()*20)
            answer = get_solution(c, s_0, x)
            #make sure there are no spaces in the formula
            formula = get_formula(x)
            formula = formula.format(c = c, s_0 = s_0, x = format_list(x))
            questions = ["Let a state machine be described with the equations s_t = f(s_(t-1), x_t) and y_t = g(s_t), where x_t is the input. If s_0 is {s_0} , f(s_(t-1), x_t) = max ( s_(t-1) , x_t ) , and g(s_t) = {c} * s_t , what is the output y_{len_x} after the inputs {x} ?", "If we have a state machine , defined as s_t = f(s_(t-1), x_t) and y_t = g(s_t) , where x_t is the input , what is the output y_{len_x} if we have s_0 being {s_0} , f(s_(t-1), x_t) = max ( s_(t-1) , x_t ) , g(s_t) = {c} * s_t , and we input {x} ?", "Consider the input x_t = {x} to a state machine with equations s_t = f(s_(t-1), x_t) and y_t = g(s_t) . Compute y_{len_x} if our initial conditions are s_0 is {s_0} , f(s_(t-1), x_t) = max ( s_(t-1) , x_t ) , and g(s_t) = {c} * s_t .", "A state machine is defined by the equations s_t = f(s_(t-1), x_t) and y_t = g(s_t) . Given the conditions s_0 = {s_0} , f(s_(t-1), x_t) = max ( s_(t-1) , x_t ) , and g(s_t) = {c} * s_t , compute y_{len_x} if the input is x_t = {x} .", "What is the output y_{len_x} of a state machine with equations s_t = f(s_(t-1), x_t) and y_t = g(s_t) , conditions s_0 = {s_0} , f(s_(t-1), x_t) = max ( s_(t-1) , x_t ) , and g(s_t) = {c} * s_t , and input x_t = {x} ?"]

            for question in questions:
                question = question.format(c = c, s_0 = s_0, x = format_list(x), len_x = len(x))

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