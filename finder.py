import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

###   BookingFinder #################################################################
class BookingFinder:
    def load_template(self, filename):
        '''
        input:  filename of cvs in the format given by booking_template.csv
                assumes a format of 3TE,3TE,3TM,7T,operator with an (ignored) header
        output: numpy array with booking template        
        '''

        template = [] #as list
        
        with open(filename, 'r') as csvfile:
            header = csvfile.readline().split(',')
            header = [header[idx].strip() for idx in range(0,len(header)) ]

            print('filename: ' + filename)
            print(header)

            csvlines = csv.reader(csvfile, delimiter=',')
            for row in csvlines:
                template_line = [ int(resource.strip()) for resource in row ]
                template.append(template_line)
        print(template)
        self.template_np = np.array(template)
        print(self.template_np)
     
    def load_template_dict(self, filename):
        '''
        input:  filename of cvs in the format given by booking_template.csv
                loads template as dict
        output: numpy array with booking template
        NOT WORKING
        '''
        template_dict = []  # dictionary version, from csv file
        template = [] #list/numpy array? for use in the optimiser/locator

        print('filename: ' + filename)
        with open(filename, 'r') as csvfile:
            # need the next few lines to deal with whitespaces in key.  Explicitly send this to DictReader
            header = csvfile.readline().split(',')
            header = [header[idx].strip() for idx in range(0,len(header)) ]
            for res in header:
                print(res)
            csvread = csv.DictReader(csvfile, fieldnames=header)
            for row in csvread:
                tmp=list(row.values())
                # still not there with the typing:  this gets it into a LIST of INTs
                print(tmp[1])
                print(int(tmp[1]))
                template_dict.append(row) #as a dictionary

        # express as lists
        nslots = len(template_dict)
        template_resources = header
        for slot in range(0,nslots):
            #print(slot)
            #print(template)
            template.append(list(template_dict[slot].values()))

        #print(template_resources)
        #print(template)

        # this is a numpy array of STRINGS - need to convert to ints for the booking locator.
        test = np.array(template)
        #print(test)
        #print(type(test[0][0]))

    def calc_availability(self):
        '''
        input: a BookingFilter object.  Specifically needs booking_datetime (start time),
          booking duration_hours (numpy array)
        output: numpy array of availabilities
        '''
        return

    def find_slot(self):
        '''
        input: two numpy arrays - template and resource_free (availability)
        and works out the available slots
        output: list of slots
        '''
        return 0

    def empty_fn(self):
        return "Hello from BookingFinder"

###   main() #################################################################
test_finder = BookingFinder()
test_finder.load_template('finder_template.csv')
print(test_finder.empty_fn())
