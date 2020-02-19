
import requests
from datetime import datetime
import random
import os

getCurrentActiveDates = "https://super6.skysports.com/api/v2/round/active"
postToSlackURL = os.environ["SLACK_WEB_HOOK"]

def getMatches(data):
  matches = [[x['match']['homeTeam']['name'], x['match']['awayTeam']['name']]  for x in data['scoreChallenges']]
  return '\\n' + str('\\n'.join([x for x in [' - '.join(match) for match in matches]]))

def generateGenericMessage(startDate, endDate, today, data):
  messages = ["Do you super six you silly sausage.", "Do you want to win a million or not? Do your super six.", "Be super slick and do your super six.", "Come on, come on get your super six on, it's {} morning and it won't take long".format(str(today.strftime("%A")))]
  messageNo = random.randint(0, len(messages) - 1)
  return "{message} You have {days} days left! - https://super6.skysports.com/".format(message = messages[messageNo], days=str((endDate - today).days))

request = requests.get(getCurrentActiveDates)
data = request.json()

today = datetime.today().date()
startDate = datetime.strptime(data['startDateTime'][0:10], "%Y-%m-%d").date()
endDate = datetime.strptime(data['endDateTime'][0:10], "%Y-%m-%d").date()

message = generateGenericMessage(startDate, endDate, today, data)

if startDate == today:
  message += getMatches(data) 

if ((today >= startDate) & (today <= endDate)):
  r = requests.post(
    postToSlackURL,
    json={'text': message},
    headers={'content-type': 'application/json'}
  )
