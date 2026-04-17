from flask import Flask, render_template, request, session, redirect, url_for
import csv
import random

app = Flask(__name__)
#app.secret_key = "geheim123"
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))



'''
def load_questions(filename):
	questions = []
	
	with open(filename, newline='', encoding='utf-8') as file:
		reader = csv.reader(file, delimiter='|', skipinitialspace=True)
		next(reader)
		
		for row in reader:
			if len(row) == 1:
				parts = row[0].split("|")
				if len(parts) >= 2:
					questions.append({"q": parts[0].strip(), "a": parts[1].strip()})
				elif len(row) >= 2:
					questions.append({"q": row[0].strip(), "a": row[1].strip()})
	return questions
	'''


# ✅ Fragen laden 	
def load_questions(filename):
    questions = []

    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|', skipinitialspace=True)
        next(reader, None)

        for row in reader:
            # ✅ Normalfall
            if len(row) >= 2:
                q = row[0].strip()
                a = row[1].strip()
                if q and a:
                    questions.append({"q": q, "a": a})
                else:
                    print("⚠️ Leere Werte:", row)

            # 🔧 Fallback (dein alter Trick)
            elif len(row) == 1:
                parts = row[0].split("|")
                if len(parts) >= 2:
                    questions.append({
                        "q": parts[0].strip(),
                        "a": parts[1].strip()
                    })
                else:
                    print("❌ Fehlerhafte Zeile:", row)

    print("✅ Geladene Fragen:", len(questions))
    return questions

questions = load_questions("fragen2.csv")




# ✅ Spiel starten
@app.route("/start", methods=["POST"])
def start():
    amount = int(request.form["amount"])
    
    max_available = len(questions)
    amount = min(amount, max_available)

    shuffled = questions.copy()
    random.shuffle(shuffled)

    selected = shuffled[:amount]

    session["remaining"] = selected
    session["total"] = len(selected)
    session["score"] = 0
    session["finished"] = False

    return redirect(url_for("home"))









# ✅ Startseite (Auswahl)
@app.route("/")
def home():	
	# 👉 Noch kein Spiel gestartet
	if "remaining" not in session:
		return render_template("start.html")
		
	# 👉 Fertig
	if session.get("finished"):
		return render_template(
			"done.html",
			score=session.get("score", 0),
			total=session.get("total", 0)
			)

	
	# 👉 WICHTIG: Schutz gegen leere Liste
	if not session["remaining"]:
		session["finished"] = True
		return redirect(url_for("home"))
	
	
	current = session["remaining"][0]
	
	progress = f"{session['total'] - len(session['remaining'])}/{session['total']}"
	percent = int((session['total'] - len(session['remaining'])) / session['total'] * 100)
	
	feedback = session.pop("feedback", None)
	correct_answer = session.pop("correct_answer", None)
	
	return render_template(
		"index.html",
		question=current["q"],
		progress=progress,
		percent=percent,
		score=session["score"],
		feedback=feedback,
		correct_answer=correct_answer
	)
	
	
	
	
	#if not session["remaining"]:
	#	return render_template("done.html", score=session["score"], total=session["total"])
	
	#if not remaining:
	#	return render_template(
	#	"done.html",
	#	score=session["score"],
	#	total=session["total"]
	#)
	
	if not remaining:
		session["finished"] = True
		return redirect(url_for("home"))
	
	
	current = session["remaining"][0]
	
	progress = f"{session['total'] - len(session['remaining'])}/{session['total']}"
	percent = int((session['total'] - len(session['remaining'])) / session['total'] * 100)
	
	return render_template(
		"index.html",
		question=current["q"],
		progress=progress,
		percent=percent,
		score=session["score"]
		 )







# Antwort prüfen
@app.route("/check", methods=["POST"])
def check():
	user_answer = request.form["antwort123"].strip().lower()
	
	remaining = session.get("remaining", [])
	
	if not remaining:
		session["finished"] = True
		return redirect(url_for("home"))
	
	current = remaining[0]
	correct_answer = current["a"].strip().lower()
	
	
	'''
	if user_answer == correct_answer:
		session["score"] += 1
		remaining.pop(0)
	
	else:
		# falsche Frage ans Ende
		remaining.append(remaining.pop(0))
		session["feedback"] = "wrong"
	'''
	
	# FALL 1: Zeit abgelaufen (keine Eingabe)
	if not user_answer:
		session["feedback"] = "timeout"
		session["correct_answer"] = correct_answer
		remaining.append(remaining.pop(0))
 
	# FALL 2: richtig
	elif user_answer == correct_answer:
		session["score"] += 1
		remaining.pop(0)
		session["feedback"] = "correct"
 
	# FALL 3: falsch
	else:
		session["feedback"] = "wrong"
		session["correct_answer"] = correct_answer
		remaining.append(remaining.pop(0))
 
	
	session["remaining"] = remaining
	
	if not remaining:
		session["finished"] = True
	
	return redirect(url_for("home"))







# ✅ Neustart
@app.route("/restart")
def restart():
	session.clear()
	return redirect(url_for("home"))




if __name__ == "__main__":
	#app.run(debug=True)
	app.run()
