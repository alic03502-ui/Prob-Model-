import numpy as np
from scipy.stats import poisson

def fair_odds(prob):
    if prob == 0:
        return 0
    return round(1 / prob, 2)

def calculate_match(home_xg_home, home_xga_home,
                    away_xg_away, away_xga_away,
                    league_avg):

    # --- Expected goals ---
    home_xg = (home_xg_home * away_xga_away) / league_avg
    away_xg = (away_xg_away * home_xga_home) / league_avg
    total_xg = home_xg + away_xg

    max_goals = 10

    home_probs = [poisson.pmf(i, home_xg) for i in range(max_goals)]
    away_probs = [poisson.pmf(i, away_xg) for i in range(max_goals)]
    matrix = np.outer(home_probs, away_probs)

    # --- Goal markets ---
    def prob_total(threshold, over=True):
        if over:
            return sum(matrix[i][j] for i in range(max_goals)
                                      for j in range(max_goals)
                                      if i + j >= threshold)
        else:
            return sum(matrix[i][j] for i in range(max_goals)
                                      for j in range(max_goals)
                                      if i + j <= threshold)

    over_0_5 = prob_total(1)
    over_1_5 = prob_total(2)
    over_2_5 = prob_total(3)
    over_3_5 = prob_total(4)
    over_4_5 = prob_total(5)

    under_0_5 = 1 - over_0_5
    under_1_5 = 1 - over_1_5
    under_2_5 = 1 - over_2_5
    under_3_5 = 1 - over_3_5
    under_4_5 = 1 - over_4_5

    # --- BTTS ---
    btts = sum(matrix[i][j] for i in range(1, max_goals)
                              for j in range(1, max_goals))

    # --- Match result ---
    home_win = sum(matrix[i][j] for i in range(max_goals)
                                  for j in range(max_goals)
                                  if i > j)

    draw = sum(matrix[i][j] for i in range(max_goals)
                              for j in range(max_goals)
                              if i == j)

    away_win = sum(matrix[i][j] for i in range(max_goals)
                                  for j in range(max_goals)
                                  if i < j)

    one_x = home_win + draw
    x_two = away_win + draw
    one_two = home_win + away_win

    # --- Team totals ---
    def team_total(probs, threshold):
        return sum(probs[i] for i in range(threshold, max_goals))

    home_over_0_5 = team_total(home_probs, 1)
    home_over_1_5 = team_total(home_probs, 2)
    home_over_2_5 = team_total(home_probs, 3)

    away_over_0_5 = team_total(away_probs, 1)
    away_over_1_5 = team_total(away_probs, 2)
    away_over_2_5 = team_total(away_probs, 3)

    # --- Combo markets ---
    def combo(condition):
        return sum(matrix[i][j] for i in range(max_goals)
                                  for j in range(max_goals)
                                  if condition(i, j))

    one_x_o15 = combo(lambda i, j: (i >= j) and (i + j >= 2))
    one_x_o25 = combo(lambda i, j: (i >= j) and (i + j >= 3))
    one_x_u35 = combo(lambda i, j: (i >= j) and (i + j <= 3))

    x_two_o15 = combo(lambda i, j: (i <= j) and (i + j >= 2))
    x_two_o25 = combo(lambda i, j: (i <= j) and (i + j >= 3))
    x_two_u35 = combo(lambda i, j: (i <= j) and (i + j <= 3))

    markets = {
        "Over 0.5": over_0_5,
        "Over 1.5": over_1_5,
        "Over 2.5": over_2_5,
        "Over 3.5": over_3_5,
        "Over 4.5": over_4_5,

        "Under 0.5": under_0_5,
        "Under 1.5": under_1_5,
        "Under 2.5": under_2_5,
        "Under 3.5": under_3_5,
        "Under 4.5": under_4_5,

        "BTTS": btts,

        "Home Win": home_win,
        "Draw": draw,
        "Away Win": away_win,
        "1X": one_x,
        "X2": x_two,
        "12": one_two,

        "Home O0.5": home_over_0_5,
        "Home O1.5": home_over_1_5,
        "Home O2.5": home_over_2_5,

        "Away O0.5": away_over_0_5,
        "Away O1.5": away_over_1_5,
        "Away O2.5": away_over_2_5,

        "1X + O1.5": one_x_o15,
        "1X + O2.5": one_x_o25,
        "1X + U3.5": one_x_u35,

        "X2 + O1.5": x_two_o15,
        "X2 + O2.5": x_two_o25,
        "X2 + U3.5": x_two_u35,
    }

    # --- Convert to % and fair odds ---
    output = {
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "total_xg": round(total_xg, 2),
        "markets": {}
    }

    for market, prob in markets.items():
        prob = round(prob, 4)
        output["markets"][market] = {
            "probability_%": round(prob * 100, 2),
            "fair_odds": fair_odds(prob)
        }

    return output
