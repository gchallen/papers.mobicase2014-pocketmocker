#!/usr/bin/env python

import matplotlib,datetime,csv,os
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc

rc('font',**{'family':'serif','serif':['Times'],'size':'9'})
rc('text', usetex=True)

for filename in ['idle.csv', 'recording.csv', 'replaying.csv']:
  times, currents = [], []
  first_time = None
  with open(filename, 'rb') as csvfile:
    for row in csv.reader(csvfile):
      try:
        time, current = float(row[0]), float(row[1])
      except:
        continue
      if first_time == None:
        first_time = time
      times.append(time - first_time)
      currents.append(current)

  fig = plt.figure()
  ax = fig.add_subplot(111)
  
  ax.plot(times, currents, linewidth=0.1, color='black')

  ax.set_xlabel('\\textbf{Time (s)}')
  ax.set_ylabel('\\textbf{Power (mA)}')

  fig.set_size_inches(2.5, 2.0)
  fig.savefig(os.path.splitext(filename)[0] + '.pdf', bbox_inches='tight')
