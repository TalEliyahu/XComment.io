# SOURCE: https://wiki.python.org/moin/SimplePrograms

from time import localtime # this is how you're supposed to import stuff

activities = {8: 'Sleeping',
              9: 'Commuting',
              17: 'Working',
              18: 'Commuting',
              20: 'Eating',
              22: 'Resting' }

time_now = localtime()
# What we got here?!
# Yet another comment
# pretending to be
# a multiline one!
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    # Branching is about to start...
    if hour < activity_time: # Yes, sir, we're already here!
        print activities[activity_time]
        break
else:
    # else'ty!
    print 'Unknown, AFK or sleeping!'

# Gosh! That was tough! :)
