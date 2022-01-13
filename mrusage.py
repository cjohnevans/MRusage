# analysis of MR usage
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt

fname = 'mri_activity_dec_2021.csv'

# class for a single input csv file (could be several, one month each)
class Booking:
    def __init__ (self, filename) :
        # lists, with values from each booking
        self.booking_dict = []
        self.filename = filename
        print self.filename
        
    def read_csv(self):
# read csv data into dict_import
        print 'filename: ' + self.filename
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
        self.booking_description = []
        self.cancellation_date = []
        self.cancellation_notice_length_days = []
        self.cancellation_notice_length_verbose = []
        self.cancellation_reason = []
        self.cancellation_comments = []

# get the resource specific bookings
    def get_bookings(self, booking_dict):
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
                self.start_date.append(row['start_date'])
                self.finish_date.append(row['finish_date'])
                self.duration_minutes.append(int(row['duration_minutes']))
                self.booking_description.append(row['booking_description'])
                self.cancellation_date.append(row['cancellation_date'])
                self.cancellation_notice_length_days.append(row['cancellation_notice_length_days'])
                self.cancellation_notice_length_verbose.append(row['cancellation_notice_length_verbose'])
                self.cancellation_reason.append(row['project'])
                self.cancellation_comments.append(row['project'])

                self.date_yymmdd = []

    def calc_datetime(self):
        # take date part and split y, m, d
        for ii in self.start_date:
            datetmp = ii[0:10].split('-') # string
            datetmp2 = []
            for jj in datetmp:
                datetmp2.append(int(jj))
            print datetmp
            print type(datetmp)
            self.date_yymmdd.append(datetmp2)
        
    def show_bookings(self):
        print self.project[2]
        print self.start_date
        print self.duration_minutes
        print self.date_yymmdd

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        print(range(0, len(self.duration_minutes)))
        ax1.plot(range(0, len(self.duration_minutes)) , self.duration_minutes )
        plt.show()


dec_bookings = Booking(fname)
dec_bookings.read_csv()

prisma_west = Resource('3TW')
prisma_west.get_bookings(dec_bookings.booking_dict)
prisma_west.calc_datetime()
prisma_west.show_bookings()
