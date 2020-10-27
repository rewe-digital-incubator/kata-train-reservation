"""
Implementation of Train Data Service.
"""

import json

import cherrypy


class TrainDataService:

    def __init__(self, json_data):
        self.trains = json.loads(json_data)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def data_for_train(self, train_id):
        return self.trains.get(train_id)

    @cherrypy.expose()
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def reserve(self):
        reservation = cherrypy.request.json
        train_id = reservation['train_id']
        seats = reservation['seats']
        booking_reference = reservation['booking_reference']

        train = self.trains.get(train_id)
        for seat in seats:
            if seat not in train["seats"]:
                return "seat not found {0}".format(seat)
            existing_reservation = train["seats"][seat]["booking_reference"]
            if existing_reservation and existing_reservation != booking_reference:
                return "already booked with reference: {0}".format(existing_reservation)
        for seat in seats:
            train["seats"][seat]["booking_reference"] = booking_reference
        return self.data_for_train(train_id)

    @cherrypy.tools.json_out()
    def reset(self, train_id):
        train = self.trains.get(train_id)
        for _, seat in train["seats"].items():
            seat["booking_reference"] = ""
        return self.data_for_train(train_id)

# def start(trains_data):
#     cherrypy.config.update({"server.socket_port": 8081})
#     cherrypy.quickstart(TrainDataService(trains_data))
