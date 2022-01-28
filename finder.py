import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

###   BookingFinder #################################################################
class BookingFinder:
    def load_template(self, filename):
        '''
        load cvs in the format given by booking_template.csv 
        '''
        template_dict = []  # dictionary version, from csv file
        template = [] #list/numpy array? for use in the optimiser/locator
        
        print('filename: ' + filename)
        with open(filename, 'r') as csvfile:
            # need the next few lines to deal with whitespaces in key.  Explicitly send this to DictReader
            header = csvfile.readline().split(',')
            header = [header[idx].strip() for idx in range(0,len(header)) ]
            print(header)
            csvread = csv.DictReader(csvfile, fieldnames=header)
            for row in csvread:
                print(row)
                template_dict.append(row) #as a dictionary 

        # express as lists
        nslots = len(template_dict)
        template_resources = header
        for slot in range(0,nslots):
            print(slot)
            print(template)
            template.append(list(template_dict[slot].values()))

        print(template_resources)
        print(template)

        # this is a numpy array of STRINGS - need to convert to ints for the booking locator.
        test = np.array(template)
        print(test)
        print(type(test[0][0]))
        
    def empty_fn(self):
        return "Hello from BookingFinder"

###   main() #################################################################
test_finder = BookingFinder()
test_finder.load_template('finder_template.csv')
print(test_finder.empty_fn())
