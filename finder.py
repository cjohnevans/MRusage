import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import random as rnd

###   BookingFinder #################################################################
class BookingFinder:
    def load_schedule(self, filename):
        '''
        input:  filename of cvs with 3TE,3TE,3TM,7T,operator with an (ignored) header
        output: numpy array with schedule (which could be an availability or a requirement)
        '''

        schedule = [] #as list

        with open(filename, 'r') as csvfile:
            header = csvfile.readline().split(',')
            header = [header[idx].strip() for idx in range(0,len(header)) ]

            print('filename: ' + filename)

            csvlines = csv.reader(csvfile, delimiter=',')
            for row in csvlines:
                if row:    #trap empty lines
                    schedule_line = [ int(resource.strip()) for resource in row ]
                    schedule.append(schedule_line)
        schedule_np = np.array(schedule)
        #print(availability_np)
        return schedule_np

    def random_schedule(self, n_slots):
        '''
        generate a random schedule of 5 resources x n_slots
        '''
        n_resources = 5
        occupancy = [0.5, 0.5, 0.5, 0.5, 0.5]  # proby of being occupied
        available = np.zeros((n_slots, n_resources))
        
        for resource in range(n_resources):
            for slot in range(n_slots):
                if rnd.random() > occupancy[resource]:
                    available[slot][resource] = 0  #not available if occupied
                else:
                    available[slot][resource] = 1  #available if not occupied
        print(np.shape(available))
        print(np.sum(available))
        return available

    def get_schedule(self, method):
        '''
        input: a BookingFilter object.  Specifically needs booking_datetime (start time),
          booking duration_hours (numpy array)
               method = 'finder', 'csv' or 'random' (string)
        output: numpy array of availabilities
        '''
        if method == 'csv':
            print('debug')
            resource_availability = self.load_schedule('debug_availability.csv')
        elif method == 'random':
            nslots = 200
            resource_availability = self.random_schedule(nslots)
        else:  #assume 'finder'
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
#load the required schedule
required = test_finder.load_schedule('required_schedule.csv')

# works for csv, not for random
#resource = test_finder.get_schedule('random')
resource = test_finder.get_schedule('csv')

#need some error trapping here
#test_finder.plot_schedule(resource, slots_wk, n_weeks )
# this returns a list of 1/0 values indicating whether the availability
# of resources at the slot match the requirement
found_slot = test_finder.find_slot(required, resource)
test_finder.plot_matches(resource, required, found_slot, slots_wk, n_weeks )
#test_finder.random_schedule(100)
