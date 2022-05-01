import finder

###   main() #################################################################
slots_wk = 2 * 9 * 5  # slots/hr * hours/day * days/wk
n_weeks = 26

test_finder = finder.BookingFinder()
#load the required schedule
required = test_finder.load_schedule('required_schedule.csv')

resource = test_finder.get_schedule('random')
#resource = test_finder.get_schedule('csv')

#need some error trapping here
#test_finder.plot_schedule(resource, slots_wk, n_weeks )
# this returns a list of 1/0 values indicating whether the availability
# of resources at the slot match the requirement
found_slot = test_finder.find_slot(required, resource)
test_finder.summarise(required, found_slot)
test_finder.plot_matches(resource, required, found_slot, slots_wk, n_weeks )
#test_finder.random_schedule(100)
