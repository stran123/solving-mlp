from utils import *
import paraphraser
import random

"""
Question: If f(theta) is {c1} times theta plus {c2} squared and theta is {theta} what is f(theta) ?
Expression: ({c1}*{theta}+{c2})*({c1}*{theta}+{c2})

Question: Given theta = {theta} and lambda = {lda} , compute the mean squared error with the data points [ ( {x1} {y1} )  and ( {x2} {y2} ) ] .
Expression: ({theta}*{x1} - {y1})+({lda}*{theta}*{theta})*({theta}*{x2} - {y2})+({lda}*{theta}*{theta})/2

Question: With lambda = {lambda} , the optimal theta is {theta} . If the data points are [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] , what is the value of y ? The optimal theta is computed by mean squared error .
Expression: 0-(({theta}*{x1}-{y1})*({theta}*{x1}-{y1})+{lambda}*{theta}*{theta}+({theta}*{x2}-{y2})*({theta}*{x2}-{y2}))^0.5+{theta}*{x3}
"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for theta in [1, 2]:
        for c1 in range(1, 11):
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

    for theta in range(5):
        for lda in [0.5, 1]:
            for x1 in [2]:
                for y1 in range(-2, 3):
                    for x2 in [1, 2]:
                        y2 = int(random.random()*5+1)
                        answer = eval(f"({theta}*{x1}-{y1})+({lda}*{theta}*{theta})*({theta}*{x2}-{y2})+({lda}*{theta}*{theta})/2")
                        #make sure there are no spaces in the formula
                        formula = "({theta}*{x1}-{y1})+({lda}*{theta}*{theta})*({theta}*{x2}-{y2})+({lda}*{theta}*{theta})/2".format(theta = format_exp(theta), lda = format_exp(lda), x1 = format_exp(x1), y1 = format_exp(y1), x2 = format_exp(x2), y2 = format_exp(y2))
                        questions = ["Given theta = {theta} and lda = {lda} , compute the mean squared error with the data points [ ( {x1} {y1} )  and ( {x2} {y2} ) ] .",
                                     "Given the points  [ ( {x1} {y1} )  and ( {x2} {y2} ) ] , what is the mean squared error if theta is {theta} and lda is {lda} ?",
                                     "Compute the mean squared error with the data points  [ ( {x1} {y1} )  and ( {x2} {y2} ) ] , theta = {theta} , and lda = {lda} .",
                                     "Using theta = {theta} and lda = {lda} , calculate the mean squared error of the points  [ ( {x1} {y1} )  and ( {x2} {y2} ) ] .",
                                     "If we let theta be {theta} and lda be {lda} , what is the mean squared error of the given points  [ ( {x1} {y1} )  and ( {x2} {y2} ) ] ?"]
                        for question in questions:
                            question = question.format(theta = format_num(theta), lda = format_num(lda), x1 = format_num(x1), y1 = format_num(y1), x2 = format_num(x2), y2 = format_num(y2))
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

    for theta in [1, 2]:
        for lda in [0.5, 1]:
            for y1 in range(-2, 3):
                for y2 in range(-2, 3):
                    answer = eval(f"0-(({theta}*0-{y1})*({theta}*0-{y1})+{lda}*{theta}*{theta}+({theta}*1-{y2})*({theta}*1-{y2}))**0.5+{theta}*2")
                    #make sure there are no spaces in the formula
                    formula = "0-(({theta}*0-{y1})*({theta}*0-{y1})+{lda}*{theta}*{theta}+({theta}*1-{y2})*({theta}*1-{y2}))^0.5+{theta}*2".format(theta = format_exp(theta), lda = format_exp(lda), y1 = format_exp(y1), y2 = format_exp(y2))
                    questions = ["With lambda = {lda} , the optimal theta is {theta} . If the datapoints are [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] , what is the value of y ? The optimal theta is computed by mean squared error .",
                                 "Let {theta} be the optimal theta by mean squared error. Given the datapoints [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] and lambda is {lda} , compute the value of y .",
                                 "The optimal theta value computed by mean squared error is {theta} using the datapoints [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] . If lambda is {lda} , what is y ?",
                                 "Given the dataset [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] , we get that the mean squared error for a theta = {theta} is minimal . What does y need to be if lambda is {lda} ?",
                                 "Calculate the value of y in the dataset [ ( 0 {y1} ) , ( 1 {y2} ) , ( 2 y ) ] if we know that the optimal theta {theta} used mean squared error . Let lambda be {lda} ."]
                    for question in questions:
                        question = question.format(theta = format_num(theta), lda = format_num(lda), y1 = format_num(y1), y2 = format_num(y2))
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