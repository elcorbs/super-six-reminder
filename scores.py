import requests
import lxml.html
import cssselect

from main import data

matches = [i['match'] for i in data['scoreChallenges']] # extract match data

def match_urls(matches):
    competition_urls = {
        "Sky Bet Championship":"english/championship",
        "Premier League":"english/premier-league"}
    match_urls = []
    for match in matches:
        match_urls.append(
            '/'.join(["https://www.oddschecker.com/football",
                competition_urls[match['competitionName']],
                match['homeTeam']['name'].lower().replace(" ","-") + '-v-' + match['awayTeam']['name'].lower().replace(" ","-"),
                "correct-score"
            ])
        )
    return match_urls

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
    message = 'Prediction score data <Probabilities from bookies odds> \\n'
    sorted_probs = sorted(probs.items(), key=lambda i: i[1], reverse=True)
    for score, prob in sorted_probs[0:display_no]:
        message += f"{score} @ {prob*100:.1f}% \\n"
    return message

# main #
match_urls = match_urls(matches)
for url in match_urls:
    score_probabilities = get_score_probabilities(url)
    if not score_probabilities:
        print(f'Couldnt find data from url: {url}')
    else:
        print(scores_probabilities_message(score_probabilities))
