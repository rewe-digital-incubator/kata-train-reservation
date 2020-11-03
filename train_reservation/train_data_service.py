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
        with cherrypy.HTTPError.handle(KeyError, 404):
            return self.trains[train_id]

    @cherrypy.expose()
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def reserve(self):
        reservation = cherrypy.request.json
        train_id = reservation["train_id"]
        seats = reservation["seats"]
        booking_reference = reservation["booking_reference"]

        with cherrypy.HTTPError.handle(KeyError, 400, f"Train not found: {train_id}."):
            train = self.trains[train_id]

        for seat in seats:
            with cherrypy.HTTPError.handle(KeyError, 400, f"Seat not found: {seat}."):
                existing_booking_reference = train["seats"][seat]["booking_reference"]

                if (
                    existing_booking_reference
                    and existing_booking_reference != booking_reference
                ):
                    return "already booked with reference: {0}".format(
                        existing_booking_reference
                    )

        for seat in seats:
            train["seats"][seat]["booking_reference"] = booking_reference

        return self.data_for_train(train_id)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def reset(self, train_id):
        train = self.trains.get(train_id)
        for _, seat in train["seats"].items():
            seat["booking_reference"] = ""
        return self.data_for_train(train_id)
