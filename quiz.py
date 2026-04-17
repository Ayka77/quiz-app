import random
import tkinter as tk 



questions = [
	{"q": "Hauptstadt von Deutschland?", "a": "Berlin"},
	{"q": "2+2=?", "a": "4"}
]


current = random.choice(questions)

def check():
	if entry.get().lower() == current["a"].lower():
		result.config(text="Richtig!")
	else:
		result.config(text="Falsch! Richtige Antwort: {current['a']}")


root = tk.Tk()
root.title("Quiz App")

label = tk.Label(root, text=current["q"])
label.pack()

entry = tk.Entry(root)
entry.pack()

btn = tk.Button(root, text="Antwort prüfen", command=check)
btn.pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()
