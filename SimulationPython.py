import random
import csv
import copy
import numpy as np

class Runner(object):
    # Constructor of the runner class that represents a participant
    def __init__(self, gender, bib, age, t5k, officialTime):
        self.Gender = gender
        self.Bib = bib
        self.Age = age
        self.Time5k = t5k
        self.OfficialTime = officialTime
        self.Result = 0
        
    # Printing override
    def __str__(self):
        output = 'Runner Gender = ' + str(self.Gender) + ', Bib : ' + \
        str(self.Bib) + ', Age : ' + str(self.Age) + ', Time5k : ' + \
        str(self.Time5k) + ', Official Time: ' + str(self.OfficialTime) + \
        ", Result: " + str(self.Result) + "\n"
        return output
    
    # Calculation using the linear model
    # Includes random noise from a normal distribution
    def calcResultL1(self, cAge, c5k, cBibN, cGender):
        self.Result = float(self.Age) * cAge + \
        float(self.Gender) * cGender + \
        float(self.Bib) * cBibN + float(self.Time5k) * c5k + \
        np.random.normal(0,0.5) * 100
        self.Result = int(self.Result)
        
      
class EmpiricalDistribution(object):
    # Constructor of the empirical distribution
    def __init__(self):
        self.Name = 'Empirical Distribution'
        self.Runners = []
        self.Selection = []
        
    # Method that reads the data from a txt file previously 
    # build using RStudio that contains the empirical distribution
    # of the total of participants
    def readData(self):
        with open('EmpiricalData.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    self.Runners.append(Runner(row[2], row[1],\
                                               row[3], row[4], row[5]))
            print(f'Processed {line_count} lines.')
    
    # Selects a sample of size n with replacement from 
    # the empirical distribution
    def selectRandom(self, n):
        self.Selection = []
        print(str(n) + ' runners picked at random')
        for i in range(n):
          runner = random.choice(self.Runners)
          self.Selection.append(runner)
          print(str(runner))
          
        return self.Selection
        

class Simulation(object):
    # Constructor, contains the coefficient of the linear model
    # Also contains the min and max values for the 2^k Factorial Exp.
    def __init__(self, distribution):
      self.Empirical = distribution
      
      self.L1Age = 5.404e+00
      self.L15k = 9.006e+00
      self.L1BibN = 8.650e-03
      self.L1Gender = -1.865e+02
      
      self.AgePos = 20
      self.AgeNeg = 60
      self.GenderPos = 1
      self.GenderNeg = 2
      self.BibPos = 3
      self.BibNeg = 31437

    # Method that executes the simulation for all the runners
    # Calls the calcResultL1 methods and sends the coefficientes
    # The Result property of each runner is filled with the result
    def runSimulation(self,currentDistro,file):
      
      for runner in currentDistro:
          runner.calcResultL1(self.L1Age, self.L15k, \
                              self.L1BibN, self.L1Gender)
          print(str(runner))
      
      output = '"Num","Bib","Gender","Age","Time5k","OfficialTime","Result"\n'
      i = 0
      for run in currentDistro:
          i += 1
          output += str(i) + ',' + str(run.Bib) + ',' + str(run.Gender) + ',' + \
          str(run.Age) + ',' + str(run.Time5k) + ',' + \
          str(run.OfficialTime) + \
          ',' + str(run.Result) + '\n'
            
      print(output,  file=open(file, 'w'))
    
    # Runs a regular simulation with a random sample
    # Does not modify factors
    def runRegularSim(self):
        currentDistro = copy.deepcopy(self.Empirical)
        self.runSimulation(currentDistro,'regularSim.txt')
   
    # Runs a simulation according to some factor setup
    # Receives a + or - sign for each factor
    # Uses the values from the constructor accordingly
    # Stores the results in a file that can be import to RStudio
    def runFactorialSim(self, age, gender, bib, identity):
        currentDistro = copy.deepcopy(self.Empirical)
        for runner in currentDistro:
            runner.Bib = self.BibPos if bib == '+' else self.BibNeg
            runner.Gender = self.GenderPos if \
            gender == '+' else self.GenderNeg
            runner.Age = self.AgePos if age == '+' else self.AgeNeg
        self.runSimulation(currentDistro, str(identity) + 'Sim_Bib' + \
                           str(bib) + 'Gender' + str(gender) + 'Age' + \
                           str(age) + 'factors.txt')
        
    def printRunners(self):
        for runner in self.Empirical:
            print(runner)

empirical = EmpiricalDistribution()
empirical.readData()
# Taking a random sample of 379 participants
mySim1 = Simulation(empirical.selectRandom(379))

mySim1.runRegularSim()

# Running the total of Factorial Experiments
mySim1.runFactorialSim('-','-','-','R1')
mySim1.runFactorialSim('+','-','-','R2')
mySim1.runFactorialSim('-','+','-','R3')
mySim1.runFactorialSim('+','+','-','R4')
mySim1.runFactorialSim('-','-','+','R5')
mySim1.runFactorialSim('+','-','+','R6')
mySim1.runFactorialSim('-','+','+','R7')
mySim1.runFactorialSim('+','+','+','R8')

'''
mySim = Simulation(0)
print(mySim.readEmpiricalData())
print(mySim.printRunners())
print(mySim.runSimulation(100))

x = mySim.runSimulation(1000)
print(x,  file=open('log.txt', 'w'))
'''