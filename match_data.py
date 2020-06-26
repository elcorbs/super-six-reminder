import requests
import lxml.html
import cssselect


class MatchData:
    def match_url(self, match: dict) -> str:
        competition_urls = {
            "Sky Bet Championship": "english/championship",
            "Premier League": "english/premier-league",
            "FA Cup": "english/fa-cup",
        }
        return "/".join(
            [
                "https://www.oddschecker.com/football",
                competition_urls[match["competitionName"]],
                match["homeTeam"]["name"].lower().replace(" ", "-")
                + "-v-"
                + match["awayTeam"]["name"].lower().replace(" ", "-"),
                "correct-score",
            ]
        )

    def get_score_probabilities(self, url: str) -> dict:
        response = requests.get(url)
        elems = lxml.html.fromstring(response.text)
        score_probabilities = {}
        for score in elems.cssselect('[id="t1"] tr'):
            text = score.get("data-bname")
            odds = score.get("data-best-dig")
            prob = 1 / float(odds)
            score_probabilities[text] = prob
        if len(score_probabilities) == 0:
            return
        return score_probabilities

    def scores_probabilities_message(self, probs: dict, display_no=4) -> str:
        if not probs:
            return f"Couldnt find probability data"

        message = "Prediction score data: \n"
        sorted_probs = sorted(probs.items(), key=lambda i: i[1], reverse=True)
        for score, prob in sorted_probs[0:display_no]:
            message += f"{score} @ {prob*100:.1f}% \n"
        return message

    def get_details_for_match(self, match):
        details = f"{match['homeTeam']['name']}-{match['awayTeam']['name']}"
        try:
            url = self.match_url(match)
            probabilities = self.scores_probabilities_message(self.get_score_probabilities(url), 2)
        except KeyError:
            probabilities = "Could not find odds for this competition"
        return "*" + details + "*" + "\n" + probabilities

    def retrieve(self, data):
        matches = [i["match"] for i in data["scoreChallenges"]]
        match_details = [self.get_details_for_match(match) for match in matches]
        return "\n" + str("\n".join(match_details))

