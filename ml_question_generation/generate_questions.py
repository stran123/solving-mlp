import json
from tqdm import tqdm
import random
import basics as b # week 1
import perceptrons as p # week 2
import features as f # week 3
import logisticregression as lr # week 4
import regression as r # week 5
# import regression2_unused as r2 # week 5
import neuralnetwork_i as nn_i # week 6
import neuralnetwork_ii as nn_ii # week 7
import cnn as cnn # week 8
# import cnn2_unused as cnn2 # week 8
import rnn as rnn # week 9
import state_machine_mdp as sm_mdp # week 10
import reinforcement_learning as rl # week 11
import dt_nn as dtnn # week 12
# import clustering_unused as c # week 13


false = False
true = True
use_paraphraser = False

# modules = [b, p, p2, f, lg, r, r2, nn_i, nn_ii, cnn, cnn2, rnn, sm_mdp, rl, dtnn, c]
modules = [b, p, f, lr, r, nn_i, nn_ii, cnn, rnn, sm_mdp, rl, dtnn]
names = ['b', 'p', 'f', 'lr', 'r', 'nn_i', 'nn_ii', 'cnn', 'rnn', 'sm_mdp', 'rl', 'dtnn']
assert(len(modules) == len(names))

def get_and_update(mod, train_id, test_id, train_data, test_data, test_answers):
    train, test, answers = mod.return_data(train_id, test_id, use_paraphraser)
    return len(train_data + train), len(test_data + test), train_data + train, test_data+test, test_answers + answers

def get_question_to_topic_dict(mod, mod_string, question_to_topic=None):
    train, _, _ = mod.return_data(0, 0)
    if question_to_topic is None:
        question_to_topic = dict()
    for elt in train:
        elt = elt['processed_question']
        elt = elt.replace(",","")
        elt = elt.replace(".", "")
        elt = elt.replace(" ","")
        elt = elt.replace("negative", "")
        elt = elt.replace("-", "")
        for i in range(10):
            elt = elt.replace(str(i),"")
        question_to_topic[str(elt)] = mod_string
    return question_to_topic

def generate_data(destination):
    train_id = 0
    test_id = 0
    train_data = []
    test_data = []
    test_answers = []
    progress = 0
    for mod in tqdm(modules):
        progress += 1
        train_id, test_id, train_data, test_data, test_answers = get_and_update(mod, train_id, test_id, train_data, test_data, test_answers)
        print("Progress:", str(progress) + " / " + str(len(modules)))

    random.shuffle(train_data)
    with open("../data/" + destination, 'w') as outfile:
        json.dump(train_data, outfile)

def generate_topic_label_dict(destination):
    question_to_topic = dict()
    for mod,name in tqdm(zip(modules,names)):
        question_to_topic = get_question_to_topic_dict(mod, name, question_to_topic)
    with open("../data/" + destination, 'w') as outfile:
        json.dump(question_to_topic, outfile)

generate_data("train-cleaned.json")
generate_topic_label_dict("question-to-topic-cleaned.json")


