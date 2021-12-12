from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'HELLLOOOO'


if __name__ == '__main__':
   app.run()


# Select from db cities or data point 
# offer to make an excel file
# or show as data vis