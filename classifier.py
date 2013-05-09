import nltk
import csv
import random
import collections

#feature extraction
def extract_features(row): 
       features = {}
       features = { 'dayofweek': row[4], 
                    'airline': row[6] ,  
                    'origin' : row[11],
                    'dest': row[16],
                    'depthour' :  row[18][:len(row[18])-2] }
       return features

#label extraction
def extract_label(row):
       if float(row[21]) > 0.0:
          label = 'late'
       else: 
          label = 'ontime'
       return label

""" A python singleton """
class Classifier:
 
    class __impl:

	rows = []
        _classifier = None

        """ Implementation of the singleton interface """

        def load(self,filename):
	  rows = []
          self.__dict__['rows'] = rows
          with open(filename, 'rb') as csvfile:
           mycsv = csv.reader(csvfile)
           for row in mycsv:
             if row[21] != '':
              rows.append(row)

        def train(self):
	  print "training classifier"
	  sample = self.__dict__['rows']
#	  random.shuffle(sample)
	  samples = len(sample)
	  teststart = int(2*samples/3)
          featuresets = [ (extract_features(a), extract_label(a)) for a in sample] 
	  train_set = featuresets[:teststart]
	  test_set =  featuresets[teststart:samples-1]

	  classifier = nltk.NaiveBayesClassifier.train(train_set)
          self.__dict__['classifier'] = classifier
	  
	  classifier.show_most_informative_features()

	  refsets = collections.defaultdict(set)
	  testsets = collections.defaultdict(set)
	 
	  # test all of the classifications
	  for i, (feats, label) in enumerate(test_set):
	    refsets[label].add(i)
	    observed = classifier.classify(feats)
	    testsets[observed].add(i)
	 
	  print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)
	  print 'ontime precision:', nltk.metrics.precision(refsets['ontime'],  testsets['ontime'])
	  print 'ontime recall:', nltk.metrics.recall(refsets['ontime'], testsets['ontime'])
	  print 'late precision:', nltk.metrics.precision(refsets['late'], testsets['late'])
	  print 'late recall:', nltk.metrics.recall(refsets['late'], testsets['late'])
          print "training complete"

        def findprob(self,featureset,label):
          print featureset, label
	  classifier = self.__dict__['classifier']
          prob = classifier.prob_classify(featureset).prob(label)
          return prob


    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """        
        # Check whether we already have an instance
        if Classifier.__instance is None:
            # Create and remember instance
            Classifier.__instance = Classifier.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = Classifier.__instance
                                 

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

