import globals
from flask import Flask,url_for,render_template,request,session,redirect
from flaskext.markdown import Markdown
import markdown
from user import User

# Init App
app = Flask(__name__)
app.secret_key = 'AHJBHG236RT6YT4GYH2BN_"_ç"rç372UYFG2EIU2YG'
Markdown(app)
if __name__ == '__main__':
      globals.init() 


text = """
# Title

Some text.

"""

html = markdown.markdown(text, extensions=['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code'])

@app.route('/')
def index():
      if not('email' in session and 'password' in session):
            return render_template('index.html',html=html)
      else:
            return render_template('card.html')

@app.route('/logout')
def logout():
      session.pop('email')
      session.pop('password')
      return render_template('index.html',html=html)

@app.route('/login',methods = ['POST'])
def login():
      email = request.form['email']
      password = request.form['password']
      if email != "" and password != "":
            if globals.users_data.login(email, password):
                  session['email'] = email
                  session['password'] = password
                  return render_template('card.html')
            else:
                  return render_template('index.html',html=html)

@app.route('/register', methods=['POST'])
def register():
      email = request.form['email']
      password = request.form['password']
      name = request.form['name']
      firstname = request.form['firstname']
      if ('email' in request.form and 'password' in request.form and 'name' in request.form and 'firstname' in request.form):
            if globals.users_data.addUser(User(email, password, name, firstname)):
                  session['email'] = email
                  session['password'] = password
                  return render_template('card.html')
            else:
                  return render_template('index.html')

print(globals.users_data.users_array)


@app.route('/newcard')
def newcard():
      return {"id":1} ## Remplacer 1 par id

@app.route('/newanswer')
def newanswer():
      return {"answercount":1} ## Remplacer 1 par id

if __name__ == '__main__':
      app.run(debug=True)