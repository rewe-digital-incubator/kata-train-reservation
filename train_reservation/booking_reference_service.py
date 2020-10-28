import cherrypy
import itertools


class BookingReferenceService:

    def __init__(self, starting_point):
        self.counter = itertools.count(int(str(starting_point), 16) + 1)

    @cherrypy.expose()
    def booking_reference(self):
        next_number = next(self.counter)
        return str(hex(next_number))[2:]
