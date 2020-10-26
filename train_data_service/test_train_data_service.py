""" Use py.test to run this test """

import json

import cherrypy
from cherrypy.test import helper

from train_data_service.train_data_service import TrainDataService


class TrainDataServiceEmptyTrainTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(TrainDataService(json.dumps(
            {'foo_train': {'seats': {'1A': {'coach': 'A', 'seat_number': '1', 'booking_reference': ''}}}})))

    def test_fetch_train_data(self):
        self.getPage('/data_for_train/foo_train')
        self.assertInBody('1A')

    def test_reserve_seat(self):
        body = json.dumps({'train_id': 'foo_train', 'seats': ['1A'], 'booking_reference': '01234567'})
        self.getPage('/reserve',
                     method='POST',
                     headers=[('Content-Type', 'application/json'), ('Content-Length', str(len(body)))],
                     body=body)
        self.assertInBody('"booking_reference": "01234567"')


class TrainDataServiceReservedTrainTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(TrainDataService(json.dumps(
            {'foo_train': {'seats': {'1A': {'coach': 'A', 'seat_number': '1', 'booking_reference': 'existing'}}}})))

    def test_reserve_seat_when_already_reserved(self):
        body = json.dumps({'train_id': 'foo_train', 'seats': ['1A'], 'booking_reference': '01234567'})
        self.getPage('/reserve',
                     method='POST',
                     headers=[('Content-Type', 'application/json'), ('Content-Length', str(len(body)))],
                     body=body)
        self.assertInBody('already booked with reference: existing')

        self.getPage('/data_for_train/foo_train')
        self.assertInBody('"booking_reference": "existing"')

    def test_reserve_with_typo_in_seat_id(self):
        body = json.dumps({'train_id': 'foo_train', 'seats': ['typo'], 'booking_reference': '01234567'})
        self.getPage('/reserve',
                     method='POST',
                     headers=[('Content-Type', 'application/json'), ('Content-Length', str(len(body)))],
                     body=body)
        self.assertInBody('seat not found typo')

    def test_reset(self):
        self.getPage('/reset/foo_train')
        self.assertNotInBody('existing')
