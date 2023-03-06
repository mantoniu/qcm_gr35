import globals
import saving
from flask import Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
from user import Student, Teacher
from qcm import *
import markdown as md
from utilities import read_file
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit

# Initialisation
app = Flask(__name__)
app.debug = True
app.secret_key = 'AHJBHG236RT6YT4GYH2BN__r372UYFG2EIU2YG'
app.config['SECRET_TYPE'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
socketio = SocketIO(app, manage_session=False,logger=True, engineio_logger=True)

globals.init() 
saving.init()

# Fonction qui récupère les information d'un énoncé dans un formulaire
def statement_values():
      possibles_responses = []
      valids_reponses = []
      name = request.form['statement_name']
      question = request.form['enonce']
      question = question.replace("\r","")    
      tags = []  
      if request.form.getlist('etiquettes'):
            tags = request.form.getlist('etiquettes')
      if "decimal" not in request.form :
            for i in range (0,int(request.form['count'])+1):
                  if 'statement'+str(i) in request.form:
                        possibles_responses.append(request.form['statement'+str(i)])
                  if "switch"+str(i) in request.form:
                        valids_reponses.append(i)
      else:
            possibles_responses.append(request.form['statement'])
            valids_reponses.append(0)
            
      return  Statement(name=name, question=question, valids_reponses=valids_reponses, possibles_responses=possibles_responses, user_email=session['email'])

# Fonction qui vérifie si l'utilisateur est connecté
def is_logged():
      return 'email' in session and 'password' in session and (saving.teachers_data.login(session['email'], session['password']) or saving.students_data.login(session['email'], session['password']))

# Renvoie sur la route "/" des fichiers html
@app.route('/')
def index():
      if is_logged():
            return render_template('/teacher/home.html')
      else:
            return render_template('/teacher/index.html')

@app.route('/student/login')
def student_login():
      return render_template('/student/login.html')

@app.route('/student/home',methods = ['GET','POST'])
def student_home():
      return render_template('/student/home.html')

@app.route('/student/myaccount')
def student_account():
      return render_template('/student/myaccount.html')

# Route qui gère la déconnexion
@app.route('/logout')
def logout():
      session.pop('email')
      session.pop('password')
      return redirect('/')

# Route qui gère la connexion
@app.route('/login',methods = ['POST'])
def login():
      if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            if saving.teachers_data.login(email, password):
                  session['email'] = email
                  session['password'] = password
            return redirect('/')

# Route qui gère l'inscription
@app.route('/register', methods=['POST'])
def register():
      if 'email' in request.form and 'password' in request.form and 'name' in request.form and 'firstname' in request.form:
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            firstname = request.form['firstname']
            if saving.teachers_data.add_user(Teacher(email, password, name, firstname)):
                  session['email'] = email
                  session['password'] = password
                  return redirect('/')
            else:
                  return render_template('/teacher/index.html')

# Permet de renvoyer la liste des qcm et donc l'affichage de ceux-ci dans my_qcm.html
@app.route('/my_qcm')
def my_qcm():
      if is_logged():
            return render_template('/teacher/my_qcm.html', my_qcm_array=saving.qcm_data.get_qcm_from_user(session['email']))
      else:
            return redirect('/')

# Permet de renvoyer la liste des énoncés et donc l'affichage de ceux-ci dans my_states.html
# et si des tags ont été rentrés d'afficher seulement les énoncés correspondant
@app.route('/my_states',methods=['POST','GET'])
def my_states():
      if is_logged():
            if request.form.getlist('etiquettes'):
                  tags = request.form.getlist('etiquettes')
                  statement_array = saving.statements_data.get_all_statements()
                  countains_tag = []
                  for statement in statement_array:
                        for tag in statement.tags:
                              if tag in tags and statement not in countains_tag:
                                    countains_tag.append(statement)
                  return render_template('/teacher/my_states.html', my_states_array=countains_tag,tags=(saving.teachers_data.get_user_by_email(session['email'])).tags_array)
            else :
                  return render_template('/teacher/my_states.html', my_states_array=saving.statements_data.get_statement_from_user(session['email']),tags=(saving.teachers_data.get_user_by_email(session['email'])).tags_array)
      else:
            return redirect('/')

# Renvoi les informations d'un qcm pour l'afficher
@app.route('/qcm')
def qcm():
      if is_logged():
            return render_template('/teacher/qcm_list.html', qcm_array=saving.qcm_data.get_all_qcm())
      else:
            return redirect('/')

# Creation d'un nouvel énoncé (submit formulaire)
@app.route('/newstate',methods=['POST'])
def newstate():
      statement = statement_values()
      print(statement.decimal)
      saving.statements_data.add_statement(statement)
      return redirect('/my_states')

# Creation d'un nouveau qcm
@app.route('/newqcm',methods=['POST'])
def newqcm():
      statements_list = []
      for statement in saving.statements_data.get_statement_from_user(session['email']):
            if statement.id in request.form:
                  statements_list.append(statement)
      qcm = QCM(name=request.form['qcm_title'],statements=statements_list,user_email=session['email'])
      saving.qcm_data.add_qcm(qcm)
      return redirect('/my_qcm')

# Creation d'un nouvel énoncé (formulaire)
@app.route('/create')
def create():
      return render_template("/teacher/create.html",tags=(saving.teachers_data.get_user_by_email(session['email'])).tags_array)

# Edition énoncé
@app.route('/statement/edit/<id>',methods=['GET'])
def edit(id):
      return render_template('/teacher/edit.html',statement=saving.statements_data.get_statement_by_id(id))

# Renvoi de l'affichage de l'énoncé correspondant
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
      return render_template("/teacher/enonce.html",statement=statement)   
      
# Renvoi de l'affichage du qcm correspondant
@app.route('/qcm/<id>')
def qcm_id(id):
      return render_template("/teacher/qcm.html",qcm=saving.qcm_data.get_qcm_by_id(id)) 

# Renvoi la conversion html du markdown 
@app.route('/preview',methods=['POST','GET'])
def preview():
      return md.markdown("\n"+request.form['text'], extensions=md_extensions)

# Creation d'un tag
@app.route('/newtag',methods=['POST'])
def newtag():
      saving.teachers_data.add_tag_to_user_by_email(session['email'],request.form['tag'])
      return {"success":True}

# Edition formulaire (submit formulaire)
@app.route('/set/<id>',methods=['POST'])
def edit_statement(id):
      statement = statement_values()
      saving.statements_data.set_statement(id,statement)
      return redirect('/my_states')

# Suppression d'un énoncé
@app.route('/statement/delete/<id>')
def delete_statement(id):
      saving.statements_data.remove_statement_by_id(id)
      return redirect('/my_states')

# Suppression d' un qcm
@app.route('/qcm/delete/<id>')
def delete_qcm(id):
      saving.qcm_data.remove_qcm_by_id(id)
      return redirect('/qcm')

@socketio.on('connect')
def connect():
      print("Utilisateur connecté")


if __name__ == '__main__':
      socketio.run(app)