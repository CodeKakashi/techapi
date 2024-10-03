# from app.main import app

# if __name__ == "__main__":
#     app.run(debug=True)

# # lets check deployment

from flask import Flask

app = Flask(__name__)

@app.route('/home')
def home():
    return "Welcome All"

@app.route('/')
def Error():
    return "Error on my side"
