import json
import numpy as np
import math


#opening the json file
f = open('train.json')


#return JSON object as a dictionary 
data = json.load(f)

#Each data item is of the form
#['expression', 'quant_cell_positions', 'processed_question', 'raw_question', 'is_quadratic', 'Id', 'Expected']

print([k for k in data[0]])

# print(data[0])

#Questions

question = "What is the updated Q value of a tuple (s, a) if q is 3, the a is 0.8, and t is 8?"

question = "A classifier has a decision boundary where theta is ( 1 3 ) . What value does it classify p , where p is ( 2 negative 4 ) ?'"

#We obtain prefix_list for a question from ml_model_trainer

#Prefix list for Q value question
prefix_list = ['+', '3', '*', '0.8', '-', '8', '3']
# prefix_list = ['*', '+', '3', '4', '/', '7', '6']

#Prefix List for the last classifier question
prefix_list = ['+', '*', '1.0', '2.0', '*', '3.0', '-', '0', '4.0']

# ['(', (0, 2), '*', '(', (0, 2), '+', (1,), ')', ')']
eliminate_words = ["what", "the", "also", "where", "let", "also", "and", "for", "if", "we", ".", "does", "it", "has"]

def process_question(question):
	if question[-1] == "." or question[-1] == "?":
		question = question[:-1]
	split_question = [s.lower() for s in question.split(" ")]
	split_question = [s for s in split_question if s not in eliminate_words]

	print(split_question)
	return split_question

def quant_position(split_question):
	quant_index = []
	quant_num = []
	for i in range(len(split_question)):
		q = split_question[i]
		if len(q) > 1 and q[-1] == ",":
			q = q[:-1]
		try:
			num = float(q)
			if isinstance(num, float) or isinstance(num, int):
				quant_index.append(i)
				quant_num.append(num)
		except:
			pass
	return quant_index, quant_num

processed_question = process_question(question)
print(quant_position(processed_question))



def check_num(s):
	try: 
		a = float(s)
		return True
	except:
		return False


def priority_equation(question):
	processed_question = process_question(question)
	quant_index, quant_num = quant_position(processed_question)
	variables_dict = {}
	num_to_variables = {}
	print(quant_index, quant_num)
	variable_used = [-1]*len(processed_question)

	for i in range(len(quant_index)):
		q_idx = quant_index[i]
		left_idx = q_idx - 1
		right_idx = q_idx
		key_words = ["=", "be", "is"]
		neglect_words = ["=", "be", "is", "(", ")", ".", "?", ",", "negative"]
		if left_idx > 1 and processed_question[left_idx] in key_words:
			variable = processed_question[left_idx-1]
			variables_dict[variable] = quant_num[i]
			if quant_num[i] not in num_to_variables:
				num_to_variables[quant_num[i]] = [variable]
			else:
				num_to_variables[quant_num[i]].append(variable)
		elif left_idx > 1 and processed_question[left_idx] == "(":
			temp_idx = left_idx
			while processed_question[temp_idx] in neglect_words and temp_idx > 0:
				temp_idx -= 1
			if temp_idx >= 0:
				print(processed_question[temp_idx])
				variable_used[temp_idx] += 1
				variable = processed_question[temp_idx] + str(variable_used[temp_idx])
				variables_dict[variable] = quant_num[i]
				if quant_num[i] not in num_to_variables:
					num_to_variables[quant_num[i]] = [variable]
				else:
					num_to_variables[quant_num[i]].append(variable)

		elif left_idx > 1 and (check_num(processed_question[left_idx]) or processed_question[left_idx] == 'negative'):
			# print("Now", processed_question[q_idx])
			temp_idx = left_idx
			while processed_question[temp_idx] in neglect_words or check_num(processed_question[temp_idx]):
				temp_idx -= 1
			if temp_idx >= 0:
				# print(processed_question[temp_idx])
				variable_used[temp_idx] += 1
				# print("this is temp", processed_question[temp_idx])
				variable = processed_question[temp_idx] + str(variable_used[temp_idx])
				# print("this is variable", variable)
				variables_dict[variable] = quant_num[i]
				if quant_num[i] not in num_to_variables:
					num_to_variables[quant_num[i]] = [variable]
				else:
					num_to_variables[quant_num[i]].append(variable)






	print(num_to_variables)
	print(variables_dict)
	return variables_dict, num_to_variables




def get_variable_expression(question, prefix_list):
	hint_list = []
	variables_dict, num_to_variables = priority_equation(question)
	operators = {'+': np.add, '-': np.subtract, '*': np.multiply, '/': np.divide, 'm': max, 'l':math.log, '^': np.power}
	# operator = {'+': '+', '*': '*', '/': '/', 'm': 'max', 'l':'log'}
	new_variables = []
	# print("This is prefix_list", prefix_list)
	print("---------------")
	print("Expression Hints")

	def help(index):
		if index == len(prefix_list):
			return np.nan, index
		if prefix_list[index] not in operators:
			return float(prefix_list[index]), index + 1
		operation = operators[prefix_list[index]]
		op1, end = help(index+1)
		op2, end = help(end)
		if prefix_list[index] in  ['+', '-', '*', '/', '^', 'm', 'l']:
			if check_num(op1) == False and check_num(op2) == False:
				s = op1 + prefix_list[index] + op2
			elif check_num(op1) == True and check_num(op2) == False:
				try: 
					s = "(" + num_to_variables[op1][0] + prefix_list[index] + op2 + ")"
				except:
					s = "(" + "x " +  prefix_list[index] + op2 + ")"
			elif check_num(op1) == False and check_num(op2) == True:
				try: 
					s = "(" + op1 + prefix_list[index] + num_to_variables[op2][0] +")"
				except:
					s = "(" + op2 +  prefix_list[index] + "y" + ")"
			else:
				op1_list = [op1]
				op2_list = [op2]
				# print("here", op1)
				if op1 in num_to_variables and op2 in num_to_variables:
					s = "(" + num_to_variables[op1][0] + prefix_list[index] + num_to_variables[op2][0] + ")"
				elif op1 not in num_to_variables and op2 in num_to_variables:
					s =  "(" + str(op1_list[0]) + prefix_list[index] + str(num_to_variables[op2][0]) + ")"
				elif op1 in num_to_variables and op2 not in num_to_variables:
					s = "(" + str(num_to_variables[op1][0]) + prefix_list[index] + str(op2) + ")"
				else:
					s = "(" + "x" +  prefix_list[index] + "y" + ")"
				# try: 
				# 	s = "(" + num_to_variables[op1][0] + prefix_list[index] + num_to_variables[op2][0] + ")"
				# except:
				# 	s = "(" + "x" +  prefix_list[index] + "y" + ")"
			print(s)
			hint_list.append(s)
		return s, end

	final_equation, end = help(0)
	print(final_equation)

	return hint_list



def evaluate_expression(prefix_list):
	hint_list = []
	operators = {'+': np.add, '-': np.subtract, '*': np.multiply, '/': np.divide, 'm': max, 'l':math.log, '^': np.power}
	def help(index):
		if index == len(prefix_list):
			return np.nan, index
		if prefix_list[index] not in operators:
			return float(prefix_list[index]), index + 1
		operation = operators[prefix_list[index]]
		op1, end = help(index+1)
		op2, end = help(end)

		if prefix_list[index] in  ['+', '-', '*', '/', '^', 'm', 'l']:
			print(op1, prefix_list[index], op2, '=', operation(op1, op2))
			# hint_list.append(operation(op1, op2))


		return operation(op1, op2), end

	final_equation, end = help(0)
	print(final_equation)
	# print("This is final hint_list", hint_list)
	return final_equation


def get_hints(question, prefix_list):
	hint_variables = get_variable_expression(question, prefix_list)
	print("Value Hints")
	hint_numbers = evaluate_expression(evaluate_expression(prefix_list))
	# print(hint_numbers)
	# print(len(hint_variables), len(hint_numbers))
	# for i in range()
	# for i in range(len(hint_variables)):
	# 	s = hint_variables[i] + "=" + hint_numbers[i]
	# 	print(s)


evaluate_expression(prefix_list)
priority_equation(question)
get_variable_expression(question, prefix_list)








