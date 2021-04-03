from utils import *
import paraphraser
import random

"""
Question: How does a classifier with decision boundary theta classify a point p if theta is {theta} and p is {p}? # Note: would need to pass rsult through sign() function, but sign() is not possible with only +,-,*,/
Expression: {theta[0]}*{p[0]} + {theta[1]}*{p[1]}

Question: If the margin of the dataset with respect to a separator is {gamma} and the maximum magnitude of a point is {R}, what is the worst-case theoretical bound for the number of mistakes the perceptron algorithm would make?
Expression: ({R}*{gamma})^2

Question: Consider the classifier [ {x} {y} {z} {w} ] and [ {a} {b} {c} {d} ]. Do they represent the same hyperplane? Return 1 if true and another value if false.
Expression: (1-({x}-{a})*({x}+{a}))*(1-({y}-{b})*({y}+{b}))*(1-({z}-{c})*({z}+{c}))*(1-({w}-{d})*({w}+{d}))

Question: Consider the classifier [ {x} {y} {z} {w} ] and [ {a} {b} {c} {d} ]. Do they represent the same classifier? Return 1 if true and another value if false.
Expression: (1-({x}-{a}))*(1-({y}-{b}))*(1-({z}-{c}))*(1-({w}-{d}))
"""
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
                         "If the decision boundary of a classifier is theta , where theta is equal to ( {theta0} {theta1} ) , how does it classify point p , where p is equal to ( {p0} {p1} ) ?",
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

    for gamma in range(1, 26):
        for R in range(1, 21):
            answer = (R*gamma)**2
            #make sure there are no spaces in the formula
            formula = f"({R}*{gamma})^2"
            questions = [f"If the margin of the dataset with respect to a separator is {gamma} and the maximum magnitude of a point is {R} , what is the worst-case theoretical bound for the number of mistakes the perceptron algorithm would make ?",
                         f"Let {gamma} be the margin of the dataset with respect to the separator . Also let {R} be the maximum magnitude of a point from the dataset . Compute the maximum number of mistakes made by the perceptron algorithm .",
                         f"Calculate the maximum number of possible mistakes made by the perceptron algorithm if the margin of the separator is {gamma} and the maximum magnitude of a point is {R} .",
                         f"Given the largest magnitude of a point as {R} and the margin of the dataset be {gamma} from the separator , compute the most number of mistakes made by the perceptron algotithm .",
                         f"What is the most number of mistakes made by the perceptron algorithm if {R} is the maximum magnitude of a point in the dataset and the dataset has a margin of {gamma} to the separator ."]
            for question in questions:
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

    for x in range(5):
        for y in range(5):
            for z in range(2):
                for c in range(2):
                    for b in range(5):
                        a = int(random.random()*5)
                        answer = eval(f"(1-({x}-{a})*({x}+{a}))*(1-({y}-{b})*({y}+{b}))*(1-({z}-{c})*({z}+{c}))")
                        #make sure there are no spaces in the formula
                        formula = f"(1-({x}-{a})*({x}+{a}))*(1-({y}-{b})*({y}+{b}))*(1-({z}-{c})*({z}+{c}))"
                        questions = [f"Consider the classifier [ {x} {y} {z} ] and [ {a} {b} {c} ] . Do they represent the same hyperplane ? Return 1 if true and another value if false .",
                                     f"Given two classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] , determine if they are the same hyperplane. Return 1 if true and a different value if false .",
                                     f"If the classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] both represent the same hyperplane , return 1 . Otherwise , return anything else .",
                                     f"Do the two classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] represent the same hyperplane ? Return 1 if true and anythin else otherwise .",
                                     f"Determine if the following two classifiers represent the same hyperplane , [ {x} {y} {z} ] and [ {a} {b} {c} ] . If so , return 1 , and return anything else otherwise ."]
                        for question in questions:
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

    for x in range(5):
        for y in range(5):
            for z in range(2):
                for c in range(2):
                    for b in range(5):
                        a = int(random.random()*5)
                        answer = eval(f"(1-({x}-{a}))*(1-({y}-{b}))*(1-({z}-{c}))")
                        #make sure there are no spaces in the formula
                        formula = f"(1-({x}-{a}))*(1-({y}-{b}))*(1-({z}-{c}))"
                        questions = [f"Consider the classifier [ {x} {y} {z} ] and [ {a} {b} {c} ] . Do they represent the same classifier ? Return 1 if true and another value if false .",
                                     f"If we are given the classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] , can you determine if they represent the same classifier ? Return 1 if true and anything else if not .",
                                     f"Do the classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] represent the same classifier ? If so , return a 1 . If not, return anything but a 1 .",
                                     f"Given the classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] , determine if they are the same classifier . Return 1 if so and anything else if not .",
                                     f"If you are given two classifiers [ {x} {y} {z} ] and [ {a} {b} {c} ] , can you determine if they are the same classifier ? Return 1 if so and anything but a 1 if not ."]
                        for question in questions:
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


# return_data(0, 0)