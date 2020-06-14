import requests
import lxml.html
import cssselect

def match_url(match: dict) -> str:
    competition_urls = {
        "Sky Bet Championship":"english/championship",
        "Premier League":"english/premier-league"}
    return '/'.join(["https://www.oddschecker.com/football",
            competition_urls[match['competitionName']],
            match['homeTeam']['name'].lower().replace(" ","-") + '-v-' + \
            match['awayTeam']['name'].lower().replace(" ","-"),
            "correct-score"])

def get_score_probabilities(url: str) -> dict:
    response = requests.get(url)
    elems = lxml.html.fromstring(response.text)
    score_probabilities = {}
    for score in elems.cssselect('[id="t1"] tr'):
        text = score.get('data-bname')
        odds = score.get('data-best-dig')
        prob = 1 / float(odds)
        score_probabilities[text] = prob
    if len(score_probabilities) == 0:
        return
    return score_probabilities

def scores_probabilities_message(probs: dict, display_no=4) -> str:
    if not probs:
        return f'Couldnt find probability data'
    
    message = 'Prediction score data: \n'
    sorted_probs = sorted(probs.items(), key=lambda i: i[1], reverse=True)
    for score, prob in sorted_probs[0:display_no]:
        message += f"{score} @ {prob*100:.1f}% \n"
    return message

def get_matches(data):
  matches = [i['match'] for i in data['scoreChallenges']]
  match_urls = [match_url(match) for match in matches]

  messages = [scores_probabilities_message(get_score_probabilities(url)) for url in match_urls]
  return str('\n'.join(messages))