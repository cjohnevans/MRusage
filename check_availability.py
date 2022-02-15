import calpendobookings as cal

fname = 'mri_activity_2021aprdec_all_b.csv'
book_src = cal.BookingSource(fname) #source
book_flt = {}   #filter
book_ana = {}   #analysis
print(book_src.filename)

#scanner_list = ['3TE', '3TW', '7T', '3TM']
scanner_list = ['3TE']

for x in scanner_list:
    book_flt[x] = cal.BookingFilter(book_src.booking, x, 'APPROVED')
    book_ana[x] = cal.BookingAnalyse(x)
    book_ana[x].calc_availability(book_flt[x])
