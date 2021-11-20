#!/usr/bin/env python3

import os,statistics

def generate_question(title, answers, prefix):
	print(f"<h1>{title}</h1><br>")
	c = 0
	for i in answers:
		print(f"<input type='radio' id='{prefix}-{c}' name='{prefix}' value='{c}' required><label for='{prefix}-{c}'>{i}</label>")
		c = c + 1
	print("<hr>")

def find_param(pname):
	c = os.getenv("QUERY_STRING")
	s = c.find(f"{pname}=")
	if s == -1:
		return
	s += 1 + len(pname)
	e = c.find("&",s)
	if e == -1:
		return c[s:]
	else:
		return c[s:e]

def generate_histogram(title,datas,choices):
	c = {}
	print(f"<h1>{title}</h1><br>")
	ctr = 0
	for i in choices:
		c[str(ctr)] = 0
		ctr += 1
	for i in datas:
		c[str(i)] += 1
	print("<table border='1'><tr><th>Answer</th><th>%</th><th>Graph</th></tr>")
	for k,v in c.items():
		r = v / len(datas)
		g = "#" * int(r * 20)
		#g += "X" * (20 - len(g))
		print("<tr><td>%s</td><td>%.3f%%</td><td>%s</td></tr>" % (choices[int(k)],(r * 100),g))
	print("</table><br>")
	s = 0
	try:
		s = statistics.stdev(datas)
	except:
		pass
	print("Data count: %d Data shapeness: %.3f (less value, less sharper)<hr>" % (len(datas),s))

Q1_choice = ("Sour","Sweet","Bitter","Spicy")
Q2_choice = ("Yes","No")
Q3_choice = ["Below 999,999 km <sup>2</sup>"]
for i in range(1,10):
	Q3_choice.append(f"From {i},000,000 to {i},999,999 km <sup>2</sup>")
Q3_choice.append("Over 10,000,000 km<sup>2</sup>")
Q1 = "How apple tastes like?"
Q2 = "Is america big?"
Q3 = "How big is america?"

print("""Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>How answer distributes?</title>
</head>
<body>
""")

if os.getenv("QUERY_STRING") != "":
	q1_ans = find_param("Q1")
	q2_ans = find_param("Q2")
	q3_ans = find_param("Q3")
	if q1_ans != None and q2_ans != None and q3_ans != None:
		try:
			q1_ans = int(q1_ans)
			q2_ans = int(q2_ans)
			q3_ans = int(q3_ans)
			if q1_ans >= 0 and q2_ans >= 0 and q3_ans >= 0 and q1_ans < len(Q1_choice) and q2_ans < len(Q2_choice) and q3_ans <= len(Q3_choice):
				f = open("../questions_result","a")
				f.write(f"{q1_ans},{q2_ans},{q3_ans}\n")
				f.close()
		except:
			pass

print("<form action='/' method='get'>")
generate_question(Q1, Q1_choice,"Q1")
generate_question(Q2, Q2_choice,"Q2")
generate_question(Q3, Q3_choice,"Q3")
print("<button>Submit your answer</button></form>")
print("<h1>Thanks for your answer!</h1><br>")
print("This is what happens to answer distribution:<hr>")
answer_q0 = []
answer_q1 = []
answer_q2 = []
try:
	for i in open("../questions_result"):
		if i != "":
			c = i.strip().split(",")
			answer_q0.append(int(c[0]))
			answer_q1.append(int(c[1]))
			answer_q2.append(int(c[2]))
	generate_histogram(Q1,answer_q0,Q1_choice);
	generate_histogram(Q2,answer_q1,Q2_choice);
	generate_histogram(Q3,answer_q2,Q3_choice);
except:
	print("No records yet")

print("""
</body>
</html>
""")
