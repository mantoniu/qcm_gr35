import globals
import saving
from flask import Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
import markdown as md
from user import User
from qcm import *

# Init App
app = Flask(__name__)
app.secret_key = 'AHJBHG236RT6YT4GYH2BN__r372UYFG2EIU2YG'
Markdown(app)
if __name__ == '__main__':
      globals.init() 
      saving.init()


text = """
# Title

Some text.

"""

html = md.markdown(text, extensions=globals.md_extensions)

@app.route('/')
def index():
      if not('email' in session and 'password' in session):
            return render_template('index.html',html=html)
      else:
            return render_template('card.html', question_array=saving.qcm_data.get_question_from_user(session['email']))

@app.route('/logout')
def logout():
      session.pop('email')
      session.pop('password')
      return redirect('/')

@app.route('/login',methods = ['POST'])
def login():
      print("test1")
      if 'email' in request.form and 'password' in request.form:
            print("test2")
            email = request.form['email']
            password = request.form['password']
            if saving.users_data.login(email, password):
                  print("test3")
                  session['email'] = email
                  session['password'] = password
            return redirect('/')

@app.route('/register', methods=['POST'])
def register():
      if 'email' in request.form and 'password' in request.form and 'name' in request.form and 'firstname' in request.form:
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            firstname = request.form['firstname']
            if saving.users_data.addUser(User(email, password, name, firstname)):
                  session['email'] = email
                  session['password'] = password
                  return redirect('/')
            else:
                  return render_template('index.html',html=html)

@app.route('/newstate/',methods=['POST'])
def newstate():
      if 'enonce' in request.form:
            response_list = []
            good_answer = []
            enonce = request.form['enonce']
            for i in range (0,int(request.form['count'])+1):
                  response_list.append(request.form['question'+str(i)])
                  if "switch"+str(i) in request.form:
                        good_answer.append(i)
            question = Question(enonce,good_answer,response_list,session['email'])
            saving.questions_data.add_question(question)
      print(response_list,good_answer)
      return redirect('/')
      


q1 = Question(question="Combien ?", possibles_responses=["Onze", "Treize"], valids_reponses=[0], user_email="kilian.dcs@gmail.com")
q2 = Question(question="Où?", possibles_responses=["Ici", "Là-bas", "Par là"], valids_reponses=[2, 3], user_email="kilian.dcs@gmail.com")
qcm1 = QCM("QCM Test", [q1, q2], user_email="kilian.dcs@gmail.com")
saving.qcm_data.add_qcm(qcm1)

if __name__ == '__main__':
      app.run(debug=True)