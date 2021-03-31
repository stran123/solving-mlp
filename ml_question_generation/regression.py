from utils import *
import paraphraser

"""
Question: if f(theta) = ({c1}*theta+{c2}) squared and theta = {theta_a}
            what is f(theta) ?
Expression: ({c1}*{theta}+{c2})*({c1}*{theta}+{c2})

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta in [1, 4, 6,  9.4, 3, 15.4, 0.5, 0.23, 0.1, 5]:
        for c1 in [3, 4, 7, 10, 0.3, 1, 2, 5, 6, 0.5]:
            for c2 in [19, 3, 5,  6, 8]:
                answer = (c1*theta+c2)*(c1*theta+c2)
                #make sure there are no spaces in the formula
                formula = "({c1}*{theta}+{c2})*({c1}*{theta}+{c2})"
                formula = formula.format(c1 = format_exp(c1), c2 = format_exp(c2), theta = format_exp(theta))
                questions = ["If f(theta) is {c1} times theta plus {c2} squared and theta is {theta} what is f(theta) ?",
                             "f(theta) is defined as {c1} times theta plus {c2} squared and theta is {theta} . What is f(theta) ?",
                             "f(theta) is the square of the sum of {c2} and the product of {c1} and theta , where theta is {theta} . What is f(theta) ?",
                             "What is f(theta) if f(theta) is theta times {c1} plus {c2} squared and theta is {theta} ?",
                             "If f(theta) is {c1} times theta plus {c2} squared , what is f(theta) when theta is {theta} ?"]
                for question in questions:
                    question = question.format(c1 = format_num(c1), c2 = format_num(c2), theta = format_num(theta))

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
    print("regression.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))