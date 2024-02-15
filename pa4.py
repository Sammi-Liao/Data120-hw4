# Problem 1: Flight class
class Flight():
    def __init__(self, origin, dest, takeoff, land, airline, miles):
        self.origin = origin
        self.dest = dest
        self.takeoff = takeoff
        #int('{:04d}'.format(takeoff))
        self.land = land
        #int('{:04d}'.format(land))
        self.airline = airline
        self.miles = miles

        if not isinstance(origin, str):
            raise TypeError('Origin airport code must be a string')
        if len(origin) != 3:
            raise ValueError('Origin airport code must be 3-letter')
        if not isinstance(dest, str):
            raise TypeError('Destination airport code must be a string')
        if len(dest) != 3:
            raise ValueError('Desination airport code must be 3-letter')
        if not isinstance(takeoff, int):
            raise TypeError('Takeoff time must be an int')
        if not isinstance(land, int):
            raise TypeError('Landing time must be an int')
        if not (0 <= int('{:04d}'.format(takeoff)[: 2]) <= 23 and
                0 <= int('{:04d}'.format(takeoff)[2: ]) <= 59):
            raise ValueError('Takeoff time is invalid')
        if not (0 <= int('{:04d}'.format(land)[: 2]) <= 23 and
                0 <= int('{:04d}'.format(land)[2: ]) <= 59):
            raise ValueError('Landing time is invalid')
        if land < takeoff:
            raise ValueError('Landing time should be after takeoff time')
        if not isinstance(airline, str):
            raise TypeError('Airline must be a string')
        if airline not in ['Columbian', 'Epsilon', 'Divided', 'Cardioid']:
            raise ValueError('Airline name is not in the four carriers')
        if not isinstance(miles, int):
            raise TypeError('Miles must be an int')
        if miles < 0:
            raise ValueError('Miles must be positive')

    def can_connect(self, earlier, layover):
        '''Returns a boolean indicating whether it is possible to connect 
        from earlier, another Flight object, to this flight (self).'''
        if self.origin != earlier.dest:
            return False
        elif self.takeoff < earlier.land:
            return False
        elif ((int('{:04d}'.format(self.takeoff)[2: ]) -
             int('{:04d}'.format(earlier.land)[2: ])) +
            (int('{:04d}'.format(self.takeoff)[: 2]) -
             int('{:04d}'.format(earlier.land)[: 2])) * 60) < layover:
            return False
        else:
            return True

    def duration(self):
        '''returns the duration of the flight, in minutes'''
        return ((int('{:04d}'.format(self.land)[2: ]) -
                 int('{:04d}'.format(self.takeoff)[2: ])) +
                (int('{:04d}'.format(self.land)[: 2]) -
                 int('{:04d}'.format(self.takeoff)[: 2]))* 60)

    def average_speed(self):
        '''returns the average speed of the flight, in miles per hour'''
        return self.miles / (self.duration() / 60)


# Problem 2: Itinerary Class
class Itinerary():
    def __init__(self, flights):
        self.flights = []
        if not isinstance(flights, list):
            raise TypeError('This is not a list')
        if not flights:
            raise ValueError('List of flights should not be empty')
        for f in flights:
            if not isinstance(f, Flight):
                raise TypeError('It has elements that is not Flight type')
        self.flights = flights

    def is_plausible(self, layover):
        '''Return a boolean indicating whether the proposed itinerary is 
        physically possible, defined as being able to connect, with the 
        specified minimum layover, between each adjacent pair of flights 
        in the sequence.'''
        self.flights.sort(key = lambda f: f.takeoff)
        for i in range(len(self.flights) - 1):
            ispossible = Flight.can_connect(self.flights[i + 1],
                                             self.flights[i], layover)
            if not ispossible:
                return False
            else:
                continue
        return True

    def total_miles(self):
        '''Returns the sum of the miles for all the flights in the route'''
        total_miles = 0
        for i in self.flights:
            total_miles = total_miles + i.miles
        return total_miles

    def is_single_carrier(self):
        '''Returns True if all the flights in the itinerary are operated 
        by the same airline, False otherwise.'''
        carrier = set()
        for i in self.flights:
            carrier.add(i.airline)
        if len(carrier) == 1:
            return True
        else:
            return False

    def air_time(self):
        '''return the total number of minutes in the air across the flights'''
        total_mintues = 0
        for i in self.flights:
            total_mintues = total_mintues + Flight.duration(i)
        return total_mintues

    def total_time(self):
        '''return the number of minutes from the takeoff of the first flight 
        to the landing of the last'''
        self.flights.sort(key = lambda f: f.takeoff)
        return ((int('{:04d}'.format(self.flights[-1].land)[2: ]) -
                 int('{:04d}'.format(self.flights[0].takeoff)[2: ])) +
                (int('{:04d}'.format(self.flights[-1].land)[: 2]) -
                 int('{:04d}'.format(self.flights[0].takeoff)[: 2])) * 60)

    def miles_earned(self):
        '''return a dictionary whose keys are the names of the airlines 
        involved in the itinerary, and whose associated values are the total 
        miles traveled on the corresponding airline within the itinerary.'''
        milesearned = {}
        for i in self.flights:
            milesearned[i.airline] = milesearned.get(i.airline, 0) + i.miles
        return milesearned


# Problem 3: GCD
# gcd(a, 0) = a
# gcd(a, b) = gcd(b, a mod b) a%b
# where a >= b in each case
def gcd(a, b):
    '''Take two integers, perform gcd formula to find theier 
    greatest common divisor'''
    if b == 0:
        return a
    return gcd(b, a % b)


# Problem 4: Directions
# Should remove adjacent, redundant pairs, but not further remove new pairs
# that become adjacent because of the removal of other pairs in between them

# Write a recursive solution that indexes and/or slices into the string
# and performs string concatenation as needed, but does not use string methods
# such as replace, and does not use any loops
def remove_pairs(direction_str):
    '''Take in a direction string path, return a direction string 
    such that all turnaround pairs have been removed'''
    if len(direction_str) < 2:
        return direction_str
    else:
        if (direction_str[0: 2] == 'EW' or direction_str[0: 2] == 'SN'
            or direction_str[0: 2] == 'WE' or direction_str[0: 2] == 'NS'):
            return remove_pairs(direction_str[2: ])
        else:
            return direction_str[0] + remove_pairs(direction_str[1: ])
