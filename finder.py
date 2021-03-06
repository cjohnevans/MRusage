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
        p_availability = [1, .5, .5, .5 ,1]  # proby of being available

        available = np.zeros((n_slots, n_resources))

        for resource in range(n_resources):
            for slot in range(n_slots):
                aa=rnd.random()
                if aa < p_availability[resource]:
                    available[slot][resource] = 1
                else:
                    available[slot][resource] = 0
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
            nslots = 1800 #20 weeks
            resource_availability = self.random_schedule(nslots)
        else:  #assume 'finder'
            # get resource_availability from BookingFinder calculation
            pass
        #  need to add unavailable hours at the end of each day to prevent
        #  bookings crossing overnight.
        return resource_availability

    def plot_schedule(self, fname, available, n_rows, n_weeks):
        '''
        input:   available (the availability matrix from all resources)
                 n_rows - the number of rows in plot (typically the slots_per_week)
                 n_weeks - no of weeks to plot. total columns will be
                   n_weeks * n_resources
        output:  plot of availabilty, formatted to columns of slots making up
                 one week, one column per resource
        '''
        av_rows, av_cols = available.shape
        avail_spaced = np.pad(available, ((0,0), (0,1)), mode='constant') #pad one col of zeroes, for clarity
        n_cols = (av_cols+1)*n_weeks  # n_cols = total n columns in plot
        # a block is an n_rows * (no of resources + 1) block of availability data, for
        # reshaping to a more convenient image to display.
        # floor division to find number of blocks fully populated with availability data
        full_blocks = av_rows // n_rows
#        print('full_blocks', full_blocks)

        if full_blocks > 0:
            block_no = 0
            stacked_full_blocks = np.array([])
            rows_in_stacked_full_blocks = full_blocks*n_rows
            while block_no < full_blocks:
#                print('block_no', block_no)
                if block_no == 0:  # first pass:  set stacked_full_blocks explicitly
                    stacked_full_blocks = np.array( avail_spaced[0:n_rows][:] )
#                    print('stacked_full_blocks.shape', stacked_full_blocks.shape)
                else:  # subsequent passes, append to existing stacked_full_blocks
#                    print('block_no', block_no, 'n_rows', n_rows)
                    new_block = np.array(avail_spaced[ (block_no * n_rows) : (block_no+1)*n_rows ][:])
#                    print('new_block shape ', new_block.shape)
#                    print('stacked_full_blocks.shape', stacked_full_blocks.shape)
                    stacked_full_blocks = np.append(stacked_full_blocks, new_block, axis=1)
                block_no += 1
            avail_part = avail_spaced[rows_in_stacked_full_blocks:][:] # the remainder
        else:       # no full cols, so just the 'remainder'
            stacked_full_blocks = []
            avail_part = avail_spaced

        av_part_rows, av_part_cols = avail_part.shape
        pad_rows = n_rows - av_part_rows
        pad_cols = n_cols - av_part_cols
#        print('avail_part_r', av_part_rows, 'avail part col', av_part_cols, 'pad rows ', pad_rows, 'pad cols ', pad_cols)
        avail_part_pad = np.pad(avail_part, ((0,pad_rows), (0,n_cols)), mode='constant' )
        # append the (padded) partially filled columns to the full columns
#        print('aval_full', stacked_full_blocks.shape, 'avail_part_pad',avail_part_pad.shape)
        if len(stacked_full_blocks) == 0:
            plot_avail = avail_part_pad
        else:
            plot_avail = np.append(stacked_full_blocks, avail_part_pad, axis=1)
        fig, ax = plt.subplots()
        ax.imshow(plot_avail, cmap='gray')
        plt.savefig('output/' + fname, dpi=720)

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
        slot=0

        while slot <= (avail_slots - reqd_slots):
            if match[slot] == 1:
                match_img[slot:(slot+reqd_slots)][:] = required
#                print('match_img for slot ', slot)
#                print(match_img[slot:(slot+reqd_slots)][:])
            slot += 1

        match_avail_img = match_img + available # add match to available to highlight matches
        # fig, ax = plt.subplots()
        # ax.imshow(match_avail_img, cmap='gray')
        # plt.show()
        # plt.close(fig)
        self.plot_schedule('availability_img.tiff', available, n_rows, n_weeks)
        self.plot_schedule('match_img.tiff', match_avail_img, n_rows, n_weeks)

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
        plt.savefig('output/match_plot.png')
        return match

    def summarise(self, template, match):
        print('Booking template is:')
        print(template)
        print('Found ', np.sum(match), ' out of ', len(match), ' slots')
        print('or ', (np.sum(match) / (len(match)/90) ), ' slots per week')
        

