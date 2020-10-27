import json

import cherrypy
from cherrypy.test import helper

from train_reservation.train_data_service import TrainDataService


class TrainDataServiceTest(helper.CPWebCase):
    def post(self, url, body):
        self.getPage(url=url,
                     method='POST',
                     headers=[('Content-Type', 'application/json'), ('Content-Length', str(len(body)))],
                     body=body)


class EmptyTrainTest(TrainDataServiceTest):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(TrainDataService(json.dumps(
            {'foo_train': {'seats': {'1A': {'coach': 'A', 'seat_number': '1', 'booking_reference': ''}}}})))

    def test_fetch_train_data(self):
        self.getPage('/data_for_train/foo_train')
        self.assertInBody('1A')

    def test_reserve_seat(self):
        self.post('/reserve', json.dumps({'train_id': 'foo_train', 'seats': ['1A'], 'booking_reference': '01234567'}))
        self.assertInBody('"booking_reference": "01234567"')


class ReservedTrainTest(TrainDataServiceTest):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(TrainDataService(json.dumps(
            {'foo_train': {'seats': {'1A': {'coach': 'A', 'seat_number': '1', 'booking_reference': 'existing'}}}})))

    def test_reserve_seat_when_already_reserved(self):
        self.post('/reserve', json.dumps({'train_id': 'foo_train', 'seats': ['1A'], 'booking_reference': '01234567'}))
        self.assertInBody('already booked with reference: existing')

        self.getPage('/data_for_train/foo_train')
        self.assertInBody('"booking_reference": "existing"')

    def test_reserve_with_typo_in_seat_id(self):
        self.post('/reserve', json.dumps({'train_id': 'foo_train', 'seats': ['typo'], 'booking_reference': '01234567'}))
        self.assertInBody('seat not found typo')

    def test_reset(self):
        self.getPage('/reset/foo_train')
        self.assertNotInBody('existing')
