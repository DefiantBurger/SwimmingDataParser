from flask import Flask

from routes import all_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporaryKeyThing'
app.register_blueprint(all_routes)

if __name__ == '__main__':
    app.run(port=42069, debug=True)
