#!/usr/bin/env python

import sys
import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument('input', type=str, help="Input CSV file.")

args = parser.parse_args()

common_responses = {
  'income': {'short': 'Income', 'fear factor': 3},
  'weight': {'short': 'Weight', 'fear factor': 5},
  'activity': {'short': 'Activity Level', 'fear factor': 3},
  'friends': {'short': 'Social Network', 'fear factor': 2},
  'address': {'short': 'Address', 'fear factor': 1}
}

fear_responses = {
  'income':
    {'question': 'Without asking, what could an application determine your yearly income?',
     'responses': {'An application could predict my income exactly, to within $1 / year.': {'level': 3, 'short': '\$1', 'impossible': True},
                   'An application could predict my income to within $100 / year.': {'level': 2, 'short': '\$100', 'impossible': True},
                   'An application could predict my income to within $10,000 / year.': {'level': 1, 'short': '\$10,000', 'impossible': False},
                   'An application could not determine anything about my income level.': {'level': 0, 'short': 'nothing', 'impossible': False}
                   }
    },
  'weight':
    {'question': 'Without asking, what could an application determine about your weight?',
     'responses': {'An application could predict my weight exactly, to within 1 lb.': {'level': 3, 'short': '1 lb', 'impossible': True},
                   'An application could predict my weight to within 10 lbs.': {'level': 2, 'short': '10 lb', 'impossible': True},
                   'An application could predict whether I was at a healthy weight, overweight, or extremely overweight.': {'level': 1, 'short': 'category', 'impossible': False},
                   'An application could not determine anything about my weight.': {'level': 0, 'short': 'nothing', 'impossible': False}
                  }
    },
  'friends':
    {'question': 'Without asking, what could an application determine about your social network?',
     'responses': {'An application could determine exactly who my five best friends were.': {'level': 3, 'short': 'five best friends', 'impossible': False},
                   'An application could determine who some of my friends were.': {'level': 2, 'short': 'some friends', 'impossible': False},
                   'An application could determine how socially active I am.': {'level': 1, 'short': 'how social', 'impossible': False},
                   'An application could not determine anything about my social network.': {'level': 0, 'short': 'nothing', 'impossible': False}
                  }
    },
  'activity':
    {'question': 'Without asking, what could an application determine about your activity level?',
     'responses': {'An application could determine how much and what forms of exercise I engage in.': {'level': 3, 'short': 'quantity and type', 'impossible': True},
                   'An application could determine how much I exercise.': {'level': 2, 'short': 'how much', 'impossible': False},
                   'An application could determine whether I was generally very active, active, or sedentary.': {'level': 1, 'short': 'activity level', 'impossible': False},
                   'An application could not determine anything about my activity level.': {'level': 0, 'short': 'nothing', 'impossible': False}
                  }
    },
  'address':
    {'question': 'Without asking, what could an application determine about where you live?',
     'responses': {'An application could determine the exact address where I live.': {'level': 3, 'short': 'exact', 'impossible': False},
                   'An application could determine what street I live on.': {'level': 2, 'short': 'street', 'impossible': False},
                   'An application could determine what neighborhood I live in.': {'level': 1, 'short': 'neighborhood', 'impossible': False},
                   'An application could not determine anything about where I live.': {'level': 0, 'short': 'nothing', 'impossible': False}
                  }
    },
}

fear_questions = {}
for fear_response in fear_responses.values():
  for response in fear_response['responses'].values():
    response['count'] = 0
  fear_questions[fear_response['question']] = fear_response

comfort_responses = {
  'income':
    {'question': 'How comfortable are you with smartphone applications knowing your yearly income?',},
  'weight':
    {'question': 'How comfortable are you with smartphone applications knowing your weight?',},
  'friends':
    {'question': 'How comfortable are you with smartphone applications knowing about your social network?',},
  'activity':
    {'question': 'How comfortable are you with smartphone applications knowing your activity level?',},
  'address':
    {'question': 'How comfortable are you with smartphone applications knowing where you live?',},
}

comfort_questions = {}
for comfort_response in comfort_responses.values():
  comfort_response['responses'] = {}
  for i in range(1, 6):
    comfort_response['responses'][i] = {}
  for response in comfort_response['responses'].values():
    response['count'] = 0
  comfort_questions[comfort_response['question']] = comfort_response

mocking_responses = {
  'income':
    {'question': 'If a smartphone application could accurately determine my income level',
     'responses': {'I would like to appear to have a lower yearly income than I actually do.': {'mocking': True, 'short': 'lower', 'order': 2},
                   'I would like to appear to have a higher yearly income than I actually do.': {'mocking': True, 'short': 'higher', 'order': 1},
                   'I am comfortable revealing my true income level to the application.': {'mocking': False, 'short': 'true', 'order': 0},
                  }
    },
  'weight':
    {'question': 'If a smartphone application could accurately determine my weight',
     'responses': {'I would like to appear to have a higher weight than I actually do.': {'mocking': True, 'short': 'higher', 'order': 2},
                   'I would like to appear to have a lower weight than I actually do.': {'mocking': True, 'short': 'lower', 'order': 1},
                   'I am comfortable revealing my true weight to the application.': {'mocking': False, 'short': 'true', 'order': 0},
                  },
    },
  'friends':
    {'question': 'If a smartphone application could accurately determine my social network',
     'responses': {'I would like to appear to have more friends than I actually do.': {'mocking': True, 'short': 'more', 'order': 2},
                   'I would like to appear to have fewer friends than I actually do.': {'mocking': True, 'short': 'fewer', 'order': 1},
                   'I am comfortable revealing my true friends and social network to the application.': {'mocking': False, 'short': 'true', 'order': 0},
                  },
    },
  'activity':
    {'question': 'If a smartphone application could accurately determine my activity level',
     'responses': {'I would like to appear less active than I actually am.': {'mocking': True, 'short': 'less', 'order': 2},
                   'I would like to appear more active than I actually am.': {'mocking': True, 'short': 'more', 'order': 1},
                   'I am comfortable revealing how active I truly am to the application.': {'mocking': False, 'short': 'true', 'order': 0},
                  },
    },
  'address':
    {'question': 'If a smartphone application could accurately determine where I live',
     'responses': {'I would like to appear to live in a different place than I actually do.': {'mocking': True, 'short': 'different', 'order': 1},
                   'I am comfortable revealing the true location of my home to the application.': {'mocking': False, 'short': 'true', 'order': 0},
                  },
    },
}

mocking_questions = {}
for mocking_response in mocking_responses.values():
  for response in mocking_response['responses'].values():
    response['count'] = 0
  mocking_questions[mocking_response['question']] = mocking_response

total_responses = 0
mocking_yes = 0
mocking_total = 0

mocking_counts = {}
comfort_counts = {}
fear_counts = {}

ordered_keys = sorted(common_responses.keys(), key=lambda k: common_responses[k]['fear factor'])
ordered_values = sorted(common_responses.values(), key=lambda v: v['fear factor'])

for line in csv.DictReader(open(args.input, 'rb')):
  total_responses += 1

  mocking_counts[total_responses] = 0
  comfort_counts[total_responses] = 0
  fear_counts[total_responses] = 0

  assert len(set(line.keys()).intersection(set(fear_questions.keys()))) == len(fear_responses)
  assert len(set(line.keys()).intersection(set(comfort_questions.keys()))) == len(comfort_responses)
  assert len(set(line.keys()).intersection(set(mocking_questions.keys()))) == len(mocking_responses)
  
  saw_mocking = False
  
  for k,v in line.items():
    if k in fear_questions:
      assert v in fear_questions[k]['responses'].keys()
      fear_questions[k]['responses'][v]['count'] += 1
      if fear_questions[k]['responses'][v]['impossible']:
        fear_counts[total_responses] += 1
    elif k in comfort_questions:
      v = int(v)
      assert v >= 0 and v <= 5
      comfort_questions[k]['responses'][v]['count'] += 1
      if int(v) <= 2:
        comfort_counts[total_responses] += 1
    elif k in mocking_questions:
      assert v in mocking_questions[k]['responses'].keys()
      mocking_questions[k]['responses'][v]['count'] += 1
      if mocking_questions[k]['responses'][v]['mocking']:
        if not saw_mocking:
          mocking_yes += 1
          saw_mocking = True
        mocking_total += 1
        mocking_counts[total_responses] += 1

mocked_counts = {}
comforted_counts = {}
fearful_counts = {}

for i in range(6):
  mocked_counts[i] = 0.
  comforted_counts[i] = 0.
  fearful_counts[i] = 0.

for unused,count in mocking_counts.items():
  mocked_counts[count] += 1.

for unused,count in comfort_counts.items():
  comforted_counts[count] += 1.

for unused,count in fear_counts.items():
  fearful_counts[count] += 1.

table = open('summarytable.tex', 'wb')

print >>table,"""
\\begin{tabularx}{\\columnwidth}{Xcccccc}
& \multicolumn{6}{c}{\\normalsize{\\textbf{Attribute Count}}} \\\\
& {\\normalsize{\\textbf{0}}} 
& {\\normalsize{\\textbf{1}}} 
& {\\normalsize{\\textbf{2}}} 
& {\\normalsize{\\textbf{3}}} 
& {\\normalsize{\\textbf{4}}} 
& {\\normalsize{\\textbf{5}}} \\\\ \\midrule"""

print >>table,"""Unreasonable Fear & %s \\\\""" % \
    ("""&""".join([str(int(round(fearful_counts[i] / total_responses * 100.))) for i in range(6)]),)
print >>table,"""Uncomfortable & %s \\\\""" % \
    ("""&""".join([str(int(round(comforted_counts[i] / total_responses * 100.))) for i in range(6)]),)
print >>table,"""Interested in changing & %s \\\\""" % \
     ("""&""".join([str(int(round(mocked_counts[i] / total_responses * 100.))) for i in range(6)]),)

print >>table,"""
\\end{tabularx}"""

table.close()

table = open('surveytable.tex', 'wb')

print >>table,"""
\\begin{tabularx}{\\textwidth}{Xr@{\hskip 0.2in}rr@{\hskip 0.2in}rr@{\hskip 0.2in}rr@{\hskip 0.2in}rr@{\hskip 0.2in}rr}"""

print >>table,"&&%s\\\\ \\toprule" % ("&".join(["\\multicolumn{2}{c}{\\normalsize{\\textbf{%s}}}" %
                                      (c['short'],) for c in ordered_values]))
#print >>table, "\\multicolumn{2}{l}{\\normalsize{Fear Factor}} &%s\\\\ \\midrule" % ("&".join(["\\multicolumn{2}{c}{%s}" % (c['fear factor'],) for c in ordered_values]))

for i in range(3, -1, -1):
  cells = []
  if i == 3:
    cells.append("\\multirow{4}{*}{\\normalsize{Accuracy}}&")
  else:
    cells.append("&")
  for c in ordered_keys:
    for r in fear_responses[c]['responses'].values():
      if r['level'] == i:
        if r['impossible']:
          cells.append("\\textbf{%s}" % (str(r['short'])))
        else:
          cells.append(str(r['short']))
        cells.append("%d" % (100. * r['count'] / total_responses))
        break

  print >>table, " & ".join(cells), " \\\\",
  if i == 0:
    print >>table, "\\midrule"
  else:
    print >>table

for i in range(5, 0, -1) :
  cells = []
  if i == 5:
    cells.append("\\multirow{5}{*}{\\normalsize{Comfort}}")
  else:
    cells.append("")
  
  if i == 5:
    cells.append("High")
  elif i == 1:
    cells.append("Low")
  else:
    cells.append("")

  for c in ordered_keys:
    for l, r in comfort_responses[c]['responses'].items():
      if l == i:
        cells.append("\\multicolumn{2}{c}{%s}" % ("%d" % (100. * r['count'] / total_responses)))
        break
  
  print >>table, " & ".join(cells), " \\\\",
  if i == 1:
    print >>table, "\\midrule"
  else:
    print >>table

for i in range(2, -1, -1):
  cells = []
  if i == 2:
    cells.append("\\multirow{3}{*}{\\normalsize{Mocking}}")
  else:
    cells.append("")
  
  if i == 2:
    cells.append("\\multirow{2}{*}{\\normalsize{Yes}}")
  elif i == 0:
    cells.append("\\normalsize{No}")
  else:
    cells.append("")

  for c in ordered_keys:
    found = False
    for r in mocking_responses[c]['responses'].values():
      if r['order'] == i:
        found = True
        cells.append(str(r['short']))
        cells.append("%d" % (100. * r['count'] / total_responses))
        break
    if not found:
      cells.append("")
      cells.append("")

  
  print >>table, " & ".join(cells), " \\\\",
  if i == 0:
    print >>table, "\\midrule"
  else:
    print >>table

print >>table,"""
\\end{tabularx}
"""
