from utils import *
import paraphraser
import random

"""
Question: An image I has length {len_I} and filter F has length {len_F} , what is the length of the result of applying F to I ?
Expression: {len_I}-{len_F}+1

Question: Given a {n} by {n} image and {m} by {m} filter , what is the minimum amount of padding needed on each side of the image to keep the output the same size as the input ?
Expression: ({m}-1)/2

Question: Consider an image I of length {len_I} and filter F of length {len_F} . What is the length of the output if we have a stride length of {s} ?
Expression: ({len_I}-{len_F}+1)/{s}

Question: Given an image row [ {x} {y} {z} ] and filter [ {a} {b} {c} ] , what is the result from applying the filter to the image row such that they both align ?
Expression: {x}*{a}+{y}*{b}+{z}*{c}

Question: Given an image row [ {x} {y} {z} ] and filter [ {a} {b} {c} ] , what is the result from applying the filter to the image row after applying ReLU activation on the filter’s output ?
Expression: 0m({x}*{a}+{y}*{b}+{z}*{c})

Question: Now consider a zero-padded max pooling layer with {x} inputs , a pooling filter size of {f} and stride of {s} . How many total output units are there for this layer?
Expression: {x}/{s}
"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for len_I in range(5, 10):
        len_I = len_I * 10
        for len_F in range(3, 43, 2):
            answer = len_I-len_F+1

            #make sure there are no spaces in the formula
            formula = "{len_I}-{len_F}+1"
            formula = formula.format(len_I = len_I, len_F = len_F)
            questions = ["An image I has length {len_I} and filter F has length {len_F} , what is the length of the result of applying F to I ?",
                         "Given a 1D image I that is length {len_I} and a filter F that is length {len_F} , what is the length of the result from applying F to I ?",
                         "If filter F has length {len_F} and an image I has length {len_I} , what is the length of the result from applying F to I ?",
                         "What is the length of the result from applying F to I if F has length {len_F} and I has length {len_I}?",
                         "If an image has length {len_I} and filter has length {len_F} , compute the length of the output from applying the filter to the image ?"]
            for question in questions:
                question = question.format(len_I = len_I, len_F = len_F)

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

    for m in range(3, 43, 2):
        for n in range(5, 10):
            n = n * 10
            # for y1 in range(-2, 3):
            #     for y2 in range(-2, 3):
            answer = eval(f"({m}-1)/2")
            #make sure there are no spaces in the formula
            formula = "({m}-1)/2".format(m = format_exp(m))
            questions = ["Given a {n} by {n} image and {m} by {m} filter , what is the minimum amount of padding needed on each side of the image to keep the output the same size as the input ?",
                         "What is the minimum number of padding needed to maintain the same output size if the input image is {n} by {n} and the filter is {m} by {m} ?",
                         "If we have an image of size {n} by {n} and a filter of size {m} by {m} , how far out on each side should we pad to maintain the same output dimensions ?",
                         "Determine how many pixels of padding we need on the input of size {n} by {n} to ensure our filter {m} by {m} gives an output of the same size .",
                         "How much padding is needed on each side of a {n} by {n} input using a {m} by {m} filter to get an output the same size as the input ?"]
            for question in questions:
                question = question.format(m = format_num(m), n = format_num(n))
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

    for len_F in range(3, 23, 2):
        for len_I in range(50, 55):
            for s in [1, 2]:
            #     for y2 in range(-2, 3):
                answer = eval(f"({len_I}-{len_F}+1)/{s}")
                #make sure there are no spaces in the formula
                formula = "({len_I}-{len_F}+1)/{s}".format(len_I = format_exp(len_I), len_F = format_exp(len_F), s = format_exp(s))
                questions = ["Consider an image I of length {len_I} and filter F of length {len_F} . What is the length of the output if we have a stride length of {s} ?",
                             "Given an image of length {len_I} and a filter of length {len_F} , compute the output from applying the filter if we have a stride length of {s} ?",
                             "Using a stride length of {s} , what is the output from applying a filter of length {len_F} to an image of length {len_I} ?",
                             "What is the length of the output when we use an image of length {len_I} and a filter of length {len_F} if we use a stride length of {s} ?",
                             "Compute the output length given the stride {s} , image length {len_I} , and filter length {len_F} ."]
                for question in questions:
                    question = question.format(len_I = format_num(len_I), len_F = format_num(len_F), s = format_num(s))
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

    for x in [1]:
        for y in range(5):
            for z in range(2):
                for c in range(2):
                    for b in range(5):
                        a = int(random.random()*5)
                        answer = eval(f"{x}*{a}+{y}*{b}+{z}*{c}")
                        #make sure there are no spaces in the formula
                        formula = f"{x}*{a}+{y}*{b}+{z}*{c}"
                        questions = [f"Given an image row [ {x} {y} {z} ] and filter [ {a} {b} {c} ] , what is the result from applying the filter to the image row such that they both align ?",
                                     f"The row of an image  [ {x} {y} {z} ] has a filter [ {a} {b} {c} ] applied to it . What is the resulting value if they both align ?",
                                     f"Using the row of an image  [ {x} {y} {z} ] and a filter [ {a} {b} {c} ] , calculate the value of applying the filter on top of the image .",
                                     f"Compute the value returned from aligning the filter  [ {x} {y} {z} ] to the image  [ {x} {y} {z} ] on top of one another .",
                                     f"What is the value from applying a filter [ {a} {b} {c} ] directly on top of an image  [ {x} {y} {z} ] ?"]
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
        for y in [3]:
            for z in range(2):
                for c in range(2):
                    for b in range(5):
                        a = int(random.random()*5)
                        answer = eval(f"max(0, {x}*{a}+{y}*{b}+{z}*{c})")
                        #make sure there are no spaces in the formula
                        formula = f"0m({x}*{a}+{y}{b}+{z}{c})"
                        questions = [f"Given an image row [ {x} {y} {z} ] and filter [ {a} {b} {c} ] , what is the result from applying the filter to the image row after applying ReLU activation on the filter’s output ?",
                                     f"Using a row of an image [ {x} {y} {z} ] and filter [ {a} {b} {c} ] , calculate the value from applying the filter which has a ReLU on its output .",
                                     f"What is the result from applying a filter [ {a} {b} {c} ] to a row of an image [ {x} {y} {z} ] , where the filter has a ReLU activation on its output ?",
                                     f"Using a filter [ {a} {b} {c} ] with a ReLU on its output , compute the result from applying it right on top of the image  [ {x} {y} {z} ] .",
                                     f"Consider a filter [ {a} {b} {c} ] applied on an image [ {x} {y} {z} ] . What is the output if the filter has a ReLU activation ?"]
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

    for x in range(10, 30, 2):
        for f in range(1, 6):
            for s in [1, 2]:
                answer = eval(f"{x}/{s}")
                #make sure there are no spaces in the formula
                formula = f"{x}/{s}"
                questions = [f"Now consider a zero-padded max pooling layer with {x} inputs , a pooling filter size of {f} and stride of {s} . How many total output units are there for this layer?",
                             f"What is the total number of outputs for a zero-padded max pooling layer that has {x} inputs , a stride of {s} , and a pooling filter size of {f} ?",
                             f"Given that there are {x} inputs to a zero-padded max pooling layer and a stride length of {s} , compute the number of output units if we also know the pooling filter size of {f} ?",
                             f"A max pooling layer has {x} inputs, a pooling filter length of {f} , a stride length of {s} , and is zero-padded . Compute the number of output units for this layer .",
                             f"If we know the stride length of a max pooling layer , along with the filter length of {f} and input length of {x} , what is the number of outputs of this layer ?"]
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
    print("cnn.py: ", count)
    return train_data, test_data, test_answers

return_data(0, 0)