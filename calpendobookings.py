import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt

#### class BookingSource ############################################################################
# class for a single input csv file (could be several, each with different timespan)
class BookingSource:
    def __init__ (self, filename) :
        # lists, with values from each booking
        self.booking = []
        self.filename = filename
        self.read_csv()

    # read csv data 
    def read_csv(self):
        print('filename: ' + self.filename)
        with open(self.filename, 'r') as csvfile:
            csvread = csv.DictReader(csvfile)
            for row in csvread:
                self.booking.append(row)

#### class BookingFilter ############################################################################
# object containing all bookings for a given filter
# for example, all APPROVED bookings on 3TW
class BookingFilter:
    def __init__ (self, source_bookings, resource_name_filter, booking_status_filter):
        # variables are lists with [variable_booking1, variable_booking2, ...]
        self.resource_name_filter = resource_name_filter
        self.booking_status_filter = booking_status_filter
        self.resource = []
        self.project = []
        self.booking_status = []
        self.booker = []
        self.owner = []
        self.project_type = []
        self.booking_type = []
        self.repeat_type = []
        self.start_date = []
        self.finish_date = []
        self.duration_minutes = []
        self.duration_hours = []
        self.booking_description = []
        self.cancellation_date = []
        self.cancellation_notice_length_days = []
        self.cancellation_notice_length_verbose = []
        self.cancellation_reason = []
        self.cancellation_comments = []
        self.booking_datetime = []  # list of datetime objects
        self.booking_week_num = []
        self.project_list = [] #set with unique project names
        self.start_duration = [] #list of tuples with (starttime, duration)
        #setup functions
        self.get_bookings(source_bookings)
        self.calc_booking_date()
 
    # popluate the variable in BookingFilter class, from bookings matching the filter.
    def get_bookings(self, source_bookings):
        '''
        input:   source_bookings from BookingSource
        
        output:  populate the booking info in the BookingFilter object, subject to matching
                   the appropriate filters (resource, status)

        todo:    add time filter to set a date range of bookings to return
        '''
        tmp_duration_hours = [] #list
        for row in source_bookings:
            # include booking if resource matches the filter of if resource set to 'all'
            if (self.resource_name_filter == 'all') or (row['resource'] == self.resource_name_filter):
                # include booking if status matches filter or if booking is set to 'all'
                if (self.booking_status_filter == 'all') or (row['booking_status'] == self.booking_status_filter):
                    self.start_date.append(row['start_date'])
                    self.project.append(row['project'])
                    self.booking_status.append(row['booking_status'])
                    self.booker.append(row['booker'])
                    self.owner.append(row['owner'])
                    self.project_type.append(row['project_type'])
                    self.booking_type.append(row['booking_type'])
                    self.repeat_type.append(row['repeat_type'])
                    self.finish_date.append(row['finish_date'])
                    self.duration_minutes.append(row['duration_minutes']) # str
                    tmp_duration_hours.append(float(row['duration_minutes'])/60.0) #list
                    if 'booking_description' in row:
                        self.booking_description.append(row['booking_description'])
                    elif 'description' in row:
                        self.booking_description.append(row['description'])                        
                    self.cancellation_date.append(row['cancellation_date'])
                    self.cancellation_notice_length_days.append(row['cancellation_notice_length_days'])
                    self.cancellation_notice_length_verbose.append(row['cancellation_notice_length_verbose'])
                    self.cancellation_reason.append(row['project'])
                    self.cancellation_comments.append(row['project'])
        self.duration_hours = np.array(tmp_duration_hours)
        self.project_list = set(self.project)

    # May need to repeat this for start and end dates.  Could make this a fn which has the list start_date (or end_date)
    # passed to it, and it returns the (i) booking date in datetime format, and (ii) the booking week no.
    # i.e. in get_bookings: self.booking_datetime = calc_booking_date(self.start_date)
    def calc_booking_date(self):
        # take date part and split y, m, d
        week_num = [] # as list
        for ii in self.start_date:
            date_tmp = ii[0:10]
            if '-' in date_tmp:  # yyyy-mm-dd format
                date_split = date_tmp.split('-') # date string
            elif '/' in date_tmp: # dd/mm/yyy format
                date_split_rev = date_tmp.split('/')
                date_split = date_split_rev[::-1] #reverse
            else:
                print("Unrecognised date format.") 
            time_tmp = ii[11:]
            time_split = time_tmp.split(':') 
            if len(time_split) == 3:
                pass
            elif len(time_split) == 2:  # handle missing ss in hh:mm format
                time_split.append('0')
            else:
                print("Unrecognised time format.")
            # date_split needs to be [yyyy, mm, dd]
            datetime_tmp = datetime.datetime( int(date_split[0]), int(date_split[1]), int(date_split[2]), \
                                          int(time_split[0]), int(time_split[1]), int(time_split[2]) )    
            self.booking_datetime.append(datetime_tmp)
            week_num.append(datetime_tmp.isocalendar()[1]) #list
        self.booking_week_num = np.array(week_num) # np array


        ######### this logic isn't right.  
        intduration = [ int(dur) for dur in self.duration_minutes ]  #ok
        #### next line needs to iterate across all items
        self.start_duration.append( tuple(zip(self.booking_datetime, intduration )))



        print('self_duration', len(self.start_duration))

    # total the hours per project.  Can be all resources, or resource-specific, depending on the filter
    # applied to the BookingFilter class
    def calc_bookings_project(self):
        week_num = range(min(self.booking_week_num), max(self.booking_week_num)+1)
        booking_week_hours = []
        ##########  need to implement calculation by project in here #######

#### class BookingAnalyse #####################################################
# object to analyse the data recovered from BookingFilter.
class BookingAnalyse:
    def __init__(self, res):
        self.resource = res
        self.week_num = []
        self.week_hours = []
    
    def calc_bookings_weeknum(self, booking_filter_list):
        # use lowest and highest week numbers in the data
        if(not np.any(booking_filter_list.booking_week_num)):
            return([], []) # return empty lists for week_num and week_hours if no bookings match the filter.
        week_num = range(min(booking_filter_list.booking_week_num), max(booking_filter_list.booking_week_num)+1)
        booking_week_hours = []
        week_hours = []
        for wk in week_num:
            # include hours if booking is a member of week_num
            booking_week_hours = np.where(booking_filter_list.booking_week_num == wk, \
                                               booking_filter_list.duration_hours, 0)
            week_hours.append(np.sum(booking_week_hours))
        self.week_num = week_num
        self.week_hours = week_hours
        self.calc_stats()

    def calc_availability(self, flt):
        '''
        based on the filter_list, calculate the availability in blocks
        '''
        time_block_length = 30 # mins
        ignore_weekends = True
        start_hour_limit = 9   # ignore hours before this
        end_hour_limit = 18  # ignore hours after this
        print(flt.booking_datetime)
        print(flt.duration_minutes)

        slot_available = np.array([]) # n_slots x n_resources array of availability (0,1)
        full_slot = []   # list of full slots

        # populate the full_slot array
        # need to work this out in integer slots
        if(ignore_weekends):
            max_day = 5
        else:
            max_day = 7
        print('max_day',max_day)

        new_min = 0
        for (bk, dur) in flt.start_duration:
            print(bk, dur)
            # logic to populate full_slot array goes here
            # step 1 - greedy slot.  make sure full 30min slot is marked 'full'
            if bk.minute < 30:  #before half past
                new_min = 0
            else:    # after half past
                new_min = 30
            print(bk.weekday(), bk.hour, bk.minute, '       ', bk.hour, new_min)   
            bk_start = datetime.datetime(bk.year, bk.month, bk.day, bk.hour, new_min)
            print(bk_start)

# not sure I'll need this, but keep the logic for now
#            if bk.weekday() < max_day: # ignore weekends
#                if bk.hour >= start_hour_limit and bk.hour <= end_hour_limit:   # ignore out of hours



    def calc_stats(self):
        self.week_hour_avg = np.mean(self.week_hours)
        self.week_hour_stdev = np.std(self.week_hours)
        self.week_hour_max = np.amax(self.week_hours)
        self.week_hour_min = np.amin(self.week_hours)
        print('----------------------')
        print(self.resource)
        print('Average Hrs/wk', self.week_hour_avg)
        print('StdDev  Hrs/wk', self.week_hour_stdev)
        print('Maximum Hrs/wk', self.week_hour_max)
        print('Minimum Hrs/wk', self.week_hour_min)

    def plot_hours(self):
        hours_max = 60 # default to 60hours max
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.set_ylim(0, hours_max)
        ax1.bar(self.week_num, self.week_hours)
        plt.title(self.resource)
        plt.savefig('output/' + self.resource )
