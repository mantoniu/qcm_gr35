import globals
import saving
from flask import Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
from user import User
from qcm import *
import markdown as md

# Init App
app = Flask(__name__)
app.secret_key = 'AHJBHG236RT6YT4GYH2BN__r372UYFG2EIU2YG'
Markdown(app)
if __name__ == '__main__':
      globals.init() 
      saving.init()


def is_logged():
      return 'email' in session and 'password' in session and saving.users_data.login(session['email'], session['password'])

@app.route('/')
def index():
      if is_logged():
            return render_template('home.html')
      else:
            return render_template('index.html',html=html)

@app.route('/logout')
def logout():
      session.pop('email')
      session.pop('password')
      return redirect('/')


@app.route('/login',methods = ['POST'])
def login():
      if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            if saving.users_data.login(email, password):
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

@app.route('/my_qcm')
def my_qcm():
      if is_logged():
            return render_template('my_qcm.html', my_qcm_array=saving.qcm_data.get_qcm_from_user(session['email']))
      else:
            return redirect('/')

@app.route('/qcm')
def qcm():
      if is_logged():
            return render_template('qcm.html', qcm_array=saving.qcm_data.get_all_qcm())
      else:
            return redirect('/')

@app.route('/newstate',methods=['POST'])
def newstate():
      if 'enonce' in request.form:
            response_list = []
            good_answer = []
            enonce = request.form['enonce']
            enonce = enonce.replace("\r","")
            for i in range (0,int(request.form['count'])+1):
                  response_list.append(request.form['question'+str(i)])
                  if "switch"+str(i) in request.form:
                        good_answer.append(i)
            question = Question(enonce,good_answer,response_list,session['email'])
            saving.questions_data.add_question(question)
      return render_template('card.html',html = question.get_state())


@app.route('/create')
def create():
      return render_template("card.html")


@app.route('/preview',methods=['POST','GET'])
def preview():
      return md.markdown(request.form['text'], extensions=md_extensions)


q1 = Question(question="Combien ?", possibles_responses=["Onze", "Treize"], valids_reponses=[0], user_email="kilian.dcs@gmail.com")
q2 = Question(question="Où?", possibles_responses=["Ici", "Là-bas", "Par là"], valids_reponses=[2, 3], user_email="kilian.dcs@gmail.com")
qcm1 = QCM("QCM Test", [q1, q2], user_email="kilian.dcs@gmail.com")
saving.qcm_data.add_qcm(qcm1)

if __name__ == '__main__':
      app.run(debug=True)