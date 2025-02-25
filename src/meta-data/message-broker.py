import argparse
import json
import traceback

import urllib3
from kafka import KafkaConsumer

from airqo_api import AirQoApi
from config import Config
from api.models import extract as ext

urllib3.disable_warnings()


class MessageBroker:
    @staticmethod
    def listen_to_created_sites():
        airqo_api = AirQoApi()
        consumer = KafkaConsumer(
            Config.SITES_TOPIC,
            bootstrap_servers=Config.BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        model = ext.Extract()

        print("Listening to created sites.....")

        for msg in consumer:
            try:
                site = msg.value
                print(f"\nReceived site : {site}")
                data_is_valid = True

                for field in ["latitude", "longitude", "network", "_id"]:
                    if not site.get(field, None):
                        print(f"Error : {field} is missing in site details")
                        data_is_valid = False

                if not data_is_valid:
                    continue

                site_latitude = site.get("latitude")
                site_longitude = site.get("longitude")
                site_network = site.get("network")
                site_id = site.get("_id")

                site_latitude = float(site_latitude)
                site_longitude = float(site_longitude)

            except Exception as ex:
                print(ex)
                traceback.print_exc()
                continue

            site_meta_data = {
                "network": site_network,
                "id": site_id,
            }

            print("Computing altitude.....")
            altitude = model.get_altitude(site_latitude, site_longitude)
            print("Computing aspect.....")
            aspect = model.get_aspect_270(site_latitude, site_longitude)
            print("Computing landform 90.....")
            landform_90 = model.get_landform90(site_latitude, site_longitude)
            print("Computing landform 270.....")
            landform_270 = model.get_landform270(site_latitude, site_longitude)
            print("Computing bearing from kampala.....")
            bearing_from_kampala = model.get_bearing_from_kampala(
                site_latitude, site_longitude
            )
            print("Computing weather stations.....")
            weather_stations = model.get_nearest_weather_stations(
                site_latitude, site_longitude
            )
            print("Saving site information.....")
            airqo_api.update_site_meta_data(
                {
                    **site_meta_data,
                    **{
                        "altitude": altitude,
                        "aspect": aspect,
                        "landform_90": landform_90,
                        "landform_270": landform_270,
                        "bearing_to_kampala_center": bearing_from_kampala,
                        "weather_stations": weather_stations,
                    },
                }
            )

            print("Computing distance from kampala.....")
            distance_from_kampala = model.get_distance_from_kampala(
                site_latitude, site_longitude
            )
            print("Computing distance to closest road.....")
            distance_to_closest_road = model.get_distance_to_closest_road(
                site_latitude, site_longitude
            )
            print("Computing distance to closest primary road.....")
            distance_to_closest_primary_road = (
                model.get_distance_to_closest_primary_road(
                    site_latitude, site_longitude
                )
            )
            print("Computing distance to closest secondary road.....")
            distance_to_closest_secondary_road = (
                model.get_distance_to_closest_secondary_road(
                    site_latitude, site_longitude
                )
            )
            print("Computing distance to closest residential road.....")
            distance_to_closest_residential_road = (
                model.get_distance_to_closest_residential_road(
                    site_latitude, site_longitude
                )
            )
            print("Computing distance to closest tertiary road.....")
            distance_to_closest_tertiary_road = (
                model.get_distance_to_closest_tertiary_road(
                    site_latitude, site_longitude
                )
            )
            print("Computing distance to closest trunk.....")
            distance_to_closest_trunk = model.get_distance_to_closest_trunk(
                site_latitude, site_longitude
            )
            print("Computing distance to closest unclassified road.....")
            distance_to_closest_unclassified_road = (
                model.get_distance_to_closest_unclassified_road(
                    site_latitude, site_longitude
                )
            )
            print("Computing distance to closest motorway.....")
            distance_to_closest_motorway = model.get_distance_to_closest_motorway(
                site_latitude, site_longitude
            )
            print("Saving distances.....")
            airqo_api.update_site_meta_data(
                {
                    **site_meta_data,
                    **{
                        "distance_to_kampala_center": distance_from_kampala,
                        "distance_to_nearest_road": distance_to_closest_road,
                        "distance_to_nearest_secondary_road": distance_to_closest_secondary_road,
                        "distance_to_nearest_primary_road": distance_to_closest_primary_road,
                        "distance_to_nearest_residential_road": distance_to_closest_residential_road,
                        "distance_to_nearest_tertiary_road": distance_to_closest_tertiary_road,
                        "distance_to_nearest_trunk": distance_to_closest_trunk,
                        "distance_to_nearest_unclassified_road": distance_to_closest_unclassified_road,
                        "distance_to_nearest_motorway": distance_to_closest_motorway,
                    },
                }
            )

            print("Computing land use.....")
            land_use = model.get_landuse(site_latitude, site_longitude)
            print("Saving land use.....")
            airqo_api.update_site_meta_data(
                {
                    **site_meta_data,
                    **{
                        "land_use": land_use,
                    },
                }
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        required=True,
        type=str.lower,
        choices=[
            "air-qlouds-consumer",
            "sites-consumer",
            "devices-consumer",
        ],
    )

    args = parser.parse_args()
    if args.target == "air-qlouds-consumer":
        pass

    elif args.target == "sites-consumer":
        MessageBroker.listen_to_created_sites()

    elif args.target == "devices-consumer":
        pass
