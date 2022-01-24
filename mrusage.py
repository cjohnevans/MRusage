
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np

#fname = 'mri_activity_dec_2021.csv'
#fname = 'mri_activity_aprnov_2021.csv'
fname = 'mri_activity_2021aprdec_all.csv'


#### class BookingSource ############################################################################
# class for a single input csv file (could be several, each with different timespan)
class BookingSource:
    def __init__ (self, filename) :
        # lists, with values from each booking
        self.booking_dict = []
        self.filename = filename

    # read csv data 
    def read_csv(self):
        print('filename: ' + self.filename)
        with open(self.filename, 'r') as csvfile:
            csvread = csv.DictReader(csvfile)
            for row in csvread:
                self.booking_dict.append(row)

#### class BookingFilter ############################################################################
# object containing all bookings for a given filter
# for example, all APPROVED bookings on 3TW
class BookingFilter:
    def __init__ (self, resource_name_filter, booking_status_filter):
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
 
    # popluate the variable in BookingFilter class, from bookings matching the filter.
    def get_bookings(self, booking_dict):
        tmp_duration_hours = [] #list
        for row in booking_dict:
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
        self.calc_booking_date()
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
            #print(week_num)
        self.booking_week_num = np.array(week_num) # np array

    # total the hours per project.  Can be all resources, or resource-specific, depending on the filter
    # applied to the BookingFilter class
    def calc_bookings_project(self):
        week_num = range(min(self.booking_week_num), max(self.booking_week_num)+1)
        booking_week_hours = []
        ##########  need to implement calculation by project in here #######

#### class BookingAnalyse #####################################################
# object to analyse the data recovered from BookingFilter.
class BookingAnalyse:
    def __init__(self, booking_filter_list):
        print(booking_filter_list)
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
        return (week_num, week_hours)
    
    def show_bookings_by_resource(self, resource_list, booking_status, plot_rows, plot_cols):
        nn=1
        hours_max = 60 # default to 60hours max
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(plot_rows,plot_cols,nn)
        ax1.set_ylim(0, hours_max)
        ax1.plot(self.week_num, self.week_hours, \
                                 self.week_num, self.week_hours)
        plt.title(resource)
        if(nn == 1):
            plt.legend(['Approved','Cancelled'])
        nn=nn+1
        plt.show()

###   Placeholder for  def calc_bookings_project(self): ##################################
#    def calc_bookings_project(self):


#### main() ##############################################################################

dec_bookings = BookingSource(fname)
dec_bookings.read_csv()

resource_list = ['3TE', '3TW', '7T', '3TM', 'Peter Hobden', 'Allison Cooper', 'Sonya Foley', 'John Evans'  ]
booking_status = ['APPROVED','CANCELLED']

hours = {}   # empty dict
week_axis = {}   # empty dict

for resource in resource_list:
    # hours is a list of dicts where the list is by resource type.  Each element in the list is a dict
    # with keys APPROVED and CANCELLED, and the value associated with APPROVED or CANCELLED
    # are the hours
    hours[resource] = {} # define each 3TE, 3TW, ... key as a dict
    week_axis[resource]={}
    ii=1
    for status in booking_status:
        booking_list = BookingFilter(resource, status)  #redefinition of booking_list here - is this OK?
        booking_list.get_bookings(dec_bookings.booking_dict)
        booking_analysis = BookingAnalyse(booking_list)
        (wk, hrs) = booking_analysis.calc_bookings_weeknum(booking_list)
        booking_analysis.show_bookings_by_resource(resource_list, booking_status,2,4)
        # populate a dict with the form hours[resource][status] = [... list of hours values ...]
        hours[resource][status] = hrs #define the booking_status key and populate values from list hrs.
        week_axis[resource][status] = wk    

#show_bookings_by_resource(resource_list, booking_status,2,4)

