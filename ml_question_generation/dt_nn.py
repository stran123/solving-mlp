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
    for x in range(44, 69):
        for r in range(23, 33):
            for lp in range(1, 11):
                # print(x, r, lp)
                # print(math.log(lp/(x-r), 2))
                # print(math.log((x-r-lp)/(x-r), 2))
                answer = (-lp/(x-r))*math.log(lp/(x-r), 2)+(-(x-r-lp)/(x-r))*math.log((x-r-lp)/(x-r), 2)
                #make sure there are no spaces in the formula
                formula = "(0-{lp}/({x}-{r}))*(({lp}/({x}-{r}))l2)+(0-({x}-{r}-{lp})/({x}-{r}))*((({x}-{r}-{lp})/({x}-{r}))l2)"
                formula = formula.format(x = x, r = r, lp = lp)
                question = "Consider a 1D classification line on a 2D plane. There is a total of {x} points, {r} of which are on the right and the rest on the left of the boundary. {lp} points on the left are classified positive. What is the entropy of the left region?"
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