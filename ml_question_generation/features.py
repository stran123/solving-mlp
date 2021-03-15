from utils import *
import paraphraser

"""
Question: What is the margin of a classifier with theta being ({theta}) and theta_0 being ({theta0}) on a point ({point}) with label {label}? # Note: to get margin of entire dataset, will need min function
Expression: {theta}*({point}-{theta0})*{label}

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta in [1, -1]:
        for theta0 in range(-12, 13, 1):
            for label in [1, -1]:
                for point in range(5):
                    answer = theta*(point-theta0)*label
                    #make sure there are no spaces in the formula
                    formula = "{theta}*({point}-{theta0})*{label}"
                    formula = formula.format(theta0 = format_exp(theta0), theta = format_exp(theta), point = format_exp(point), label = format_exp(label))
                    questions = ["What is the margin of a classifier with theta being {theta} and theta_0 being {theta0} on a point {point} with label {label}?",
                                 "If a point {point} with label {label} was classified by a classifier with theta {theta} and theta_0 {theta0}, what is the margin of this point?",
                                 "What is the margin on a point {point} with a label {label} if it is classified by a classifier with theta {theta} and theta_0 {theta0}?",
                                 "What is the size of the margin of a point {point} by a classifier with theta {theta} and theta_0 {theta0} if the point has label {label}?",
                                 "A point {point} has label {label}. Compute the margin of a classifier on this point. Let the theta of the classifier be {theta} and the theta_0 of the classifier be {theta0}."]
                    for question in questions:
                        question = question.format(theta0 = format_num(theta0), theta = format_num(theta), point = format_num(point), label = format_num(label))
                        
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
    print("features.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))