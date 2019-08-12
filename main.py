
import requests
from datetime import datetime
import random

getNextDateAPI = "https://super6.skysports.com/api/v2/round/active"
postToSlackURL = "https://hooks.slack.com/services/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"

messages = ['Do you super six you silly sausage.', 'Do you want to win a million or not? Do your super six.', 'Be super slick and do you super six.']

def generateMessage(endDate, today, messages):
  messageNo = random.randint(0, len(messages) - 1)
  return "{message} You have {days} days left!".format(message = messages[messageNo], days=str((endDate - today).days))


data = requests.get(getNextDateAPI)

today = datetime.today()
startTime = datetime.strptime(data.json()['startDateTime'][0:10], "%Y-%m-%d")
endTime = datetime.strptime(data.json()['endDateTime'][0:10], "%Y-%m-%d")

if ((today >= startTime) & (today <= endTime)):
  r = requests.post(postToSlackURL, json={'text': generateMessage(endTime, today, messages)}, headers={'content-type': 'application/json'})

print(r.status_code)
