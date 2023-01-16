from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown

# Init App
app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
	mkd_text = "## Your Markdown Here "
	return render_template('index.html',mkd_text=mkd_text)

if __name__ == '__main__':
	app.run(debug=True)