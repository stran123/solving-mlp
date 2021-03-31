from utils import *
import paraphraser

"""
Question: How does a classifier with decision boundary theta classify a point p if theta is {theta} and p is {p}? # Note: would need to pass rsult through sign() function, but sign() is not possible with only +,-,*,/
Expression: {theta[0]}*{p[0]} + {theta[1]}*{p[1]}

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta in [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]:
        theta0, theta1 = theta
        for p in [[0, -4], [0, -3], [0, -2], [0, -1], [0, 0], [1, -4], [1, -3], [1, -2], [1, -1], [1, 0], [2, -4], [2, -3], [2, -2], [2, -1], [2, 0], [3, -4], [3, -3], [3, -2], [3, -1], [3, 0]]:
            p0, p1 = p
            answer = theta0*p0 + theta1*p1
            #make sure there are no spaces in the formula
            formula = "{theta0}*{p0}+{theta1}*{p1}"
            formula = formula.format(theta0 = format_exp(theta0), theta1 = format_exp(theta1), p0 = format_exp(p0), p1 = format_exp(p1))
            questions = ["How does a classifier with decision boundary theta classify a point p if theta is ( {theta0} {theta1} ) and p is ( {p0} {p1} ) ?",
                         "A classifier has a decision boundary where theta is ( {theta0} {theta1} ) . What value does it classify p , where p is ( {p0} {p1} ) ?",
                         "If the decision bounary of a classifier is theta , where theta is equal to ( {theta0} {theta1} ) , how does it classify point p , where p is equal to ( {p0} {p1} ) ?",
                         "A point p is classified by a classifier whose decision boundary is theta = ( {theta0} {theta1} ) . How does it classify p , where p is ( {p0} {p1} ) ?",
                         "If theta is the decision boundary for some classifier , how does the classifier classify a point p , where theta is ( {theta0} {theta1} ) and p is ( {p0} {p1} ) ?"]
            for question in questions:
                question = question.format(theta0 = format_num(theta0), theta1 = format_num(theta1), p0 = format_num(p0), p1 = format_num(p1))
                
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
    print("perceptrons.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))