import globals
import saving
from flask import Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
import markdown
from user import User

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

html = markdown.markdown(text, extensions=globals.md_extentions)

@app.route('/')
def index():
      if not('email' in session and 'password' in session):
            return render_template('index.html',html=html)
      else:
            return render_template('card.html', qcm=saving.qcm_data.get_all_qcm())

@app.route('/logout')
def logout():
      session.pop('email')
      session.pop('password')
      return render_template('index.html',html=html)

@app.route('/login',methods = ['POST'])
def login():
      if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            if globals.users_data.login(email, password):
                  session['email'] = email
                  session['password'] = password
                  return redirect('/')
            else:
                  return render_template('index.html',html=html)

@app.route('/register', methods=['POST'])
def register():
      if 'email' in request.form and 'password' in request.form and 'name' in request.form and 'firstname' in request.form:
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            firstname = request.form['firstname']
            if globals.users_data.addUser(User(email, password, name, firstname)):
                  session['email'] = email
                  session['password'] = password
                  return redirect('/')
            else:
                  return render_template('index.html',html=html)

globals.users_data.addUser(User(email="fabiepnj@gmail.com", password="zebi", name="Wolchzbfhbzeh", firstname="Fabien"))
print(globals.users_data.users_array)

if __name__ == '__main__':
      app.run(debug=True)