import globals
from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown
import markdown
from user import User

# Init App
app = Flask(__name__)
Markdown(app)
if __name__ == '__main__':
      globals.init() 


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

globals.users_data.addUser(User(email="fabiepnj@gmail.com", password="zebi", name="Wolchzbfhbzeh", firstname="Fabien"))
print(globals.users_data.users_array)

if __name__ == '__main__':
      app.run(debug=True)