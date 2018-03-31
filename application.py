from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-guess'

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/talk', methods=['POST'])
def talk():
    user_input = request.form['user-input']
    return render_template("index.html")
if __name__ == "__main__":
    app.run()
