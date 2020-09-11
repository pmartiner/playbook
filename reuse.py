import json
import numpy as np
import pandas as pd

with open('example.json', 'r') as myfile:
    data=myfile.read()

rng = np.random.default_rng()

teams = {
    'NE': 'Patriots',
    'NO': 'Saints',
    'PIT': 'Steelers',
    'KC': 'Chiefs',
    'MIN': 'Vikings',
    'LAR': 'Rams',
    'LAC': 'Chargers',
    'PHI': 'Eagles',
    'ATL': 'Falcons',
    'DAL': 'Cowboys',
    'TB': 'Buccaneers',
    'DET': 'Lions',
    'OAK': 'Raiders',
    'SEA': 'Seahawks',
    'GB': 'Packers',
    'JAX': 'Jaguars',
    'CAR': 'Panthers',
    'TEN': 'Titans',
    'SF': '49ers',
    'WAS': 'Redskins',
    'BAL': 'Ravens',
    'CIN': 'Bengals',
    'NYG': 'Giants',
    'HOU': 'Texans',
    'NYJ': 'Jets',
    'BUF': 'Bills',
    'MIA': 'Dolhpins',
    'CHI': 'Bears',
    'IND': 'Colts',
    'ARI': 'Cardinals',
    'DEN': 'Broncos',
    'CLE': 'Browns'
}

# parse file
case = json.loads(data)

currentYardPosition = case['currentYard']
currentDown = case['currentDown']
yardsLeftForFirstDown = case['yardsLeft1stDown']
timeLeft = case['timeLeft']
scoreDifference = case['scoreGap']
home = case['home']

if currentYardPosition >= 1 and currentYardPosition <= 19:
  cyp = 'Deep Zone'
elif currentYardPosition >= 20 and currentYardPosition <= 39:
  cyp = 'Back Zone'
elif currentYardPosition >= 40 and currentYardPosition <= 60:
  cyp = 'Mid Zone'
elif currentYardPosition >= 61 and currentYardPosition <= 79:
  cyp = 'Front Zone'
else:
  cyp = 'Red Zone'

# Short: 1-2 yards to go Mid: 3-6 yards to go Long: 7+ ' ' + yards to go.

if yardsLeftForFirstDown >= 1 and yardsLeftForFirstDown <= 2:
  ylfd = ' & Short'
elif yardsLeftForFirstDown >= 3 and yardsLeftForFirstDown <= 6:
  ylfd = ' & Mid'
else:
  ylfd = ' & Long'
  
if currentDown == 1:
  cd = '1st'
  dwnYrd = cd + ' Down'
elif currentDown == 2:
  cd = '2nd'
  dwnYrd = cd + ylfd
else:
  cd = '3rd/4th'
  dwnYrd = cd + ylfd

if timeLeft >= 60 and timeLeft <= 45:
  tl = '1st Quarter'
elif timeLeft > 45 and timeLeft <= 30:
  tl = '2nd Quarter'
elif timeLeft > 30 and timeLeft <= 15:
  tl = '3rd Quarter'
else:
  tl = '4th Quarter/OT'

# Big: 8 or more points Small: 7 or fewer points Late & Close: All plays in the second half or overtime with the score within 8 points

if scoreDifference <= -8:
  sd = 'Losing Big'
elif scoreDifference > -8 and scoreDifference <= 0:
  sd = 'Tie/Losing Small'
elif scoreDifference > 0 and scoreDifference <= 7:
  sd = 'Winning Small'
else:
  sd = 'Winning Big'
  
if home:
  hm = 'Home DVOA'
else:
  hm = 'Road DVOA'

df_teamRatingsDVOA = pd.read_csv('./data/{year} Team DVOA Ratings Offense.csv'.format(year = case['year']), index_col=0)
df_downDistanceDVOA = pd.read_csv('./data/{year} DVOA by Down and Distance Offense.csv'.format(year = case['year']), index_col=0)
df_downTypePlayDVOA = pd.read_csv('./data/{year} DVOA by Down and Type of Play Offense.csv'.format(year = case['year']), index_col=0)
df_fieldZoneDVOA = pd.read_csv('./data/{year} DVOA by Field Zone Offense.csv'.format(year = case['year']), index_col=0)
df_homeDVOA = pd.read_csv('./data/{year} DVOA by Home and Road Offense.csv'.format(year = case['year']), index_col=0)
df_quartersHalvesDVOA = pd.read_csv('./data/{year} DVOA by Quarters and Halves Offense.csv'.format(year = case['year']), index_col=0)
df_singleGameDVOA = pd.read_csv('./data/{year} Single-Game DVOA Ratings {team}.csv'.format(year = case['year'], team = teams[case['currentTeam']]), index_col='Opponent')
df_scoreGapDVOA = pd.read_csv('./data/{year} DVOA by Score Gap Offense.csv'.format(year = case['year']), index_col=0)



def reuse():
  team = case['currentTeam']
  # print(df_teamRatingsDVOA.loc[team, :])
  caseDwnYrd = df_downDistanceDVOA.loc[team, dwnYrd].replace('%', '')
  # print(df_downTypePlayDVOA.loc[team, :])
  caseCyp = df_fieldZoneDVOA.loc[team, cyp].replace('%', '')
  caseHm = df_homeDVOA.loc[team, hm].replace('%', '')
  caseTl = df_quartersHalvesDVOA.loc[team, tl].replace('%', '')
  caseAvgOffensiveDVOA = df_singleGameDVOA.loc[case['opponent'], 'Offense DVOA'].replace('%', '')
  casePassPlayDVOA = df_singleGameDVOA.loc[case['opponent'], 'Offense Pass DVOA'].replace('%', '')
  caseRushPlayDVOA = df_singleGameDVOA.loc[case['opponent'], 'Offense Rush DVOA'].replace('%', '')
  caseSd = df_scoreGapDVOA.loc[team, sd].replace('%', '')
  
  currentState = sorted([
      round(float(caseDwnYrd)/100, 4),
      round(float(caseCyp)/100, 4),
      round(float(caseHm)/100, 4),
      round(float(caseTl)/100, 4),
      round(float(caseSd)/100, 4)
    ], reverse=True)
  
  caseAvgOffensiveRivalDVOA = round(float(caseAvgOffensiveDVOA)/100, 4)
  
  currentStateWeighted = np.array([
    0.5*currentState[0],
    0.25*currentState[1],
    0.125*currentState[2],
    0.0625*currentState[3],
    0.0625*currentState[4]
  ])
  
  estimatedDVOA = round(np.mean(currentStateWeighted), 4)

  successProbability = abs(rng.random() * caseAvgOffensiveRivalDVOA)
  
  successfulPassDVOA = round(float(casePassPlayDVOA)/100, 4)
  successfulRushDVOA = round(float(caseRushPlayDVOA)/100, 4)
    
  estimatedSuccessfulPassPlayDVOA = successfulPassDVOA * estimatedDVOA
  estimatedSuccessfulRushPlayDVOA = successfulRushDVOA * estimatedDVOA
  
  passSuccessProbability = abs(successProbability * estimatedSuccessfulPassPlayDVOA)
  rushSuccessProbability = abs(successProbability * estimatedSuccessfulRushPlayDVOA)

  print(currentState, currentStateWeighted, estimatedDVOA*100, passSuccessProbability, rushSuccessProbability)
  return