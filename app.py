import markdown
import md_mermaid

from flask import Flask, redirect, url_for, request, render_template
from flaskext.markdown import Markdown
app = Flask(__name__)
Markdown(app)


from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown

# Init App
app = Flask(__name__)

@app.route('/')
def index():
   mkd_text = '''## Your Markdown Here
   ```mermaid
   graph TB
   D --> E
   E --> F
   ``̀ 
   '''
   return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)