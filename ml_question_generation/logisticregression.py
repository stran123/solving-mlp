from utils import *
import paraphraser


"""
Question: x = [1, 1], theta = [1, 0], theta_0 = -0.5 and y = 0.
            what is the value of theta * x + theta_0?
Expression: (({x_a}*{theta_a})+({x_b}*{theta_b}))+{theta_0}

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta_a, theta_b in [(1, -1), (0, 0), ( 1, 0), (0, 1), (1, -2), (0, -1), (-1, 0), (0, 2), (2, 0), (-2, 1)]:
        for theta_0 in [0.5, 0, 0.25, -1,  6, 6, 18, -3, 3, 2]:
            for x_a, x_b in [(1, -1), (0, 0), (1, 0), (0, -1), (-1, 0)]:
                answer = (x_a * theta_a + x_b * theta_b) + theta_0

                #make sure there are no spaces in the formula
                formula = "(({x_a}*{theta_a})+({x_b}*{theta_b}))+{theta_0}"
                formula = formula.format(x_a = format_exp(x_a), x_b = format_exp(x_b), theta_a = format_exp(theta_a), theta_b = format_exp(theta_b), theta_0 = format_exp(theta_0))

                questions = ["x is ({x_a}, {x_b}), theta is ({theta_a}, {theta_b}) and theta_0 is {theta_0}. What is the value of theta times x plus theta_0?",
                             "What is the value of theta times x plus theta_0 if x is ({x_a}, {x_b}), theta is ({theta_a}, {theta_b}), and theta_0 is {theta_0}?",
                             "Let theta be ({theta_a}, {theta_b}), theta_0 be {theta_0}, and x be ({x_a}, {x_b}). Compute theta times x plus theta_0.",
                             "What is the result of theta times x plus theta_0 if x is ({x_a}, {x_b}), theta is ({theta_a}, {theta_b}), and theta_0 is {theta_0}?",
                             "If we have x equals ({x_a}, {x_b}), theta equals ({theta_a}, {theta_b}), and theta_0 equals {theta_0}, then what is the result of theta times x plus theta_0?"]
                for question in questions:
                    question = question.format(x_a = format_num(x_a), x_b = format_num(x_b), theta_a = format_num(theta_a), theta_b = format_num(theta_b), theta_0 = format_num(theta_0))

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
    print("logisticregression.py: ", count)
    return train_data, test_data, test_answers
