import globals
import saving
from flask import flash,Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
from user import Student, Teacher
from qcm import *
import markdown as md
from utilities import read_file
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit,rooms
from werkzeug.utils import secure_filename
import os

# Liste des questions projetées

global projected_qcmid,owners

projected_qcmid = []
owners = {}


# Initialisation
app = Flask(__name__)
app.debug = True
socket = SocketIO(app)
UPLOAD_FOLDER = 'static/files'
app.secret_key = 'AHJBHG236RT6YT4GYH2BN__r372UYFG2EIU2YG'
app.config['SECRET_TYPE'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


globals.init() 
saving.init()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            
      return  Statement(name=name, question=question, valids_reponses=valids_reponses, possibles_responses=possibles_responses, user_email=session['email'],tags=tags)

# Fonction qui vérifie si l'utilisateur est connecté
def is_logged(role:str) -> bool:
      if 'role' in session and 'email' in session and 'password' in session and role==session['role']:
            if session['role']=="teacher":
                  print("\n t \n",saving.teachers_data.login(session['email'], session['password']))
                  return saving.teachers_data.login(session['email'], session['password'])
            else:
                  print("\n s \n",saving.students_data.login(session['email'], session['password']))
                  return saving.students_data.login(session['email'], session['password'])
      return False

# Déconnecter élève
def disconnect_student(student_email):
      user_liveqcm = saving.liveqcm_data.get_liveqcm_by_student_email(session['email'])
      if user_liveqcm != None:
            user_liveqcm.student_leave(session['email'])
            socket.emit('count',user_liveqcm.get_students_count(),to=owners[user_liveqcm.owner_email])

# Renvoie sur la route "/" des fichiers html
@app.route('/')
def index():
      return render_template("student_or_teacher.html")


@app.route('/teacher')
def teacher_home():
      if is_logged("teacher"):
            return redirect("/my_states")
      else: 
            return render_template('/teacher/index.html')

@app.route('/student',methods = ['GET','POST'])
def student_home():
      if is_logged("student"):
            disconnect_student(session['email'])
            return render_template('/student/home.html')
      else:
            return render_template('/student/login.html')

@app.route('/student/myaccount')
def student_account():
      disconnect_student(session['email'])
      user = saving.students_data.get_user_by_email(session['email'])
      return render_template('/student/myaccount.html',user=user)

@app.route('/student/question/<id>')
def joined_statement(id):
      global projected_qcmid
      if is_logged("student"):
            if id in projected_qcmid:
                  liveqcm = saving.liveqcm_data.get_liveqcm_by_id(id)
                  return render_template("/student/statement.html",statement=liveqcm.get_current_statement(),liveqcmid=id,stopped=liveqcm.is_paused())
      return redirect('/student')



# Changement de mot de passe

@app.route('/student/newpassword',methods=['POST'])
def change_password():
      if 'actual_password' in request.form and 'new_password' in request.form:
            user = saving.students_data.get_user_by_email(session['email'])
            if user.change_password(request.form['actual_password'], request.form['new_password']):
                  saving.students_data.update_user_data(user)
                  session['password'] = request.form['new_password']
            return redirect('/student')

# Route qui gère la déconnexion
@app.route('/logout')
def logout():
      if session['role']=="teacher":
            session.pop('email')
            session.pop('password')
            session.pop('role')
      return redirect('/')

# Route qui gère la déconnexion
@app.route('/student/logout')
def sudent_logout():
      disconnect_student(session['email'])
      if session['role']=="student":
            session.pop('email')
            session.pop('password')
            session.pop('role')
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
                  session['role'] = "teacher"
      return redirect('/teacher')

# Route qui gère la connexion
@app.route('/student/login',methods = ['POST'])
def student_login():
      if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            if saving.students_data.login(email, password):
                  session['email'] = email
                  session['password'] = password
                  session['role'] = "student"
      return redirect('/student')

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
                  return redirect('/teacher')
            else:
                  return render_template('/teacher/index.html')

# Ajouter des étudiants

@app.route('/add_students')
def add_students():
      if is_logged("teacher"):
            return render_template('/teacher/add_students.html')
      else:
            return redirect('/teacher')

# Liste de tous les qcm
@app.route('/qcm')
def qcm():
      if is_logged("teacher"):
            return render_template('/teacher/qcm_list.html', qcm_array=saving.qcm_data.get_all_qcm())
      else:
            return redirect('/teacher')


# Permet de renvoyer la liste des qcm et donc l'affichage de ceux-ci dans my_qcm.html
@app.route('/my_qcm')
def my_qcm():
      if is_logged("teacher"):
            return render_template('/teacher/my_qcm.html', my_qcm_array=saving.qcm_data.get_qcm_from_user(session['email']))
      else:
            return redirect('/teacher')

# Permet de renvoyer la liste des énoncés et donc l'affichage de ceux-ci dans my_states.html
# et si des tags ont été rentrés d'afficher seulement les énoncés correspondant
@app.route('/my_states',methods=['POST','GET'])
def my_states():
      if is_logged("teacher"):
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
            return redirect('/teacher')


# Creation d'un nouvel énoncé (submit formulaire)
@app.route('/newstate',methods=['POST'])
def newstate():
      statement = statement_values()
      print("\n",statement.tags,"\n")
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
@app.route('/qcm/<id>/<statement_number>')
def qcm_id(id,statement_number):
      global ownersemail
      qcm = saving.qcm_data.get_qcm_by_id(id)
      liveqcm = saving.liveqcm_data.get_liveqcm_by_owner_email(session['email'])
      liveqcm_id,statement_index = 0,0
      statement_number = int(statement_number)
      if liveqcm != None:
            liveqcm_id = liveqcm.id
            statement_index = liveqcm.statement_index
      
      if statement_number+2 <= len(qcm.statements):
            current_statement = qcm.statements[statement_number]
            print("\ n",session['email'] in owners.keys())
            return render_template("/teacher/qcm.html",statement=current_statement,qcm=qcm,statement_number=statement_number,final=False,projected=session['email'] in owners.keys(),liveqcm_id=liveqcm_id,statement_index=statement_index) 
      elif statement_number == len(qcm.statements):
            print('\n TEST \n',qcm.statements)
            return redirect('/my_qcm')
      else:
            current_statement = qcm.statements[statement_number]
            return render_template("/teacher/qcm.html",statement=current_statement,qcm=qcm,statement_number=statement_number,final=True,projected=session['email'] in owners.keys(),liveqcm_id=liveqcm_id,statement_index=statement_index)

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

# Upload fichier csv étudiant
@app.route('/receive_csv',methods=['GET','POST'])
def upload_file():   
      if request.method == 'POST':
            if 'file' not in request.files:
                  flash('No file part')
                  return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                  flash('No selected file')
                  return redirect(request.url)
            if file and allowed_file(file.filename):
                  filename = secure_filename(file.filename)
                  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                  saving.students_data.create_accounts_from_csv("static/files/" + filename)
                  os.remove("static/files/" + filename)
                  return redirect(url_for('upload_file', name=filename))
      return redirect('/teacher')


@socket.on('disconnect')
def disconnection():
      print('disconnected')
      

@socket.on('connect')
def connection():
      print('ZADNAZODNAZODNAOZND \n \n')
      if session['email'] in owners.keys():
            print('1ZADNAZODNAZODNAOZND \n \n')
            owners[session['email']] = request.sid
            liveqcm = saving.liveqcm_data.get_liveqcm_by_owner_email(session['email'])
            socket.emit('count',liveqcm.get_students_count(),to=owners[session['email']])
            print("\n",request.sid,"\n")
      
      liveqcm = saving.liveqcm_data.get_liveqcm_by_student_email(session['email'])
      if liveqcm != None:
            print('\n AHAHAHAHHAHAHHA TROP MARANT \n')
            join_room(liveqcm.id)
            socket.emit('count',liveqcm.get_students_count(),to=owners[liveqcm.owner_email])


@socket.on('project')
def project(id):
      global projected_qcmid,owners
      liveqcm = None
      # Question simple
      if saving.statements_data.contains_id(id):
            statements = [saving.statements_data.get_statement_by_id(id)]
      # Séquence de question
      elif saving.qcm_data.contains_id(id):
            statements = saving.qcm_data.get_qcm_by_id(id).statements
      liveqcm = LiveQCM(owner_email=session['email'], statements=statements)
      owners[session['email']] = request.sid
      saving.liveqcm_data.add_liveqcm(liveqcm)
      projected_qcmid.append(liveqcm.id)
      print(projected_qcmid)
      socket.emit('liveqcmid',liveqcm.id,to=owners[session['email']])

@socket.on('stop')
def stop():
      global projected_qcmid
      liveqcm_id = saving.liveqcm_data.get_liveqcm_by_owner_email(session['email']).id
      if liveqcm_id in projected_qcmid:
            liveqcm = saving.liveqcm_data.get_liveqcm_by_id(liveqcm_id)
            liveqcm.end()
            saving.liveqcm_data.save_liveqcm_to_file(liveqcm)
            projected_qcmid.remove(liveqcm_id)
            print("\n STOP \n")
            socket.emit('stop',to=owners[session['email']])
            del owners[session['email']]

@socket.on('newresponse')
def response(response_list,liveqcmid):
      global owners
      student_email = session['email']
      liveqcm = saving.liveqcm_data.get_liveqcm_by_id(liveqcmid)
      success = liveqcm.respond(student_email,response_list)
      socket.emit('response_success',success)
      if success:
            socket.emit('response',{"responses_count":liveqcm.get_responses_count(),"count":liveqcm.get_total_responses_count()},to=owners[session['email']])


@socket.on('liveqcm_join')
def liveqcm_join(qcmid):
      global projected_qcmid
      print(projected_qcmid,qcmid)
      not_found = qcmid not in projected_qcmid
      socket.emit('liveqcm_join',{"not_found":not_found,"qcmid":qcmid},to=request.sid)

@socket.on('studentjoin')
def student_join(qcmid):
      disconnect_student(session['email'])      
      liveqcm = saving.liveqcm_data.get_liveqcm_by_id(qcmid)
      join_room(qcmid)
      liveqcm.student_join(session['email'])
      socket.emit('count',liveqcm.get_students_count(),to=owners[liveqcm.owner_email])

@socket.on('stop_question')
def stop_question(liveqcm_id):
      liveqcm = saving.liveqcm_data.get_liveqcm_by_id(liveqcm_id)
      liveqcm.pause()
      socket.emit('stop_question',to=liveqcm_id)
      socket.emit

@socket.on('unstop_question')
def unstop_question(liveqcm_id):
      liveqcm = saving.liveqcm_data.get_liveqcm_by_id(liveqcm_id)
      liveqcm.resume()
      socket.emit('unstop_question',to=liveqcm_id)

@socket.on('nextquestion')
def next_question(liveqcm_id,statement_number):
      global projected_qcmid,owners
      print('test')
      if liveqcm_id in projected_qcmid:
            qcm = saving.liveqcm_data.get_liveqcm_by_id(liveqcm_id)
            qcm.next_statement()
            socket.emit('nextquestion',to=liveqcm_id)
            socket.emit('nextquestion',qcm.statement_index,to=owners[qcm.owner_email])
            socket.emit('count',liveqcm.get_students_count(),to=owners[session['email']])
      else:
            socket.emit('nextquestion',statement_number+1)

if __name__ == '__main__':
      socket.run(app)