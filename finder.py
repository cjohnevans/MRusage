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
                if row:    #trap empty lines
                    availability_line = [ int(resource.strip()) for resource in row ]
                    availability.append(availability_line)
        availability_np = np.array(availability)
        #print(availability_np)
        return availability_np

    # def load_availability_dict(self, filename):
    #     '''
    #     input:  filename of cvs in the format given by booking_template.csv
    #             loads template as dict
    #     output: numpy array with booking template
    #     NOT WORKING
    #     '''
    #     template_dict = []  # dictionary version, from csv file
    #     template = [] #list/numpy array? for use in the optimiser/locator
    #
    #     print('filename: ' + filename)
    #     with open(filename, 'r') as csvfile:
    #         # need the next few lines to deal with whitespaces in key.  Explicitly send this to DictReader
    #         header = csvfile.readline().split(',')
    #         header = [header[idx].strip() for idx in range(0,len(header)) ]
    #         for res in header:
    #             print(res)
    #         csvread = csv.DictReader(csvfile, fieldnames=header)
    #         for row in csvread:
    #             tmp=list(row.values())
    #             # still not there with the typing:  this gets it into a LIST of INTs
    #             print(tmp[1])
    #             print(int(tmp[1]))
    #             template_dict.append(row) #as a dictionary
    #
    #     # express as lists
    #     nslots = len(template_dict)
    #     template_resources = header
    #     for slot in range(0,nslots):
    #         #print(slot)
    #         #print(template)
    #         template.append(list(template_dict[slot].values()))
    #
    #     #print(template_resources)
    #     #print(template)
    #
    #     # this is a numpy array of STRINGS - need to convert to ints for the booking locator.
    #     test = np.array(template)
    #     #print(test)
    #     #print(type(test[0][0]))

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
        #  need to add unavailable hours at the end of each day to prevent
        #  bookings crossing overnight.

        return resource_availability

    def plot_schedule(self, available, n_rows, n_weeks):
        '''
        input:   available (the availability matrix from all resources)
                 n_rows - the number of rows in plot (typically the slots_per_week)
                 n_weeks - no of weeks to plot. total columns will be
                   n_weeks * n_resources
        output:  plot of availabilty, formatted to columns of slots making up
                 one week, one column per resource
        '''
        print(available.shape)
        av_rows, av_cols = available.shape
        n_cols = av_cols*n_weeks  # n_cols = total n columns in plot
        # floor division to find cols fully populated with availability data
        full_columns = av_rows // n_rows
        if full_columns > 0:
            n_avail_rows_in_full = full_columns*n_rows
            avail_full = available[:n_avail_rows_in_full][:]  #just take fully-populated n_cols
            avail_part = available[n_avail_rows_in_full:][:] # the remainder
        else:       # no full cols, so just the 'remainder'
            avail_full = []
            avail_part = available

        av_part_rows, av_part_cols = avail_part.shape
        pad_rows = n_rows - av_part_rows
        pad_cols = n_cols - av_part_cols
        print('avail_part_r', av_part_rows, 'avail part col', av_part_cols, 'pad rows ', pad_rows, 'pad cols ', pad_cols)
        avail_part_pad = np.pad(avail_part, ((0,pad_rows), (0,n_cols)), mode='constant' )
        # append the (padded) partially filled columns to the full columns
        if avail_full == []:
            plot_avail = avail_part_pad
        else:
            plot_avail = np.append(avail_full, avail_part_pad, axis=1)
        fig, ax = plt.subplots()
        ax.imshow(plot_avail, cmap='gray')
        plt.show()

    def plot_matches(self, available, required, match, n_rows, n_weeks):
        '''
        input: available (the availability matrix from all resources)
               required (the template matrix of required resources)
               match (list of whether template matches available, for each slot)
               n_rows - the number of rows in plot (typically the slots_per_week)
               n_weeks - no of weeks to plot. total columns will be
                  n_weeks * n_resources
        output:  plot of availabilty, formatted to columns of slots making up
                 one week, one column per resource 
        '''
        reqd_slots, reqd_resources = required.shape  # (slot, resource)
        avail_slots, avail_resources = available.shape # (slot, resource)
        blank = np.zeros(available.shape )
        match_img = blank
        print("blank shape ", blank.shape)
        slot=0

        while slot <= (avail_slots - reqd_slots):
            if match[slot] == 1:
                match_img[slot:(slot+reqd_slots)][:] = required
            slot += 1

        match_avail_img = match_img + available # add match to available to highlight matches
       
        self.plot_schedule(match_avail_img, n_rows, n_weeks)
        
    def find_slot(self, required, available):
        '''
        input: two numpy arrays - required (template requirement) and available (from bookings)
        and works out the available slots
        output: list of slots
        #  plan: (i) slice out part of available array
        #        (ii) multiply by required array to give avail_x_reqd
        #        (iii)  if all required slots are available, then the sum of all elements
        #               in avail_x_reqd will be the same as the sum of all elements in
        #               required array.  Sum will be less if any slots are 'missing'

        # general syntax is;
        #  availablity (or av, avail) = when resource is free
        #  template = the required availability template
        #  match = when template matches availability
        '''

        reqd_slots, reqd_resources = required.shape
        avail_slots, avail_resources = available.shape
        sum_required = np.sum(required)  # total slots required for a booking, across all resources
        slot = 0
        sum_avail_x_reqd = []
        match = []
        while slot <= (avail_slots - reqd_slots):
            avail_part = available[slot:(slot+reqd_slots)][:]
            avail_x_reqd = np.multiply(avail_part, required)
            sum_avail_x_reqd.append(np.sum(avail_x_reqd))
            if sum_avail_x_reqd[slot] == sum_required:
                match.append(1)
            else:
                match.append(0)
            slot = slot + 1

        print("Found ", np.sum(np.array(match)), " slots")
        fig, ax = plt.subplots()
        ax.bar(range(len(match)), match)
        plt.show()
        return match

###   main() #################################################################
slots_wk = 2 * 9 * 5  # slots/hr * hours/day * days/wk
n_weeks = 26

test_finder = BookingFinder()
required = test_finder.load_availability('template_availability.csv')
resource = test_finder.get_availability(True)
print(resource.shape)
#need some error trapping here
#test_finder.plot_schedule(resource, slots_wk, n_weeks )
# this returns a list of 1/0 values indicating whether the availability
# of resources at the slot match the requirement
found_slot = test_finder.find_slot(required, resource)
test_finder.plot_matches(resource, required, found_slot, slots_wk, n_weeks )
