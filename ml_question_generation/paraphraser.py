import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer


def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(42)

model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_paraphraser')
# model = pickle.load(open("pretrained_t5", 'rb'))
tokenizer = T5Tokenizer.from_pretrained('t5-base')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print ("device ",device)
model = model.to(device)

def paraphrase(sentence, num_similar=10):
    # sentence = "If f(theta) is 3 times theta plus 19 squared and theta is 1 what is f(theta)?"
    text =  "paraphrase: " + sentence + " </s>"
    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

    # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=512,
        top_k=120,
        top_p=0.99,
        early_stopping=True,
        num_return_sequences=10
    )


    # print ("\nOriginal Question ::")
    # print (sentence)
    # print ("\n")
    # print ("Paraphrased Questions :: ")
    final_outputs =[]
    for beam_output in beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            final_outputs.append(sent)

    # for i, final_output in enumerate(final_outputs):
    #     print("{}: {}".format(i, final_output))
    return final_outputs[:num_similar]

# print(paraphrase("If f(theta) is 3 times theta plus 19 squared and theta is 1 what is f(theta)?"))
# print(paraphrase("If f(theta) is {c1} times theta plus {c2} squared and theta is {theta} what is f(theta)?"))
# print(paraphrase("How does a classifier with decision boundary theta classify a point p if theta is [0, 2] and p is [1, -4]?"))
# ['How do a classifier with decision boundary theta classify a point p because theta is [0, 2] and p is [1, -4]?', 'How does a classifier with decision boundary theta classify a point p? If theta is [0, 2]', 'What is the method by which a classifier with decision boundary theta classify a point if theta is [0, 2] and p is [1, -4]?', 'How does a classifier with decision boundary theta classify a point p if theta is [0, 2] and p is [1, 4]?', 'What happens if decision boundary theta classifies a point p if theta is [0, 2] and p is [1, -4]?', 'How does the decision boundary decision theta classify a point p, if theta is [0, 2] and p is [1, -4]?', 'How does a Classifier with decision boundary Theta classify the mark p if theta is [0, 2] and p is [1, -4]?']