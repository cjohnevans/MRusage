# analysis of MR usage
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

#fname = 'mri_activity_dec_2021.csv'
fname = 'mri_activity_aprnov_2021.csv'


# class for a single input csv file (could be several, one month each)
class Booking:
    def __init__ (self, filename) :
        # lists, with values from each booking
        self.booking_dict = []
        self.filename = filename
        
    def read_csv(self):
# read csv data into dict_import
        print('filename: ' + self.filename)
        with open(self.filename, 'r') as csvfile:
            csvread = csv.DictReader(csvfile)
            for row in csvread:
                self.booking_dict.append(row)

# needs to take the resulting dict, from possible multiple csv files, but resource
# and generate a resource specific dict.
class Resource:
    def __init__ (self, resource_name):
        self.resource_name = resource_name
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

# get the resource specific bookings
    def get_bookings(self, booking_dict):
        tmp_duration_hours = [] #list
        for row in booking_dict:
            if row['resource'] == self.resource_name:
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
                self.booking_description.append(row['booking_description'])
                self.cancellation_date.append(row['cancellation_date'])
                self.cancellation_notice_length_days.append(row['cancellation_notice_length_days'])
                self.cancellation_notice_length_verbose.append(row['cancellation_notice_length_verbose'])
                self.cancellation_reason.append(row['project'])
                self.cancellation_comments.append(row['project'])
        self.duration_hours = np.array(tmp_duration_hours)

    def calc_booking_date(self):
        # take date part and split y, m, d
        week_num = [] # as list
        for ii in self.start_date:
            date_tmp = ii[0:10]
            print date_tmp
            if '-' in date_tmp:  # yyyy-mm-dd format
                print "yyyy-mm-dd format"
                date_split = date_tmp.split('-') # date string
            elif '/' in date_tmp: # dd/mm/yyy format
                print "dd/mm/yyyy format"
                date_split_rev = date_tmp.split('/')
                date_split = date_split_rev[::-1] #reverse
            else:
                print "dunno" 
            time_tmp = ii[11:]
            time_split = time_tmp.split(':') 
            if len(time_split) == 2:  # handle missing ss in hh:mm format
                time_split.append('0')
            # date_split needs to be [yyyy, mm, dd]
            datetime_tmp = datetime.datetime( int(date_split[0]), int(date_split[1]), int(date_split[2]), \
                                          int(time_split[0]), int(time_split[1]), int(time_split[2]) )    
            self.booking_datetime.append(datetime_tmp)
            week_num.append(datetime_tmp.isocalendar()[1]) #list
        self.booking_week_num = np.array(week_num) # np array

    # calculate the total booked hours by week number within the year
    def calc_bookings_weeknum(self):
        # use lowest and highest week numbers in the data
        week_num = range(min(self.booking_week_num), max(self.booking_week_num)+1)
        booking_week_hours_true = []
        week_hours = []
        for wk in week_num:
            # include hours if booking is a member of week_num
            booking_week_hours_true = np.where(self.booking_week_num == wk, \
                                               self.duration_hours, 0)
            week_hours.append(np.sum(booking_week_hours_true))
        return (week_num, week_hours)
        
    def debug_num_fields(self):
        num_fields = [len(self.resource_name), \
                      len(self.resource),\
                      len(self.project),\
                      len(self.booking_status),\
                      len(self.booker),\
                      len(self.owner), \
                      len(self.project_type), \
##        self.booking_type
##        self.repeat_type
                      len(self.start_date), \
##        self.finish_date
                      len(self.duration_minutes),\
                      len(self.duration_hours), \
                      len(self.booking_description), \
##        self.cancellation_date
##        self.cancellation_notice_length_days
##        self.cancellation_notice_length_verbose
##        self.cancellation_reason
##        self.cancellation_comments
##        self.booking_datetime
##        self.booking_week_num
                      ]
        print("debug_num_fields " + str(num_fields))

#currently local.  should be a new class for summary data?
def show_bookings(date_axis, duration):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot(date_axis , duration )
    plt.show()        

dec_bookings = Booking(fname)
dec_bookings.read_csv()

prisma_west = Resource('3TW')
prisma_west.get_bookings(dec_bookings.booking_dict)
prisma_west.calc_booking_date()
prisma_west.debug_num_fields()
(wk, hrs) = prisma_west.calc_bookings_weeknum()
show_bookings(wk, hrs)
