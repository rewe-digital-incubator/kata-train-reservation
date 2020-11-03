import json

import cherrypy
from cherrypy.test import helper

from train_reservation.train_data_service import TrainDataService


class TrainDataServiceTest(helper.CPWebCase):
    def post(self, url, body):
        self.getPage(
            url=url,
            method="POST",
            headers=[
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(body))),
            ],
            body=body,
        )


class EmptyTrainTest(TrainDataServiceTest):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(
            TrainDataService(
                json.dumps(
                    {
                        "foo_train": {
                            "seats": {
                                "1A": {
                                    "coach": "A",
                                    "seat_number": "1",
                                    "booking_reference": "",
                                }
                            }
                        }
                    }
                )
            )
        )

    def test_fetch_train_data(self):
        self.getPage("/data_for_train/foo_train")
        self.assertInBody("1A")

    def test_get_data_for_unknown_train_returns_404(self):
        self.getPage("/data_for_train/bar_train")
        self.assertStatus(404)

    def test_reserve_seat(self):
        self.post(
            "/reserve",
            json.dumps(
                {
                    "train_id": "foo_train",
                    "seats": ["1A"],
                    "booking_reference": "01234567",
                }
            ),
        )
        self.assertInBody('"booking_reference": "01234567"')

    def test_reserve_seat_with_unknown_train_returns_400(self):
        self.post(
            "/reserve",
            json.dumps(
                {
                    "train_id": "bar_train",
                    "seats": ["1A"],
                    "booking_reference": "01234567",
                }
            ),
        )
        self.assertStatus(400)
        self.assertInBody("Train not found: bar_train.")

    def test_reserve_seat_with_unknown_seat_returns_400(self):
        self.post(
            "/reserve",
            json.dumps(
                {
                    "train_id": "foo_train",
                    "seats": ["2A"],
                    "booking_reference": "01234567",
                }
            ),
        )
        self.assertStatus(400)
        self.assertInBody("Seat not found: 2A.")

    def test_reset_with_unknown_train_returns_404(self):
        self.getPage("/reset/bar_train")
        self.assertStatus(404)


class ReservedTrainTest(TrainDataServiceTest):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(
            TrainDataService(
                json.dumps(
                    {
                        "foo_train": {
                            "seats": {
                                "1A": {
                                    "coach": "A",
                                    "seat_number": "1",
                                    "booking_reference": "existing",
                                }
                            }
                        }
                    }
                )
            )
        )

    def test_reserve_seat_when_already_reserved(self):
        self.post(
            "/reserve",
            json.dumps(
                {
                    "train_id": "foo_train",
                    "seats": ["1A"],
                    "booking_reference": "01234567",
                }
            ),
        )
        self.assertInBody("Already booked with reference: existing.")

        self.getPage("/data_for_train/foo_train")
        self.assertInBody('"booking_reference": "existing"')

    def test_reserve_with_typo_in_seat_id(self):
        self.post(
            "/reserve",
            json.dumps(
                {
                    "train_id": "foo_train",
                    "seats": ["typo"],
                    "booking_reference": "01234567",
                }
            ),
        )
        self.assertInBody("Seat not found: typo.")

    def test_reset(self):
        self.getPage("/reset/foo_train")
        self.assertNotInBody("existing")
