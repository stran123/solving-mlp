from utils import *
import paraphraser

"""
Question: A neural network has input x1 with weight w1 that goes into neuron A. Neuron A also has input oA that has weight wOA. 
          Neuron C inputs the output of neuron A with weight wAC. Neuron C has also has input oC that has weight wOC. 
          Neurons output the sum the products of each input with their respective weight. What is the output of neuron C 
          if x1 is {x1}, w1 is {w1}, oA is {oA}, wOA is {wOA}, wAC is {wAC}, oC is {oC}, and wOC is {wOC}?
Expression: wAC*((x1*w1)+(oA*wOA))+(oC*wOC)

Question: In a fully-connected feedforward network , how many weights ( including biases ) are there for one layer with {x} inputs and {y} outputs?
Expression: 2*{x}*{y}
"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    variables = {'x1': [0, 1, 2, 3, 4], 'w1': [1, 2], 'oA': [0.5], 'wOA': [0, 1, 2, 3, 4], 'wAC': [1], 'oC': [1, 2, 3, 4, 5], 'wOC': [2, 3]}
    prev2node = 0
    for x1 in variables['x1']:   
        for w1 in variables['w1']:
            for oA in variables['oA']:
                for wOA in variables['wOA']:
                    for wAC in variables['wAC']:
                        for oC in variables['oC']:
                            for wOC in variables['wOC']:
                                
                                answer = wAC*((x1*w1)+(oA*wOA))+(oC*wOC) if not prev2node else wAC*((x1*w1)+(oA*1))+wOC*((1*1)+(wOA*1))+oC

                                #make sure there are no spaces in the formula
                                formula = f"{wAC}*(({x1}*{w1})+({oA}*{wOA}))+({oC}*{wOC})" if not prev2node else f"{wAC}*(({x1}*{w1})+({oA}*1))+{wOC}*((1*1)+({wOA}*1))+{oC}"
                                # questions = ["A NN has inputs x1 with weight w1 and x2 with weight w2. x1 goes into neuron A with offset oA that has weight wOA. x2 has weight w2 and goes into neuron B with offset oB that has weight wOB. Neuron C has inputs from neuron A with weight wAC and neuron B with weight wBC and has offset oC that has weight wOC. Neurons output the sum the products of each input with their respective weight. What is the output of neuron C if x1 is {x1}, x2 is {x2}, w1 is {w1}, w2 is {w2}, oA is {oA}, oB is {oB}, wOA is {wOA}, wOB is {wOB}, wAC is {wAC}, wBC is {wBC}, oC is {oC}, and wOC is {wOC}?"]
                                questions = ["A neural network has input x1 with weight w1 that goes into neuron A . Neuron A also has input oA that has weight wOA . Neuron C inputs the output of neuron A with weight wAC . Neuron C has also has input oC that has weight wOC . What is the output of neuron C if x1 is {x1} , w1 is {w1} , oA is {oA} , wOA is {wOA} , wAC is {wAC} , oC is {oC} , and wOC is {wOC} ?", "Neuron A and Neuron C are the input and output neurons of a neural network . Neuron A takes in value x1 is {x1} with weight w1 being {w1} and offset value oA being {oA} with weight wOA being {wOA} . Neuron C takes in the output of neuron A with weight wAC being {wAC} and offset value oC being {oC} with weight wOC being {wOC} . What is the output of neuron C ?", "Neuron C is the output neuron and neuron A takes the input . Compute the output with the given architecture and inputs . Neuron C takes in the offset value oC being {oC} with weight wOC being {wOC} . Neuron C also takes in the output of neuron A with weight wAC being {wAC} . Neuron A takes in the input value x1 being {x1} with weight w1 being {w1} and offset value oA being {oA} and offset weight wOC being {wOC} .", "A neural network has an input neuron A and output neuron C . Neuron A takes in an offset value oA being {oA} , an offset weight wOA being {wOA} , and an input x1 being {x1} with weight w1 being {w1} . The output of neuron A is passed to neuron C , which takes it in with weight wAC being {wAC} . Neuron C also takes in offset value oC being {oC} and offset weight wOC being {wOC} . Find the output of the neural network .", "In a neural network , neuron A outputs the sum of x1 times w1 and oA times wOA and neuron C outputs the sum of the product between the input from neuron A and wAC and the product between oC and wOC . What is the output of neuron C if we are given that x1 is {x1} , w1 is {w1} , oA is {oA} , wOA is {wOA} , wAC is {wAC} , oC is {oC} , and wOC is {wOC} ?"] if not prev2node else ["A neural network has inputs x1 = {x1} with weight {w1} and x2 = {wOA} with weight 1 and offset value oA = {oA} . Neuron B inputs x2 with offset 1 . Neuron C takes in the output of neurons A and B with offsets wAC = {wAC} and wBC = {wOC} , respectively . Neuron C has offset value oC = {oC} . Compute the output .", "Compute the output of neuron C , which takes in outputs from neurons A with weight wAC = {wAC} and B with weight wBC = {wOC} and offset oC = {oC} . Neuron A takes in value x1 = {x1} with weight w1 = {w1} and offset value oA = {oA} . Neuron B takes in input x2 = {wOA} with an offset of 1 .", "Neuron A takes in value {x1} with weight {w1} and offset {oA} . Its output is passed into neuron C with weight {wAC} . Neuron B takes in value {wOA} with weight 1 and offset 1 . Its output is passed into neuron C with weight {wOC}. Neuron C has offset {oC} . Compute the output of this neural network .", "Neurons A and B take inputs {x1} and {wOA} with weights {w1} and 1 , respectively . Neuron A has offset {oA} and neuron B has offset 1 . Neuron C takes in the output of A and B with weights {wAC} and {wOC} , respectively , and with offset {oC} . What is the output ?", "Compute the output of neuron C which takes the output of neuron A with weight {wAC} and neuron B with weight {wOC} and offset {oC} . Neuron B has input {wOA} and offset 1 . Neuron A has input {x1} and offset {w1} with offset {oA} ."]
                                prev2node = 1 - prev2node
                                for question in questions:
                                    question = question.format(wAC=wAC, x1=x1, w1=w1, oA=oA, wOA=wOA, oC=oC, wOC=wOC)

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
    for x in range(1, 26):
        x = 10 * x
        for y in range(1, 21):
            y = 10 * y
            # for y1 in range(-2, 3):
            #     for y2 in range(-2, 3):
            answer = eval(f"2*{x}*{y}")
            #make sure there are no spaces in the formula
            formula = "2*{x}*{y}".format(x = format_exp(x), y = format_exp(y))
            questions = ["In a fully-connected feedforward network , how many weights ( including biases ) are there for one layer with {x} inputs and {y} outputs ?",
                         "In a neural network where it is fully-connected and feedforward , how many total weights are there if we include the biases ? We have {x} inputs and {y} outputs .",
                         "A fully-connected neural network has {y} outputs and {x} inputs . How many total weights are there including the biases ?",
                         "Given a feedforward neural network layer , compute the total number of weights including biases if we have {y} outputs and {x} inputs .",
                         "If we have a neural network layer with {x} inputs and {y} outputs , how many weights ( including biases ) are needed to describe each connection ?"]
            for question in questions:
                question = question.format(x = format_num(x), y = format_num(y))
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
    print("neuralnetwork_i.py: ", count)
    return train_data, test_data, test_answers

return_data(0, 0)