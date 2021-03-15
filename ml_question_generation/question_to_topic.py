import json
false = False
true = True

with open("../data/train.json", 'r') as f:
    data = eval(f.read())
    print(len(data))
    for d in data:
        elt = d['processed_question']
        elt = elt.replace(",","")
        elt = elt.replace(".", "")
        elt = elt.replace(" ","")
        elt = elt.replace("negative", "")
        elt = elt.replace("-", "")
        for i in range(10):
            elt = elt.replace(str(i),"")
        print(elt)
        break
