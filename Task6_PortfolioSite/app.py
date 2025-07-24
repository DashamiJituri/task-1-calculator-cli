from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return f"Thanks {name}, your message has been received!"
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

