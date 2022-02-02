import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

###   BookingFinder #################################################################
class BookingFinder:
    def load_availability(self, filename):
        '''
        input:  filename of cvs in the format given by finder_template.csv
                assumes a format of 3TE,3TE,3TM,7T,operator with an (ignored) header
        output: numpy array with booking template        
        '''

        availability = [] #as list
        
        with open(filename, 'r') as csvfile:
            header = csvfile.readline().split(',')
            header = [header[idx].strip() for idx in range(0,len(header)) ]

            print('filename: ' + filename)

            csvlines = csv.reader(csvfile, delimiter=',')
            for row in csvlines:
                availability_line = [ int(resource.strip()) for resource in row ]
                availability.append(availability_line)
        availability_np = np.array(availability)
        return availability_np
     
    def load_availability_dict(self, filename):
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

    def get_availability(self, is_debug):
        '''
        input: a BookingFilter object.  Specifically needs booking_datetime (start time),
          booking duration_hours (numpy array)
               is_debug boolean.  if true load from file rather than calculate.
        output: numpy array of availabilities
        '''
        if is_debug:
            print('debug')
            resource_availability = self.load_availability('debug_availability.csv')
        else:
            # get resource_availability from BookingFinder calculation
            pass

        return resource_availability

    def find_slot(self, required, available):
        '''
        input: two numpy arrays - required (template requirement) and available (from bookings)
        and works out the available slots
        output: list of slots
        '''

        print(required)
        print(available)
        fig, ax = plt.subplots()
        ax.imshow(available, cmap='gray')
        plt.show()
        
        return 



###   main() #################################################################
test_finder = BookingFinder()
template = test_finder.load_availability('template_availability.csv')
resource = test_finder.get_availability(True)
#need some error trapping here
test_finder.find_slot(template, resource)

