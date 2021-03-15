from utils import *
import paraphraser

"""
Question: A neural network has input x1 with weight w1 that goes into neuron A. Neuron A also has input oA that has weight wOA. 
          Neuron C inputs the output of neuron A with weight wAC. Neuron C has also has input oC that has weight wOC. 
          Neurons output the sum the products of each input with their respective weight. What is the output of neuron C 
          if s1 is {x1}, w1 is {w1}, oA is {oA}, wOA is {wOA}, wAC is {wAC}, oC is {oC}, and wOC is {wOC}?
Expression: wAC*((x1*w1)+(oA*wOA))+(oC*wOC)

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    # variables = {'x1': [0, 1, 2, 3, 4], 'x2': [0, 1, 2, 3, 4], 'w1': [1, 2, 3, 4, 5], 'w2': [2], 'oA': [2], 'wOA': [2], 'oB': [1], 'wOB': [0, 1, 2, 3, 4],
    #              'wAC': [2], 'wBC': [1, 2], 'oC': [2, 3], 'wOC': [1]}
    variables = {'x1': [0, 1, 2, 3, 4], 'w1': [1, 2], 'oA': [0.5], 'wOA': [0, 1, 2, 3, 4], 'wAC': [0, 1, 2, 3, 4], 'oC': [1, 2, 3, 4, 5], 'wOC': [2, 3]}

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

                                answer = wAC*((x1*w1)+(oA*wOA))+(oC*wOC)

                                #make sure there are no spaces in the formula
                                formula = "{wAC}*(({x1}*{w1})+({oA}*{wOA}))+({oC}*{wOC})"
                                formula = formula.format(wAC=wAC, x1=x1, w1=w1, oA=oA, wOA=wOA, oC=oC, wOC=wOC)
                                # questions = ["A NN has inputs x1 with weight w1 and x2 with weight w2. x1 goes into neuron A with offset oA that has weight wOA. x2 has weight w2 and goes into neuron B with offset oB that has weight wOB. Neuron C has inputs from neuron A with weight wAC and neuron B with weight wBC and has offset oC that has weight wOC. Neurons output the sum the products of each input with their respective weight. What is the output of neuron C if x1 is {x1}, x2 is {x2}, w1 is {w1}, w2 is {w2}, oA is {oA}, oB is {oB}, wOA is {wOA}, wOB is {wOB}, wAC is {wAC}, wBC is {wBC}, oC is {oC}, and wOC is {wOC}?"]
                                questions = ["A neural network has input x1 with weight w1 that goes into neuron A. Neuron A also has input oA that has weight wOA. Neuron C inputs the output of neuron A with weight wAC. Neuron C has also has input oC that has weight wOC. Neurons output the sum the products of each input with their respective weight. What is the output of neuron C if s1 is {x1}, w1 is {w1}, oA is {oA}, wOA is {wOA}, wAC is {wAC}, oC is {oC}, and wOC is {wOC}?"]
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
    print("neuralnetwork_i.py: ", count)
    return train_data, test_data, test_answers

# print(return_data(0, 0))