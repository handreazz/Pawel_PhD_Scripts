import numpy as np

class roller:
  def __init__(self):
    self.n_sides = 6
  def roll(self):
    return np.random.randint(1,self.n_sides+1)
  def sum_n_rolls(self,n):
    total = 0
    for i in range(n):
      total += self.roll()
    return total
  def roll_up_to(self, M):
    total = 0
    n_rolls =0
    while total < M:
      total += self.roll()
      n_rolls +=1
    return total, n_rolls

def run_simulation(r, target, n):
  totals = []
  rolls = []
  for trial in range(n):
    subtotal, subrolls = r.roll_up_to(target)
    totals.append(subtotal)
    rolls.append(subrolls)
  return totals, rolls

r = roller()

#Q1, Q3, Q5, Q7
target = 20
n_trials = 10000
totals, rolls = run_simulation(r, target, n_trials)
print "Q1: %3.1f" %(np.mean(np.array(totals)-target))
print "Q3: %3.1f" %(np.mean(rolls))
print "Q5: %3.1f" %(np.std(np.array(totals)-target))
print "Q7: %3.1f" %(np.std(rolls))

#Q2, Q4, Q6, Q8
target = 10000
n_trials = 10000
totals, rolls = run_simulation(r, target, n_trials)
print "Q2: %3.1f" %(np.mean(np.array(totals)-target))
print "Q4: %3.1f" %(np.mean(rolls))
print "Q6: %3.1f" %(np.std(np.array(totals)-target))
print "Q8: %3.1f" %(np.std(rolls))
