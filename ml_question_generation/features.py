from utils import *
import paraphraser
import math

"""
Question: What is the margin of a classifier with theta being ({theta}) and theta_0 being ({theta0}) on a point ({point}) with label {label}? # Note: to get margin of entire dataset, will need min function
Expression: {theta}*({point}-{theta0})*{label}

Question: What is the result of applying the value {z} to the sigmoid function ? Let e be equal to 2.71828 .
Expression: 1/(1+2.71828^(0-{z}))

Question: What is the NLL loss for the single data point ( {x} {y} ) where theta is {theta} and theta_0 is {theta_0} ? Let the log be natural log .
Expression: {y}*((1/(1+2.71828^(0-({theta}*{x}+{theta_0}))))l2.71828) + (1-{y})*((1-(1/(1+2.71828^(0-({theta}*{x}+{theta_0})))))l2.71828)
"""
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
                    questions = ["What is the margin of a classifier with theta being {theta} and theta_0 being {theta0} on a point {point} with label {label} ?",
                                 "If a point {point} with label {label} was classified by a classifier with theta {theta} and theta_0 {theta0} , what is the margin of this point ?",
                                 "What is the margin on a point {point} with a label {label} if it is classified by a classifier with theta {theta} and theta_0 {theta0} ?",
                                 "What is the size of the margin of a point {point} by a classifier with theta {theta} and theta_0 {theta0} if the point has label {label} ?",
                                 "A point {point} has label {label} . Compute the margin of a classifier on this point . Let the theta of the classifier be {theta} and the theta_0 of the classifier be {theta0} ."]
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

    for z in range(-250, 250):
        # z = int(random.random()*10000)/10000
        answer = eval(f"1/(1+2.71828**(0-{z}))")
        #make sure there are no spaces in the formula
        formula = "1/(1+2.71828^(0-{z}))".format(z = format_exp(z))
        questions = ["What is the result of applying the value {z} to the sigmoid function ? Let e be equal to 2.71828 .",
                     "Assume e is equal to 2.71828 . What do you get from passing the value {z} into the sigmoid function ?",
                     "What does the sigmoid function return when  you pass into it {z} ? Hint: have e be 2.71828 .",
                     "Compute the output of the sigmoid function when we pass in {z} . Let e be equal to 2.71828 .",
                     "Given the input {z} , what is the output of the sigmoid function when we pass in the input ? Set e to be 2.71828 ."]
        for question in questions:
            question = question.format(z = format_num(z))
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
        for theta_0 in range(4):
            for x in range(-2, 3):
                for y in range(-2, 3):
                    answer = eval(f"{y}*math.log(1/(1+2.71828**(0-({theta}*{x}+{theta_0}))), 2.71828)+(1-{y})*math.log(1-(1/(1+2.71828**(0-({theta}*{x}+{theta_0})))), 2.71828)")
                    #make sure there are no spaces in the formula
                    formula = "{y}*((1/(1+2.71828^(0-({theta}*{x}+{theta_0}))))l2.71828)+(1-{y})*((1-(1/(1+2.71828^(0-({theta}*{x}+{theta_0})))))l2.71828)".format(theta = format_exp(theta), theta_0 = format_exp(theta_0), x = format_exp(x), y = format_exp(y))
                    questions = ["What is the NLL loss for the single data point ( {x} {y} ) where theta is {theta} and theta_0 is {theta_0} ? Let the log be natural log ( base is 2.71828 ) .",
                                 "What is the loss for the data point ( {x} {y} ) if we use NLL . Let theta be {theta} and theta_0 be {theta_0} . Also use natural log where the base is 2.71828 .",
                                 "Consider the point ( {x} {y} ) , the theta {theta} and the theta_0 {theta_0} . What is the NLL loss ? Use natural log , where the base is 2.71828 .",
                                 "Compute the loss from the datapoint ( {x} {y} ) using NLL and natural log , where the base is 2.71828 . Have theta be {theta} and theta_0 be {theta_0} .",
                                 "Given the values for theta as {theta} and theta_0 as {theta_0} , compute the NLL loss on the data point ( {x} {y} ) . Use log base e of 2.71828 for the log ."]
                    for question in questions:
                        question = question.format(theta = format_num(theta), theta_0 = format_num(theta_0), x = format_num(x), y = format_num(y))
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


return_data(0, 0)