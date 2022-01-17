# analysis of MR usage
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

fname = 'mri_activity_dec_2021.csv'

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
            datetmp = ii[0:10].split('-') # date string
            timetmp = ii[11:].split(':') # time string

            datetime_tmp = datetime.datetime( int(datetmp[0]), int(datetmp[1]), int(datetmp[2]), \
                                          int(timetmp[0]), int(timetmp[1]), int(timetmp[2]) )
            self.booking_datetime.append(datetime_tmp)
            week_num.append(datetime_tmp.isocalendar()[1]) #list
        self.booking_week_num = np.array(week_num) # np array

    # calculate the total booked hours by week number within the year
    def calc_bookings_weeknum(self):
        # use lowest and highest week numbers in the data
        week_num = range(min(self.booking_week_num), max(self.booking_week_num)+1)
        booking_week_hours_true = []
        for wk in week_num:
            print(wk)
            # include hours if booking is a member of week_num
            booking_week_hours_true = np.where(self.booking_week_num == wk, \
                                               self.duration_hours, 0)
            # insert sum here....                                         
        
    def show_bookings(self):
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
#        print(range(0, len(self.duration_minutes)))
        ax1.plot(range(0, len(self.duration_minutes)) , self.duration_minutes )
#        plt.show()

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

        

dec_bookings = Booking(fname)
dec_bookings.read_csv()

prisma_west = Resource('3TW')
prisma_west.get_bookings(dec_bookings.booking_dict)
prisma_west.calc_booking_date()
prisma_west.show_bookings()
prisma_west.debug_num_fields()
prisma_west.calc_bookings_weeknum()
