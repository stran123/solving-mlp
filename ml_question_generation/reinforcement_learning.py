from utils import *
import paraphraser

"""
Question: What is the updated Q value of a tuple (s, a) if q is {q}, the a is {a}, and t is {t}?
Expression: q+(a*(t-q))

Returns a train_data, test_data, and test_answers
Each is a list that contains dictionaries in the associated formats"""
def return_data(train_id, test_id, use_paraphraser=False):
    count = 0
    train_data = []
    test_data = []
    test_answers = []
    for q in range(10):
        for a in range(1, 11):
            a = a/10
            for t in range(2, 12, 2):
                answer = q+(a*(t-q))
                #make sure there are no spaces in the formula
                formula = "{q}+({a}*({t}-{q}))"
                formula = formula.format(q = q, a = a, t = t)
                questions = ["What is the updated Q value of a tuple (s, a) if q is {q}, the a is {a}, and t is {t}?",
                             "If q is {q}, what is its updated value after applying Q learning if a is {a} and t is {t}?",
                             "Let q = {q}. After Q learning, what is q if a is {a} and t is {t}?",
                             "If a is {a} and t is {t}, what is the Q learning value after applying one tuple (s, a) if q is {q}?",
                             "After applying Q learning to q = {q}, what is its value? Let the t be {t} and a be {a}."]
                for question in questions:
                    question = question.format(q = q, a = a, t = t)

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
    print("reinforcement_learning.py: ", count)
    return train_data, test_data, test_answers


# print(return_data(0, 0))