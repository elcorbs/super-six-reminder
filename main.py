
import requests
from datetime import datetime
import random

getCurrentActiveDates = "https://super6.skysports.com/api/v2/round/active"
postToSlackURL = "https://hooks.slack.com/services/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"


def getMatches(data):
  matches = [[x['match']['homeTeam']['name'], x['match']['awayTeam']['name']]  for x in data['scoreChallenges']]
  return '\\n' + str('\\n'.join([x for x in [' - '.join(match) for match in matches]]))

def generateMessage(startDate, endDate, today, data):
  messages = ["Do you super six you silly sausage.", "Do you want to win a million or not? Do your super six.", "Be super slick and do your super six.", "Come on, come on get your super six on, it's {} morning and it won't take long".format(str(today.strftime("%A")))]
  messageNo = random.randint(0, len(messages) - 1)
  mainMessage = "{message} You have {days} days left! - https://super6.skysports.com/".format(message = messages[messageNo], days=str((endDate - today).days))

  if startDate == today:
    mainMessage = mainMessage + getMatches(data)
  return mainMessage


request = requests.get(getCurrentActiveDates)
data = request.json()

today = datetime.today().date()
startTime = datetime.strptime(data['startDateTime'][0:10], "%Y-%m-%d").date()
endTime = datetime.strptime(data['endDateTime'][0:10], "%Y-%m-%d").date()
if ((today >= startTime) & (today <= endTime)):
  r = requests.post(
    postToSlackURL,
    json={'text': generateMessage(startTime, endTime, today, data)},
    headers={'content-type': 'application/json'}
  )
  print(r)


