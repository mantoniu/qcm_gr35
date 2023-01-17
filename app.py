from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown
import markdown
# Init App
app = Flask(__name__)
Markdown(app)



text = """
# Title

Some text.

​```mermaid
graph TB
A --> B
B --> C
​```

Some other text.

​```mermaid
graph TB
D --> E
E --> F
​```
"""

html = markdown.markdown(text, extensions=['md_mermaid'])



@app.route('/')
def index():
      return render_template('index.html',html=html)


if __name__ == '__main__':
	app.run(debug=True)