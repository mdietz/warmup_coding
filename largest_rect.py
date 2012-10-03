import random

histogram = []

for i in range(10):
  cur_bar = []
  j = 0
  for j in range(random.randint(0,10)):
    cur_bar.append(1)
  for k in range(10-j):
    cur_bar.append(0)
  histogram.append(cur_bar)

#print histogram

work = []

for i in range(len(histogram)):
  cur_work = []
  for j in range(len(histogram[i])):
    cur_work.append((0, 0))
  work.append(cur_work)

#print work

for i in range(len(histogram)):
  for j in range(len(histogram[i])):
    # Extend up, extend right, extend both, none
        #
    # # ##
    ### ##
    ######

    # none
    if histogram[i][j] == 0:
      work[i][j] = (0, 0)
    else:
      if work[i-1][j] != (0,0) and work[i][j-1] != (0,0):
        work[i][j] = (work[i-1][j][0]+1, work[i][j-1][1]+1)
      elif work[i-1][j] != (0,0):
        work[i][j] = (work[i-1][j][0]+1, 1)
      elif work[i][j-1] != (0,0):
        work[i][j] = (1, work[i][j-1][1])
      else:
        work[i][j] = (1,1)

max_ = 0
max_loc = (-1, -1, -1, -1)
for i in range(len(work)):
  for j in range(len(work[i])):
    pos_max = work[i][j][0] * work[i][j][1]
    if pos_max > max_:
      max_loc = (i-work[i][j][0]+1, j-work[i][j][1]+1, work[i][j][0], work[i][j][1])
      max_ = pos_max

for elem in histogram:
  elem.reverse

reverse_iter = range(len(histogram))
reverse_iter.reverse()

for i in reverse_iter:
  out_line = '%d  ' % i 
  for j in range(len(histogram[i])):
    if histogram[i][j] == 1:
      out_line = out_line + '# '
    else:
      out_line = out_line + '  '
  print out_line
print '  0 1 2 3 4 5 6 7 8 9'

print max_
print max_loc