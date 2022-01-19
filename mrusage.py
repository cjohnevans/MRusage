
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

#fname = 'mri_activity_dec_2021.csv'
fname = 'mri_activity_aprnov_2021.csv'


# class for a single input csv file (could be several, one month each)
class BookingSource:
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

# object containing all bookings for a given 
class BookingFilter:
    def __init__ (self, resource_name_filter, booking_status_filter):
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
 
# get the resource specific bookings
    def get_bookings(self, booking_dict):
        tmp_duration_hours = [] #list
        for row in booking_dict:
#            if row['resource'] == self.resource_name_filter:
#                if row['booking_status'] == self.booking_status_filter:
#            if self.resource_name_filter is blank, return all values
            if (self.resource_name_filter == 'all') or (row['resource'] == self.resource_name_filter):
#                print("got into resource filter")
#                print(self.resource_name_filter == 'all')
#                print(row['resource'] == self.resource_name_filter)
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
                    self.booking_description.append(row['booking_description'])
                    self.cancellation_date.append(row['cancellation_date'])
                    self.cancellation_notice_length_days.append(row['cancellation_notice_length_days'])
                    self.cancellation_notice_length_verbose.append(row['cancellation_notice_length_verbose'])
                    self.cancellation_reason.append(row['project'])
                    self.cancellation_comments.append(row['project'])
        self.duration_hours = np.array(tmp_duration_hours)
        self.calc_booking_date()
        self.project_list = set(self.project)
        print(self.project_list)

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
                print "Unrecognised date format." 
            time_tmp = ii[11:]
            time_split = time_tmp.split(':') 
            if len(time_split) == 3:
                pass
            elif len(time_split) == 2:  # handle missing ss in hh:mm format
                time_split.append('0')
            else:
                print "Unrecognised time format."
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
        booking_week_hours = []
        week_hours = []
        for wk in week_num:
            # include hours if booking is a member of week_num
            booking_week_hours = np.where(self.booking_week_num == wk, \
                                               self.duration_hours, 0)
            week_hours.append(np.sum(booking_week_hours))
        return (week_num, week_hours)

    # total the hours per project.  Can be all scanners, or scanner-specific, depending on the filter
    # applied to the BookingFilter class
    def calc_bookings_project(self):
        week_num = range(min(self.booking_week_num), max(self.booking_week_num)+1)
        booking_week_hours = []
##########  need to implement calculation by project in here #######    

        
    def debug_num_fields(self):
        num_fields = [len(self.resource_name_filter), \
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
def show_bookings_by_scanner(week_axis, hours, scanner_list, booking_status):
    nn=1
    hours_max = 0
    fig1 = plt.figure()    
    for scanner in scanner_list:
        for status in booking_status:
            if max(hours[scanner][status]) > hours_max:
                hours_max = max(hours[scanner][status])
        ax1 = fig1.add_subplot(2,2,nn)
        ax1.set_ylim(0, hours_max)
        ax1.plot(week_axis[scanner]['APPROVED'], hours[scanner]['APPROVED'], \
                                 week_axis[scanner]['CANCELLED'], hours[scanner]['CANCELLED'])
        plt.title(scanner)
        plt.legend(['Approved','Cancelled'])
        nn=nn+1
    print(hours_max)
    plt.show()  

dec_bookings = BookingSource(fname)
dec_bookings.read_csv()

scanner_list = ['3TW', '3TE', '7T', '3TM' ]
booking_status = ['APPROVED','CANCELLED']

hours = {}   # empty dict
week_axis = {}   # empty dict

for scanner in scanner_list:
    # hours is a dict where the top level key is the scanner type.  Each value is itself a dict
    # with keys APPROVED and CANCELLED, and the value associated with APPROVED or CANCELLED
    # are the hours
    hours[scanner] = {} # define each 3TE, 3TW, ... key as a dict
    week_axis[scanner]={}
    ii=1
    for status in booking_status:
        scanner_hours = BookingFilter(scanner, status)
        scanner_hours.get_bookings(dec_bookings.booking_dict)
        (wk, hrs) = scanner_hours.calc_bookings_weeknum()
        # populate a dict with the form hours[scanner][status] = [... list of hours values ...]
        hours[scanner][status] = hrs #define the booking_status key and populate values from list hrs.
        week_axis[scanner][status] = wk    

show_bookings_by_scanner(week_axis, hours, scanner_list, booking_status)

project_hours = BookingFilter('all', 'all')

