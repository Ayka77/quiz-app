import tkinter as tk
import csv
import random

# Fragen laden
def load_questions(filename):
	questions = []
	
	with open(filename, newline='', encoding='utf-8') as file:
		reader = csv.reader(file, delimiter=',', skipinitialspace=True)
		
		next(reader, None)
		
		for i, row in enumerate(reader):
			print(f"Zeile {i}: {row}")
			
			# Falls alles in einer Spalte gelandet ist → manuell splitten
			if len(row) == 1:
				row = row[0].split('","')
			if len(row) < 2:
				print(f" Überspringe ungültige Zeile: {row}")
				continue
			
			# Anführungszeichen entfernen
			q = row[0].strip().strip('"')
			a = row[1].strip().strip('"')
			
			questions.append({"q": q, "a": a})
			
	return questions
    

questions = load_questions("fragen.csv")
current = None


def new_question():
	global current
	current = random.choice(questions)
	label.config(text=current["q"])
	entry.delete(0, tk.END)
	result.config(text="")

def check():
	user_answer = entry.get().strip().lower()
	correct_answer = current["a"].strip().lower()
	
	if user_answer == correct_answer:
		result.config(text="Richtig!", fg="green")
	else:
		result.config(text=f"Falsch! Richtige Antwort: {current['a']}", fg="red")

# GUI
root = tk.Tk()
root.title("Quiz App")

label = tk.Label(root, text="", wraplength=400, justify="left")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack()

btn_check = tk.Button(root, text="Antwort prüfen", command=check)
btn_check.pack(pady=5)

btn_next = tk.Button(root, text="Nächste Frage", command=new_question)
btn_next.pack(pady=5)

result = tk.Label(root, text="")
result.pack(pady=10)

# erste Frage laden
new_question()

root.mainloop()
