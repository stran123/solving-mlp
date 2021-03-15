from utils import *
import paraphraser

"""
Question: f(theta) is ({c1} times theta plus {c2}) squared and
            theta is {theta} and eta is {eta} what is theta after gd ?
            HINT use 2 times {c1} times theta plus 2 times {c2}
Expression: {theta}-{eta}*2*{c1}*({c1}*{theta}+{c2})

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for eta in [0.1, 0.11, 0.56, 0.05, 0.2, 0.4, 1, 0.5, 0.01, 0.3]:
        for theta in [1, 4,  6, 9.4, 0.23]:
            for c1 in [3, 4, 7, 10, 0.3]:
                for c2 in [3,  5]:
                    answer = theta - eta*2*c1*(c1*theta+c2)
                    #make sure there are no spaces in the formula
                    formula = "{theta}-{eta}*2*{c1}*({c1}*{theta}+{c2})"
                    formula = formula.format(c1 = format_exp(c1), c2 = format_exp(c2), theta = format_exp(theta), eta = format_exp(eta))
                    questions = ["f(theta) is ({c1} times theta plus {c2}) squared and theta is {theta} and eta is {eta} what is theta after gd ? HINT use 2 times {c1} times theta plus 2 times {c2}.",
                                 "f(theta) is the square of ({c1} times {theta} plus {c2}), where theta is {theta} and eta is {eta}. What is theta after gd? Use 2 times {c1} times theta plus 2 times {c2}.",
                                 "Define f(theta) as the {c1} times theta plus {c2} squared. theta is {theta} and eta is {eta}. Use 2 times theta times {c1} plus 2 times {c2} to compute theta after gd.",
                                 "f(theta) is equal to theta times {c1} plus {c2} squared. Let theta be {theta} and eta be {eta}. What is theta after gd? Use 2 times {c1} times {theta} plus 2 times {c2}.",
                                 "f(theta) is theta times {c1} plus {c2} squared and etae is {eta} and theta is {theta}. What is theta after gd? HINT use theta times {c1} times 2 plus 2 times {c2}."]
                    for question in questions:
                        question = question.format(c1 = format_num(c1), c2 = format_num(c2), theta = format_num(theta), eta = format_num(eta))

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
    print("regression2.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))