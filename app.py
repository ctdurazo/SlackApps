from flask import Flask
from slackapps import slack_apps

app = Flask(__name__)
app.register_blueprint(slack_apps)

if __name__ == '__main__':
	app.run()
