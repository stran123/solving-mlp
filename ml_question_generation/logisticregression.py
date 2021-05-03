from utils import *
import paraphraser
import random

"""
Question: x = [1, 1], theta = [1, 0], theta_0 = -0.5 and y = 0 . What is the value of theta * x + theta_0 ?
Expression: (({x_a}*{theta_a})+({x_b}*{theta_b}))+{theta_0}

Question: Let a function f(theta) = ( {x} * theta + {y} ) ^ {pow} . For theta = {theta} and eta = {eta} , calculate theta after one gradient descent step .
Expression: {theta}-{eta}*{pow}*(({x}*{theta}+{y})^({pow}-1))*{x}

Question: Let a function f(theta) = ( {x} * theta + {y} ) ^ {pow} . For theta = {theta} and eta = {eta} , calculate f(theta) after one gradient descent update .
Expression: ({x}*({theta}-{eta}*{pow}*(({x}*{theta}+{y})^({pow}-1))*{x})+{y})^{pow}
"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta_a, theta_b in [(1, -1), (-2, 1)]:
        for theta_0 in [0.5, 0, 0.25, -1,  6, 6, 18, -3, 3, 2]:
            for x_a, x_b in [(1, -1), (0, 0), (1, 0), (0, -1), (-1, 0)]:
                answer = (x_a * theta_a + x_b * theta_b) + theta_0

                #make sure there are no spaces in the formula
                formula = "(({x_a}*{theta_a})+({x_b}*{theta_b}))+{theta_0}"
                formula = formula.format(x_a = format_exp(x_a), x_b = format_exp(x_b), theta_a = format_exp(theta_a), theta_b = format_exp(theta_b), theta_0 = format_exp(theta_0))

                questions = ["x is ( {x_a} {x_b} ) , theta is ( {theta_a} {theta_b} ) and theta_0 is {theta_0} . What is the value of theta times x plus theta_0?",
                             "What is the value of theta times x plus theta_0 if x is ( {x_a} {x_b} ), theta is ( {theta_a} {theta_b} ) , and theta_0 is {theta_0} ?",
                             "Let theta be ( {theta_a} {theta_b} ) , theta_0 be {theta_0}, and x be ( {x_a} , {x_b} ) . Compute theta times x plus theta_0 .",
                             "What is the result of theta times x plus theta_0 if x is ( {x_a} {x_b} ), theta is ( {theta_a} {theta_b} ) , and theta_0 is {theta_0} ?",
                             "If we have x equals ( {x_a} {x_b} ), theta equals ( {theta_a} {theta_b} ), and theta_0 equals {theta_0} , then what is the result of theta times x plus theta_0 ?"]
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

    for theta in range(5):
        for theta_0 in [1, 2]:
            for x in range(-2, 3):
                for y in [3]:
                    for eta in [0.01, 0.05]:
                        poww = int(random.random()*3+2)
                        answer = eval(f"{theta}-{eta}*{poww}*(({x}*{theta}+{y})**({poww}-1))*{x}")
                        #make sure there are no spaces in the formula
                        formula = "{theta}-{eta}*{poww}*(({x}*{theta}+{y})^({poww}-1))*{x}".format(theta = format_exp(theta), theta_0 = format_exp(theta_0), x = format_exp(x), y = format_exp(y), poww = poww, eta = eta)
                        questions = ["Let a function f(theta) = ( {x} * theta + {y} ) ^ {poww} . For theta = {theta} and eta = {eta} , calculate theta after one gradient descent step .",
                                     "Given a function ( {x} * theta + {y} ) ^ {poww} , compute theta after one gradient descent step if theta is {theta} and eta is {eta} .",
                                     "Calculate the updated theta after one gradient descent step if theta is {theta} , eta is {eta} , and the loss function is ( {x} * theta + {y} ) ^ {poww} .",
                                     "Given a loss function , ( {x} * theta + {y} ) ^ {poww} , for gradient descent , compute the updated theta value after one gradient descent step . Let theta be {theta} and eta be {eta} .",
                                     "If you let theta be {theta} and eta be {eta} , what is the updated theta value after one gradient descent step if the loss function is given by ( {x} * theta + {y} ) ^ {poww} ?"]
                        for question in questions:
                            question = question.format(theta = format_num(theta), theta_0 = format_num(theta_0), x = format_num(x), y = format_num(y), poww = poww, eta = eta)
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

    for theta in range(5):
        for theta_0 in [1, 2]:
            for x in [2]:
                for y in range(-2, 3):
                    for eta in [0.01, 0.05]:
                        poww = int(random.random()*3+2)
                        answer = eval(f"({x}*({theta}-{eta}*{poww}*(({x}*{theta}+{y})**({poww}-1))*{x})+{y})**{poww}")
                        #make sure there are no spaces in the formula
                        formula = "({x}*({theta}-{eta}*{poww}*(({x}*{theta}+{y})^({poww}-1))*{x})+{y})^{poww}".format(theta = format_exp(theta), theta_0 = format_exp(theta_0), x = format_exp(x), y = format_exp(y), poww = poww, eta = eta)
                        questions = ["Let a function f(theta) = ( {x} * theta + {y} ) ^ {poww} . For theta = {theta} and eta = {eta} , calculate f(theta) after one gradient descent update .",
                                     "Given a function ( {x} * theta + {y} ) ^ {poww} , calculate the value of the function after one gradient descent update if theta is {theta} and eta is {eta} .",
                                     "Calculate the value of the function ( {x} * theta + {y} ) ^ {poww} after updating the theta value in one step of gradient descent . Have theta be {theta} and eta be {eta} .",
                                     "The function ( {x} * theta + {y} ) ^ {poww} is the loss function when performing a gradient descent. Calculate the loss after one step of gradient descent. Let theta be {theta} and eta be {eta} .",
                                     "Given theta be {theta} and eta be {eta} , calculate the value of the function ( {x} * theta + {y} ) ^ {poww} after one step of gradient descent ."]
                        for question in questions:
                            question = question.format(theta = format_num(theta), theta_0 = format_num(theta_0), x = format_num(x), y = format_num(y), poww = poww, eta = eta)
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