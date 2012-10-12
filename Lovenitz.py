#from pygep.functions.arithmetic import *
#from pygep.functions.linkers import sum_linker
#from pygep import *
import random


#generates the sampling points
class DataPoint(object):
	
	SAMPLE = [] #where the set of 3d points for sampling (grouped in DataPoint-type objects) will be stored
	SAMPLE_SIZE = 10 # number of 3d points in the sample
	RANGE_LOW, RANGE_HIGH = -10, 10  #span of each coordinate where the points are picked from
	RANGE_SIZE = RANGE_HIGH-RANGE_LOW  #size of that span
	MEANS = []
	
	
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.xm, self.ym, self.zm = 0, 0, 0
			
		
  #creates a random set of sampling points
  @staticmethod
	def populate():
		DataPoint.SAMPLE = []
		for _ in xrange(DataPoint.SAMPLE_SIZE):
				x = DataPoint.RANGE_LOW + (random.random() * DataPoints.RANGE_SIZE)
				y = DataPoint.RANGE_LOW + (random.random() * DataPoints.RANGE_SIZE)
				z = DataPoint.RANGE_LOW + (random.random() * DataPoints.RANGE_SIZE)
				DataPoint.SAMPLE.append(DataPoint(x, y, z))
				
	@staticmethod		
	def setMeans(population):
		for i in DataPoint.SAMPLE: #para cada ponto...
			sum = 0
			for j in population: #...calcula uma media sobre todos os cromossomas...
				inc = j(i)
				sum += inc
			DataPoint.MEANS.append(sum/population.size) #...que vai ser adicionada a uma lista
		return DataPoint.MEANS
		
	@staticmethod
	def resetMeans():
		DataPoint.MEANS=[]
		
		
				
			
class Equality(Chromosome):
	REWARD = 1000.0
	functions = multiply, add, subtract, divide
	terminals = 'x', 'y', 'z'

	
	def _fitness(self):
		total = 0
		i = 0
        for x in DataPoint.SAMPLE: #for each sampling 3d point
            try:
                guess = self(x) #value of the chromosome at this point of SAMPLE
                diff = min(1.0, abs((guess - DataPoint.MEANS[i]) / DataPoint.MEANS[i])) #deviation to the average value of all chromosomes at that point of SAMPLE
                total += self.REWARD * (1 - diff) #gets a fraction of REWARD which will determine the likelihood of the survival of its lineage
                                
            except ZeroDivisionError: # semantic error
                pass

        return total
        
		
	# checks whether a theorem has been found according to a fitness threshold
  def _solved(self):
  	return self.fitness == self.max_fitness
  	
  max_fitness = property(lambda self: self.REWARD * DataPoint.SAMPLE_SIZE)
  

		
		

 
if __name__ == '__name__':
	DataPoint.populate()
	
	p = Mob(Regression, 30, 8, 4, sum_linker)
	print p
	
	for _ in xrange(100): #for a hundred generations
		DataPoint.setMeans(p) #compute the list of average values on each sample point
		if p.best.solved:   
			break
		p.cycle()  #if not yet solved move to the next generation
		DataPoint.resetMeans()  #reset MEANS
		print
		print p
		
	if p.best.solved:
		print
		print 'SOLVED:', p.best
	

			
	
