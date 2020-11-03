import cherrypy
from cherrypy.test import helper

from train_reservation.booking_reference_service import BookingReferenceService


class BookingReferenceServiceTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(BookingReferenceService(123456789))

    def test_booking_number_has_length_greater_than_five(self):
        self.getPage("/booking_reference")
        self.assertMatchesBody("^.{6,}$")

    def test_booking_number_does_not_start_with_0x(self):
        self.getPage("/booking_reference")
        self.assertNotRegex(self.body.decode(), "^0x")

    def test_booking_reference_is_unique(self):
        self.getPage("/booking_reference")
        booking_number_1 = self.body.decode()

        self.getPage("/booking_reference")
        booking_number_2 = self.body.decode()

        self.assertNotEqual(booking_number_1, booking_number_2)
