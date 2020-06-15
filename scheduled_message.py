
import requests
from datetime import datetime
from datetime import timedelta
import random
import os
from dotenv import load_dotenv
from match_data import MatchData
from models import UserModel


project_folder = os.getcwd()
load_dotenv(os.path.join(project_folder, '.env'))

getCurrentActiveDates = "https://super6.skysports.com/api/v2/round/active"
postToSlackURL = os.environ["SLACK_WEB_HOOK"]
match_data = MatchData()
user_model = UserModel()
def generateGenericMessage(startDate, endDate, today, data):
  messages = ["Do your super six you silly sausage.", "Do you want to win a million or not? Do your super six.", "Be super slick and do your super six.", "Come on, come on get your super six on, it's {} morning and it won't take long".format(str(today.strftime("%A")))]
  messageNo = random.randint(0, len(messages) - 1)
  return "{message} You have {days} days left! - https://super6.skysports.com/".format(message = messages[messageNo], days=str((endDate - today).days))

def parse_date(timestamp):
  return datetime.strptime(timestamp[0:10], "%Y-%m-%d").date()

def generate_day_one_message(startDate, endDate, today, data):
  return generateGenericMessage(startDate, endDate, today, data) + match_data.retrieve(data)

def compose_slack_message(messageText):
  return {
  "blocks": [
    {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": messageText
        }
    },
    {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "I've entered :white_check_mark:"
					},
					"style": "primary",
					"value": "remove_me"
				}
			]
		}
  ]
}

request = requests.get(getCurrentActiveDates)
data = request.json()

today = datetime.today().date()
startDate = parse_date(data['startDateTime'])
endDate = parse_date(data['endDateTime'])

if startDate + timedelta(days=1) == today:
  user_model.start_new_round()
  message = generate_day_one_message(startDate, endDate, today, data)
  r = requests.post(
    postToSlackURL,
    json=compose_slack_message(message),
    headers={'content-type': 'application/json'}
  )
elif ((today >= startDate) & (today <= endDate) & user_model.users_still_outstanding()):
  message = generateGenericMessage(startDate, endDate, today, data)
  r = requests.post(
    postToSlackURL,
    json=message, 
    headers={'content-type': 'application/json'}
  ) 
