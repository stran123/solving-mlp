from utils import *
import paraphraser

"""
Question: A neural network has input x1 with weight w1 that goes into neuron A. Neuron A also has input oA that has weight wOA. 
          Neuron C inputs the output of neuron A with weight wAC. Neuron C has also has input oC that has weight wOC. 
          Neuron C applies a ReLU on its output. Neurons output the sum the products of each input with their respective weight.
          What is the output of neuron C if x1 is {x1}, w1 is {w1}, oA is {oA}, wOA is {wOA}, wAC is {wAC}, oC is {oC}, and wOC is {wOC}?
Expression: 0m(wAC*((x1*w1)+(oA*wOA))+(oC*wOC))

Question: A neural network has inputs x1 = {x1} with weight {w1} and x2 = {wOA} with weight 1 and offset value oA = {oA} . Neuron B inputs x2 with offset 1 . Neuron C takes in the output of neurons A and B with offsets wAC = {wAC} and wBC = {wOC} , respectively . Neuron C has offset value oC = {oC} and applies an ReLU on its output . Compute the output .

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False, prev2node = 0):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    variables = {'x1': [-1], 'w1': [1, 2], 'oA': [0.5], 'wOA': [0, 1, 2, 3, 4], 'wAC': [1], 'oC': [1, 2, 3, 4, 5], 'wOC': [2, 3]}
    
    for x1 in variables['x1']:
        # for x2 in variables['x2']:    
        for w1 in variables['w1']:                          
                # for w2 in variables['w2']:
            for oA in variables['oA']:
                for wOA in variables['wOA']:
                            # for oB in variables['oB']:
                                # for wOB in variables['wOB']:
                    for wAC in variables['wAC']:
                                        # for wBC in variables['wBC']:
                        for oC in variables['oC']:
                            for wOC in variables['wOC']:

                                answer = max(0, wAC*((x1*w1)+(oA*wOA))+(oC*wOC)) if prev2node else max(0, wAC*((x1*w1)+(oA*1))+wOC*((1*1)+(wOA*1))+oC)

                                #make sure there are no spaces in the formula
                                formula = "0m({wAC}*(({x1}*{w1})+({oA}*{wOA}))+({oC}*{wOC}))" if prev2node else "0m({wAC}*(({x1}*{w1})+({oA}*1))+{wOC}*((1*1)+({wOA}*1))+{oC})"
                                formula = formula.format(wAC=format_exp(wAC), x1=format_exp(x1), w1=format_exp(w1), oA=format_exp(oA), wOA=format_exp(wOA), oC=format_exp(oC), wOC=format_exp(wOC))
                                # questions = ["A NN has inputs x1 with weight w1 and x2 with weight w2. x1 goes into neuron A with offset oA that has weight wOA. x2 has weight w2 and goes into neuron B with offset oB that has weight wOB. Neuron C has inputs from neuron A with weight wAC and neuron B with weight wBC and has offset oC that has weight wOC. Neurons output the sum the products of each input with their respective weight. What is the output of neuron C if x1 is {x1}, x2 is {x2}, w1 is {w1}, w2 is {w2}, oA is {oA}, oB is {oB}, wOA is {wOA}, wOB is {wOB}, wAC is {wAC}, wBC is {wBC}, oC is {oC}, and wOC is {wOC}?"]
                                questions = ["A neural network has input x1 with weight w1 that goes into neuron A . Neuron A also has input oA that has weight wOA . Neuron C inputs the output of neuron A with weight wAC . Neuron C has also has input oC that has weight wOC . Neuron C applies a ReLU on its output . What is the output of neuron C if x1 is {x1} , w1 is {w1} , oA is {oA} , wOA is {wOA} , wAC is {wAC} , oC is {oC} , and wOC is {wOC} ?", "Neuron A is the input neuron of a neural network . Neuron C is the output neuron of the same neural network and applies a ReLU function on its output . Neuron A takes in value x1 is {x1} with weight w1 being {w1} and offset value oA being {oA} with weight wOA being {wOA} . Neuron C takes in the output of neuron A with weight wAC being {wAC} and offset value oC being {oC} with weight wOC being {wOC} . What is the output ?", "Neuron C is the output neuron which applies a ReLU on its output and neuron A is the input neuron to a neural network . Compute the output of a neural network with the given architecture and inputs . Neuron C takes in the offset value oC being {oC} with weight wOC being {wOC} . Neuron C takes in the output of neuron A with weight wAC being {wAC} . Neuron A takes in the input value x1 being {x1} with weight w1 being {w1} and offset value oA being {oA} and offset weight wOA being {wOA} .", "Neuron A takes in an offset value oA being {oA} , an offset weight wOA being {wOA} , and an input x1 being {x1} with weight w1 being {w1} . The output of neuron A is passed to neuron C , which takes it in with weight wAC being {wAC} . Neuron C also takes in offset value oC being {oC} and offset weight wOC being {wOC} and applies a ReLU function. Find the output of the neural network .", "In a neural network , neuron A outputs the sum of x1 times w1 and oA times wOA and neuron C outputs the ReLU of the sum of the product between the input from neuron A and wAC and the product between oC and wOC . What is the output of neuron C if we are given that x1 is {x1} , w1 is {w1} , oA is {oA} , wOA is {wOA} , wAC is {wAC} , oC is {oC} , and wOC is {wOC} ?"] if prev2node else ["A neural network has inputs x1 = {x1} with weight {w1} and x2 = {wOA} with weight 1 and offset value oA = {oA} . Neuron B inputs x2 with offset 1 . Neuron C takes in the output of neurons A and B with offsets wAC = {wAC} and wBC = {wOC} , respectively . Neuron C has offset value oC = {oC} and applies an ReLU on its output . Compute the output .", "A ReLU is applied to the output of neuron C , which takes in outputs from neurons A with weight wAC = {wAC} and B with weight wBC = {wOC} and offset oC = {oC} . Neuron A takes in value x1 = {x1} with weight w1 = {w1} and offset value oA = {oA} . Neuron B takes in input x2 = {wOA} with an offset of 1 .", "Neuron A takes in value {x1} with weight {w1} and offset {oA} . Its output is passed into neuron C with weight {wAC} . Neuron B takes in value {wOA} with weight 1 and offset 1 . Its output is passed into neuron C with weight {wOC}. Neuron C has offset {oC} and a ReLU on its output . Compute the output of this neural network .", "Neurons A and B take inputs {x1} and {wOA} with weights {w1} and 1 , respectively . Neuron A has offset {oA} and neuron B has offset 1 . Neuron C takes in the output of A and B with weights {wAC} and {wOC} , respectively , and with offset {oC} . Neuron C also applies a ReLU on its output . What is the output ?", "Compute the ReLU output of neuron C which takes the output of neuron A with weight {wAC} and neuron B with weight {wOC} and offset {oC} . Neuron B has input {wOA} and offset 1 . Neuron A has input {x1} and offset {w1} with offset {oA} ."]
                                prev2node = 1 - prev2node
                                for question in questions:
                                    question = question.format(wAC=format_num(wAC), x1=format_num(x1), w1=format_num(w1), oA=format_num(oA), wOA=format_num(wOA), oC=format_num(oC), wOC=format_num(wOC))
                                    
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
    print("neuralnetwork_ii.py: ", count)
    if prev2node == 0:
        train_data2, test_data2, test_answers2 = return_data(0, 0, use_paraphraser, 1)
        return train_data+train_data2, test_data+test_data2, test_answers+test_answers2
    else:
        return train_data, test_data, test_answers

print(len(return_data(0, 0)[0]))