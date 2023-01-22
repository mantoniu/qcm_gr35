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

def statement_values():
      response_list = []
      good_answer = []
      name = request.form['statement_name']
      statement = request.form['enonce']
      statement = statement.replace("\r","")
      for i in range (0,int(request.form['count'])+1):
            response_list.append(request.form['statement'+str(i)])
            if "switch"+str(i) in request.form:
                  good_answer.append(i)
      if request.form.getlist('etiquettes') != None:
            tags = request.form.getlist('etiquettes')
      else:
            tags = []
      return Statement(name=name,question=statement,valids_reponses=good_answer,possibles_responses=response_list,user_email=session['email'],tags=tags)


def is_logged():
      return 'email' in session and 'password' in session and saving.users_data.login(session['email'], session['password'])

@app.route('/')
def index():
      return redirect('http://pornhub.com')
      if is_logged():
            return render_template('home.html')
      else:
            return render_template('index.html')

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
            if saving.users_data.add_user(User(email, password, name, firstname)):
                  session['email'] = email
                  session['password'] = password
                  return redirect('/')
            else:
                  return render_template('index.html')

@app.route('/my_qcm')
def my_qcm():
      if is_logged():
            return render_template('my_qcm.html', my_qcm_array=saving.qcm_data.get_qcm_from_user(session['email']))
      else:
            return redirect('/')

@app.route('/my_states')
def my_states():
      if is_logged():
            return render_template('my_states.html', my_states_array=saving.statements_data.get_statement_from_user(session['email']))
      else:
            return redirect('/')

@app.route('/qcm')
def qcm():
      if is_logged():
            return render_template('qcm_list.html', qcm_array=saving.qcm_data.get_all_qcm())
      else:
            return redirect('/')

@app.route('/newstate',methods=['POST'])
def newstate():
      statement = statement_values()
      saving.statements_data.add_statement(statement)
      return redirect('/my_states')

@app.route('/newqcm',methods=['POST'])
def newqcm():
      statements_list = []
      for statement in saving.statements_data.get_statement_from_user(session['email']):
            if statement.id in request.form:
                  statements_list.append(statement)
      qcm = QCM(name=request.form['qcm_title'],statements=statements_list,user_email=session['email'])
      saving.qcm_data.add_qcm(qcm)
      return redirect('/my_qcm')

@app.route('/create')
def create():
      return render_template("create.html",tags=(saving.users_data.get_user_by_email(session['email'])).tags_array)

@app.route('/statement/edit/<id>',methods=['GET'])
def edit(id):
      return render_template('edit.html',statement=saving.statements_data.get_statement_by_id(id))

@app.route('/statement/<id>',methods=['POST','GET'])
def statement(id): 
      statement = saving.statements_data.get_statement_by_id(id)
      good_answer = []
      bad_answer = []
      for i in range (0,len(statement.possibles_responses)):
            if "switch"+str(i) in request.form:
                  if i in statement.valids_responses:
                        good_answer.append(i)
                  else:
                        bad_answer.append(i)
      return render_template("enonce.html",statement=statement)   
      

@app.route('/qcm/<id>')
def qcm_id(id):
      return render_template("qcm.html",qcm=saving.qcm_data.get_qcm_by_id(id)) 


@app.route('/preview',methods=['POST','GET'])
def preview():
      return md.markdown(request.form['text'], extensions=md_extensions)

@app.route('/newtag',methods=['POST'])
def newtag():
      saving.users_data.add_tag_to_user_by_email(session['email'],request.form['tag'])
      return {"success":True}

@app.route('/set/<id>',methods=['POST'])
def edit_statement(id):
      statement = statement_values()
      saving.statements_data.set_statement(id,statement)
      return redirect('/my_states')

if __name__ == '__main__':
      app.run(debug=True)