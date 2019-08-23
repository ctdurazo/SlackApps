from flask import Flask, jsonify, request
import urllib.request
import urllib.parse
import hashlib
import hmac
import base64

app = Flask(__name__)


@app.route("/ban", methods=['GET', 'POST'])
def ban():
	x_slack_request_timestamp = str(request.headers.get("X-Slack-Request-Timestamp"))
	version_number = "v0"
	request_body = str(request.query_string)
	signing_secret = request.values.get("sig")
	x_slack_signature = request.headers.get("X-Slack-Signature")
	auth = str(request.values.get("token"))

	# print(x_slack_request_timestamp)
	# print(version_number)
	# print(request_body)
	# print(signing_secret)
	# print(x_slack_signature)
	# print(auth)

	#base_string = bytes(version_number + ":" + x_slack_request_timestamp + ":" + request_body, 'utf-8')
	#secret = bytes(signing_secret, 'utf-8')

	#signature = base64.b64encode(hmac.new(secret, base_string, digestmod=hashlib.sha256).digest())
	#print(signature)

	#if signature == x_slack_signature:
	channel = request.values.get('channel_id')
	user = request.values.get('text')[request.values.get('text').find("<@") + 2: request.values.get('text').find('|')]
	name = request.values.get('text')[request.values.get('text').find("|") + 1: request.values.get('text').find('>')]
	reason = request.values.get('text')[request.values.get('text').find('>') + 2:]

	values = {"token": auth, "channel": channel, "user": user}
	data = urllib.parse.urlencode(values).encode('utf-8')

	uri = "https://slack.com/api/groups.kick"
	req = urllib.request.Request(uri, data)
	with urllib.request.urlopen(req) as response:
		content = str(response.read().decode("utf-8") )

	if content == '{"ok":true}':
		return jsonify({"response_type": "in_channel", 'text': '@' + name + " was banned for \"" + reason + '"'})
	else:
		uri = "https://slack.com/api/channels.kick"
		req = urllib.request.Request(uri, data)
		with urllib.request.urlopen(req) as response:
			content = str(response.read().decode("utf-8") )
		if content == '{"ok":true}':
			return jsonify(
				{"response_type": "in_channel", 'text': '@' + name + " was banned for \"" + reason + '"'})
		else:
			return jsonify({'text': "sorry this command failed due to: \"" + content + '"'})
	#else:
		#return "Failed to authenticate"


@app.route("/trivia", methods=['GET', 'POST'])
def trivia():
	content = str(urllib.request.urlopen("http://numbersapi.com/random/date").read().decode("utf-8"))

	return jsonify({"response_type": "in_channel", 'text': content})


if __name__ == '__main__':
	app.run()
