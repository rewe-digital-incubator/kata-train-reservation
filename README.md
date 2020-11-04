# Kata: Train Reservation

This repository provides the description of the [Train Reservation Kata](https://github.com/emilybache/KataTrainReservation) from Emily Bache and setup code for the two upstream services "Booking Reference Service" and "Train Data Service".

## Kata Description

Origin: [Train Reservation Kata](https://github.com/emilybache/KataTrainReservation) from Emily Bache

Railway operators aren't always known for their use of cutting edge technology, and in this case they're a little behind the times. The railway people want you to help them to improve their online booking service. They'd like to be able to not only sell tickets online, but to decide exactly which seats should be reserved, at the time of booking.

You're working on the "Ticket Office Service", and your next task is to implement the feature for reserving seats on a particular train. The railway operator has a service-oriented architecture, and both the interface you'll need to fulfill, and two services you'll need to use - "Booking Reference Service" and "Train Data Service" - are already implemented.

### Business Rules around Reservations

There are various business rules and policies around which seats may be reserved. For a train overall, no more than 70% of seats may be reserved in advance, and ideally no individual coach should have no more than 70% reserved seats either. However, there is another business rule that says you _must_ put all the seats for one reservation in the same coach. This could make you and go over 70% for some coaches, just make sure to keep to 70% for the whole train.

### The Guiding Test

The Ticket Office service needs to respond to a HTTP POST request that comes with a JSON body telling you which train the customer wants to reserve seats on, and how many they want. It should return a JSON document detailing the reservation that has been made. 

A reservation comprises a JSON document with three fields, the train id, booking reference, and the ids of the seats that have been reserved. Example JSON:

```JSON
{"train_id": "express_2000", "booking_reference": "75bcd15", "seats": ["1A", "1B"]}
```

If it is not possible to find suitable seats to reserve, the service should instead return an empty list of seats and an empty string for the booking reference.

### Booking Reference Service

You can get a unique booking reference using a REST-based service. You can use this service to get a unique booking reference. Make a GET request to `/booking_reference` and the service will return a string that looks a bit like this: `75bcd15`.
	
### Train Data Service 

You can get information about which each train has by using the train data service. You can use this service to get data for example about the train with id "express_2000" with a GET request to `/data_for_train/express_2000`. This will return a JSON document with information about the seats that this train has. The document you get back will look for example like this:

```JSON
{"seats": {"1A": {"booking_reference": "", "seat_number": "1", "coach": "A"}, "2A": {"booking_reference": "", "seat_number": "2", "coach": "A"}}}
```

Note we've left out all the extraneous details about where the train is going to and from, at what time, whether there's a buffet car etc. All that's there is which seats the train has, and if they are already booked. A seat is available if the "booking_reference" field contains an empty string. To reserve seats on a train, you'll need to make a POST request to the endpoint `/reserve` and attach JSON data for which seats to reserve. There should be three fields: "train_id", "seats", "booking_reference". The "seats" field should be a JSON encoded list of seat ids, for example: `["1A", "2A"]`. The other two fields are ordinary strings. Note the server will prevent you from booking a seat that is already reserved with another booking reference.

The service has one additional endpoint `/reset/<train_id>`, that will remove all reservations on a particular train. Use it with care.

## Run Upstream Services for Local Development using Docker

This repository includes simple implementations of the two upsteam services that can be used for local development while doing the kata.

Both services can be started using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) by issuing the following command:

```shell script
docker-compose up
```

This command will build two docker images, start two docker container and expose the train data service on port `8081` and the booking reference service on port `8082`.

### Sample Clients

Check for free seats on the train "express_2000":

```shell script
curl http://127.0.0.1:8081/data_for_train/express_2000
```

Book a seat:

```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"train_id": "express_2000", "seats": ["1A"], "booking_reference": "01234567"}' \
  http://127.0.0.1:8081/reserve
```

Reserve the seat again and it is not updated:

```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"train_id": "express_2000", "seats": ["1A"], "booking_reference": "new_reference"}' \
  http://127.0.0.1:8081/reserve
```

Remove all seat reservations for train express_2000:

```shell script
curl http://127.0.0.1:8081/reset/express_2000
```

Get a booking reference:

```shell script
curl http://127.0.0.1:8082/booking_reference
```

## Run Upstream Services for Local Development using Python

Clone the GitHub repository:

```shell script
git clone https://github.com/rewe-digital-incubator/kata-train-reservation.git
cd kata-train-reservation
```

Create a new virtual environment inside the directory:

```shell script
python3 -m venv env
```

Activate the virtual environment:

```shell script
source env/bin/activate
```

Install required packages:

```shell script
pip install -r requirements.txt
```

Install the project:

```shell script
pip install .
```

Start the `train_data_service` on port 8081 with trains.json to initialize the bookable trains:

```shell script
train_data_service --port 8081 trains.json
```

Start the `booking_reference_service` on port 8082 with the default starting point:

```shell script
booking_reference_service --port 8082
```