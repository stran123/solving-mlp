from utils import *
import paraphraser
import math

"""
Question: Consider a 1D classification line on a 2D plane. There is a total of {x} points, 
          {r} of which are on the right and the rest on the left of the boundary. 
          {lp} points on the left are classified positive. What is the entropy of the left region? 
Expression: (-{lp}/({x}-{r})*lg({lp}/({x}-{r}))+(-({x}-{r}-{lp})/({x}-{r})*lg(({x}-{r}-{lp})/({x}-{r})))

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    right = True
    for x in range(44, 49):
        for r in range(23, 33):
            for lp in range(1, 11):
                answer = (-lp/(x-r))*math.log(lp/(x-r), 2)+(-(x-r-lp)/(x-r))*math.log((x-r-lp)/(x-r), 2)
                #make sure there are no spaces in the formula
                formula = "(0-{lp}/({x}-{r}))*(({lp}/({x}-{r}))l2)+(0-({x}-{r}-{lp})/({x}-{r}))*((({x}-{r}-{lp})/({x}-{r}))l2)" if right else "(0-{lp}/({r}))*(({lp}/({r}))l2)+(0-({r}-{lp})/({r}))*((({r}-{lp})/({r}))l2)"
                formula = formula.format(x = x, r = r, lp = lp)
                questions = ["Consider a 1D classification line on a 2D plane . There is a total of {x} points, {r} of which are on the right and the rest on the left of the boundary . {lp} points on the left are classified positive . What is the entropy of the left region ?","There are {x} points on a 2D plane , {r} on the right side of a line and the rest on the left . {lp} points on the left of the line are positive . What is the entropy of the left region ?", "Calculate the entropy of the left region of a 2D plane, split by a line . There are {lp} points on the left side that are positive , {r} points on the right side , and {x} points total .", "If there are {x} points on a 2D plane , {r} of them on the right side split by a line , and {lp} points on the left side that are positive , what is the entropy of the left region ?", "Given {x} points on a plane , {r} of them are on the right side of a line , and {lp} of them that are on the left side are positive . Compute the entropy of the left side ."] if right else ["Consider a plane of {x} points , {r} of which are on the left side . Of the points on the left , {lp} points are positive . Find the entropy of the left side .", "What is the entropy of the left side of a region containing {r} points where the plane has {x} points in total and {lp} points on the left are positive ?", "The left side of a region has {r} points . Of the {r} points , {lp} are classified as positive . What is the entropy of the left region if there are {x} points in total ?", "If a region has {r} points on the left and {x} points total . {lp} points that are on the left are positive. Compute the entropy .", "A left region has {lp} points classified as positive. There are {x} points in the plane , and {r} points on the left . Compute the entropy ."]
                right = not right
                for question in questions:
                    question = question.format(x = x, r = r, lp = lp)

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
    print("dt_nn.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))