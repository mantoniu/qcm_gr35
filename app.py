from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/site/<name>/<password>')
def site(name,password):
   return 'welcome %s' % name

@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      passw = request.form['password']
      return redirect(url_for('site',name = user, password = passw))
   else:
      user = request.args.get('name')
      return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)