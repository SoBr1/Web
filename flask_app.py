from flask import *
from random import shuffle
from db import get_next_question, get_max_question, get_vopros_by_id,get_all_quest

def index():
    session["N"]=0
    session["rt_ar"]=0
    session["counter"]=0
    return render_template("index.html",victoryni=get_all_quest())

def test():
    if request.method == "GET":
        if session["N"] == get_max_question(session["n"]):
            return final()
            
        next_question_id = get_next_question(session["n"],session["N"])
        vopros_data = get_vopros_by_id(next_question_id)

        vopros_id = vopros_data[0]
        vopros = vopros_data[1]
        right_answer = vopros_data[2]
        all_answers = [vopros_data[2],vopros_data[3],vopros_data[4]]
        shuffle(all_answers)

        session["N"] += 1
        return render_template("test.html", vopros = vopros,all_answers=all_answers,right_answer=right_answer)
    else:
        session["counter"] += 1
        if request.form.get("fresh") == request.form.get("right_answer"):
            session["rt_ar"] += 1
        
        return redirect("/test")

def final():
    return render_template("final.html", ball=session["rt_ar"], square=session["counter"])

N = 0

def setN():
    session["n"] = int(request.form.get("victorID"))
    return redirect("test")

app = Flask(__name__,template_folder="",static_folder="")
app.config["SECRET_KEY"] = "qwerty"
app.add_url_rule("/","index",index)
app.add_url_rule("/test","test",test,methods=["POST","GET"])
app.add_url_rule("/final","final",final)
app.add_url_rule("/setN","setN",setN,methods=["POST"])

app.run()