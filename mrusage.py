
# next - plotting of summary data...

import csv
import matplotlib.pyplot as plt
#import datetime
import numpy as np
import finder
import calpendobookings as cal

#fname = 'mri_activity_dec_2021.csv'
#fname = 'mri_activity_aprnov_2021.csv'
# this is the utf-8 encoded version:
fname = 'mri_activity_2021aprdec_all_b.csv'

        
#### main() ##############################################################################
#  this spans multiple resources, across multiple classes, so doesn't fit in BookingAnalyse...
def bookings_stacked_bar(x_data, y_data, figfname, title):
    '''
    stacked bar plot of x_data vs y_data.  both x_data and y_data are dicts with resource titles as keys.
    '''
    hours_max = 120 # default max
    x_axis_points = 0

    for series in x_data.keys():
        temp = len(x_data[series])
        if temp > x_axis_points:
            x_axis_points = temp

    start_height = [0] * x_axis_points  # list of zeroes with length x_axis_points  

    fig, ax = plt.subplots()
    ax.set_ylim(0, hours_max)
    for series in x_data.keys():
        ax.bar(x_data[series] , y_data[series], bottom = start_height)
        # work out starting point for next bar series, by list comprehension.
        start_height = [start_height[jj] + y_data[series][jj] for jj in range(len(start_height))]
    plt.legend(x_data.keys())
    plt.title(title)
#    plt.show(block=False)
    plt.savefig('output/' + figfname)

cal_bookings = cal.BookingSource(fname)

#resource_list = ['3TE', '3TW', '7T', '3TM', 'Peter Hobden', 'Allison Cooper', 'Sonya Foley', 'John Evans'  ]
scanner_list = ['3TE', '3TW', '7T', '3TM']
#operator_list = [ 'Peter Hobden', 'Allison Cooper', 'Sonya Foley', 'John Evans' ]
operator_list = [ 'Peter Hobden', 'Allison Cooper']
booking_status = ['APPROVED','CANCELLED']
resource_list = scanner_list

hours = {}   # empty dict
week_axis = {}   # empty dict
booking_list_approved = {}  # a dict of BookingFilter object
booking_analysis_approved = {}   # a list of BookingAnalysis objects
booking_list_cancelled = {}  # a dict of BookingFilter objects
booking_analysis_cancelled = {}   # a list of BookingAnalysis objects

for resource in resource_list:
    # calls get_bookings function from the resource-specific instance of the BookingFilter class
    # booking_list_approved.
    booking_list_approved[resource] = cal.BookingFilter(cal_bookings.booking, resource, 'APPROVED')
    booking_analysis_approved[resource] = cal.BookingAnalyse(resource)
    booking_analysis_approved[resource].calc_bookings_weeknum(booking_list_approved[resource])
    booking_list_cancelled[resource] = cal.BookingFilter(cal_bookings.booking, resource, 'CANCELLED')
    booking_analysis_approved[resource].plot_hours()

# dict comprehension - assign values to a local variables for plotting.  Can pass this as a single dict to plotting fn.
scanner_stacked_axes = { resource: booking_analysis_approved[resource].week_num for resource in resource_list }
scanner_stacked_hours = { resource: booking_analysis_approved[resource].week_hours for resource in resource_list }
bookings_stacked_bar(scanner_stacked_axes, scanner_stacked_hours,\
                     'ScannerHours.png','Hours booked per week, by scanner')

operator_booking = {}
operator_analysis = {}
for resource in operator_list:
    # calls get_bookings function from the resource-specific instance of the BookingFilter class
    # booking_list_approved.
    operator_booking[resource] = cal.BookingFilter(cal_bookings.booking, resource, 'APPROVED')
    operator_analysis[resource] = cal.BookingAnalyse(resource)
    operator_analysis[resource].calc_bookings_weeknum(operator_booking[resource])
    operator_analysis[resource].plot_hours()

operator_stacked_axes = { resource: operator_analysis[resource].week_num for resource in operator_list }

operator_stacked_hours = { resource: operator_analysis[resource].week_hours for resource in operator_list }
bookings_stacked_bar(operator_stacked_axes, operator_stacked_hours, \
                     'OperatorHours.png', 'Hours booked per week, by operator')



