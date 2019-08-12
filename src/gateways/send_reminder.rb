require 'httpary'

def send_reminder
  HTTParty.post('https://hooks.slack.com/services/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',
  body: { text: 'Go do your super six: https://super6.skysports.com/' }, headers: {'Content-type': 'application/json'})
end