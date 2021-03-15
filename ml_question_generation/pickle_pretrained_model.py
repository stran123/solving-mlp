from transformers import T5ForConditionalGeneration,T5Tokenizer
import pickle

def save_model():
	model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_paraphraser')
	pickle.dump(model, open("pretrained_t5.pkl", 'wb'))

def load_model():
	return pickle.load(open("pretrained_t5.pkl", 'rb'))

if __name__ == "__main__":
	save_model()
	# load_model()