require 'httparty'

def current_active_competitions
  response = HTTParty.get('https://super6.skysports.com/api/v2/round/active')
  if (reponse.code == 200)
    { start_time: response.body.startDateTime, end_time: response.body.endDateTime }
  end
end