import globals
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


$$e^{i\pi}+1=0$$



```python
class Qcm:
    def __init__(self,statement,answers,good_answers):
        self.statement = statement
        self.answers = answers
        self.good_answers = good_answers
```
"""

html = markdown.markdown(text, extensions=['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code'])

@app.route('/')
def index():
      return render_template('index.html',html=html)


if __name__ == '__main__':
      app.run(debug=True)
      globals.initialize() 