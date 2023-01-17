from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown
import markdown

# Init App
app = Flask(__name__)
Markdown(app)

text = """
# Markdown
"""

html = markdown.markdown(text, extensions=['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code'])

@app.route('/')
def index():
      return render_template('index.html',html=html)


if __name__ == '__main__':
	app.run(debug=True)