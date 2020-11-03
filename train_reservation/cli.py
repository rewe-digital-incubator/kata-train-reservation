import cherrypy
import click

from train_reservation.booking_reference_service import BookingReferenceService
from train_reservation.train_data_service import TrainDataService


@click.command()
@click.argument(
    "trains_data_filename", default="trains.json", type=click.Path(exists=True)
)
@click.option("--port", default=8081, help="port")
def train_data_service(trains_data_filename, port):
    with open(trains_data_filename) as f:
        trains_data = f.read()

    cherrypy.config.update(
        {"server.socket_port": port, "server.socket_host": "0.0.0.0"}
    )
    cherrypy.quickstart(TrainDataService(trains_data))


@click.command()
@click.option("--starting-point", default=123456789, help="starting point reference")
@click.option("--port", default=8082, help="port")
def booking_reference_service(starting_point, port):
    cherrypy.config.update(
        {"server.socket_port": port, "server.socket_host": "0.0.0.0"}
    )
    cherrypy.quickstart(BookingReferenceService(starting_point))
