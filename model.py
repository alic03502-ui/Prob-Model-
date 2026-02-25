import math
from scipy.stats import poisson

MAX_GOALS = 6

def fair_odds(prob):
    return 1 / prob if prob > 0 else 0

def score_matrix(home_xg, away_xg):
    matrix = []
    for i in range(MAX_GOALS):
        row = []
        for j in range(MAX_GOALS):
            row.append(poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg))
        matrix.append(row)
    return matrix

def match_outcomes(matrix):
    home = draw = away = 0
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            if i > j:
                home += matrix[i][j]
            elif i == j:
                draw += matrix[i][j]
            else:
                away += matrix[i][j]
    return home, draw, away

def total_prob(matrix, line):
    under = 0
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            if i + j <= line:
                under += matrix[i][j]
    over = 1 - under
    return over, under

def team_total_prob(xg, line):
    under = poisson.cdf(line, xg)
    over = 1 - under
    return over, under

def btts_prob(matrix):
    yes = 0
    for i in range(1, MAX_GOALS):
        for j in range(1, MAX_GOALS):
            yes += matrix[i][j]
    no = 1 - yes
    return yes, no

def calculate_all_markets(home_xg, away_xg, league_avg):

    matrix = score_matrix(home_xg, away_xg)
    home_win, draw, away_win = match_outcomes(matrix)

    results = {}

    # 1X2
    results["Home Win"] = (home_win, fair_odds(home_win))
    results["Draw"] = (draw, fair_odds(draw))
    results["Away Win"] = (away_win, fair_odds(away_win))

    # Double chance
    results["1X"] = (home_win + draw, fair_odds(home_win + draw))
    results["X2"] = (away_win + draw, fair_odds(away_win + draw))
    results["12"] = (home_win + away_win, fair_odds(home_win + away_win))

    # Totals
    for line in [0.5, 1.5, 2.5, 3.5, 4.5]:
        over, under = total_prob(matrix, int(line))
        results[f"Over {line}"] = (over, fair_odds(over))
        results[f"Under {line}"] = (under, fair_odds(under))

    # BTTS
    btts_yes, btts_no = btts_prob(matrix)
    results["BTTS Yes"] = (btts_yes, fair_odds(btts_yes))
    results["BTTS No"] = (btts_no, fair_odds(btts_no))

    # Team totals
    for line in [0.5, 1.5, 2.5]:
        over_h, under_h = team_total_prob(home_xg, int(line))
        over_a, under_a = team_total_prob(away_xg, int(line))

        results[f"Home Over {line}"] = (over_h, fair_odds(over_h))
        results[f"Home Under {line}"] = (under_h, fair_odds(under_h))
        results[f"Away Over {line}"] = (over_a, fair_odds(over_a))
        results[f"Away Under {line}"] = (under_a, fair_odds(under_a))

    # Combos with totals
    over15, _ = total_prob(matrix, 1)
    over25, _ = total_prob(matrix, 2)

    results["1X + Over 1.5"] = ((home_win + draw) * over15,
                               fair_odds((home_win + draw) * over15))

    results["1X + Over 2.5"] = ((home_win + draw) * over25,
                               fair_odds((home_win + draw) * over25))

    results["X2 + Over 1.5"] = ((away_win + draw) * over15,
                               fair_odds((away_win + draw) * over15))

    results["X2 + Over 2.5"] = ((away_win + draw) * over25,
                               fair_odds((away_win + draw) * over25))

    results["Home Win + Over 1.5"] = (home_win * over15,
                                     fair_odds(home_win * over15))

    results["Away Win + Over 1.5"] = (away_win * over15,
                                     fair_odds(away_win * over15))

    return results
