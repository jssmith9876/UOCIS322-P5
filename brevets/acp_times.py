"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


"""
For arrow:
   use .shift to alter the date
   => arrow.now().shift(days=+3) returns the date 3 days from now
   => arrow.now().shift(minutes=-10) returns the date 10 minutes ago
"""

intervals = [0, 200, 400, 600, 1000]
max_speed = [34, 32, 30, 28, 26]
min_speed = [15, 15, 15, 11.428, 13.333]

def get_final(total, start_time):
   hours = int(total)
   minutes = round((total - hours) * 60)
   
   final_time = start_time.shift(hours=+hours)
   final_time = final_time.shift(minutes=+minutes)
   return final_time

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  A date object (arrow)
   Returns:
      A date object indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """
   # Truncate the control distance
   control_dist_km = round(control_dist_km)
   max_total = 0

   if (control_dist_km >= brevet_dist_km):
      if brevet_dist_km == 200:
         max_total = 5.88
      elif brevet_dist_km == 300:
         max_total = 9
      elif brevet_dist_km == 400:
         max_total = 12.13
      elif brevet_dist_km == 600:
         max_total = 18.8
      elif brevet_dist_km == 1000:
         max_total = 33.083
   else:
      # Work backwards through the intervals
      for i in range(len(intervals) - 1, -1, -1):
         if intervals[i] < control_dist_km:
            diff = control_dist_km - intervals[i]
            max_total += diff / max_speed[i]
            control_dist_km -= diff

   return get_final(max_total, brevet_start_time)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  A date object (arrow)
   Returns:
      A date object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """
   control_dist_km = round(control_dist_km)

   # Max-control-cases 
   if (control_dist_km >= brevet_dist_km):
      if brevet_dist_km == 200:
         min_total = 13.5
      elif brevet_dist_km == 300:
         min_total = 20
      elif brevet_dist_km == 400:
         min_total = 27
      elif brevet_dist_km == 600:
         min_total = 40
      elif brevet_dist_km == 1000:
         min_total = 75
   # Special case, if the control distance is between 0 and 60 km, the min-speed is 20 km/hr
   # and the total starts at 1 hour
   elif (control_dist_km > 0 and control_dist_km < 60):
      min_total = 1 + control_dist_km / 20
   # Otherwise, if the control distance is greater than 0, calculate normally
   elif (control_dist_km > 0):
      min_total = 0
      for i in range(len(intervals) - 1, -1, -1):
         if intervals[i] < control_dist_km:
            diff = control_dist_km - intervals[i]
            min_total += diff / min_speed[i]
            control_dist_km -= diff
   # Special case, when the dist is 0, closing time is 1 hour later
   else:
      min_total = 1

   return get_final(min_total, brevet_start_time)

