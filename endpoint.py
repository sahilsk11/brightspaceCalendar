import requests
import flask
app = flask.Flask(__name__)


@app.route("/")
def test_endpoint():
  token = flask.request.args.get('token');
  r = requests.get(
      "https://purdue.brightspace.com/d2l/le/calendar/feed/user/feed.ics?token="+token)
  txt = r.text
  events = txt.split("BEGIN:VEVENT")
  entries = []
  for line in events:
    entries.append(line.split("\n"))
  out = []
  for event in entries:
    if " - Availab" not in event[2]:
      out.append(event)

  out_str = ""
  for i in range(len(out)):
    event = out[i]
    if i != 0:
      out_str += "BEGIN:VEVENT"
    event_str = ""
    for line in event:
      if line != "":
        event_str += line + "\n"
    out_str += event_str
  _calendar = out_str

  #  turn calendar data into a response
  response = flask.make_response(_calendar)
  response.headers["Content-Type"] = "text/calendar; charset=UTF-8"
  return response

if __name__ == "__main__":
  app.run(debug=True, threaded=False)
