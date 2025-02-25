from airflow.decorators import dag, task

from airqo_etl_utils.airflow_custom_utils import AirflowUtils


@dag(
    "Update-BigQuery-Sites-And-Devices",
    schedule="*/15 * * * *",
    default_args=AirflowUtils.dag_default_configs(),
    catchup=False,
    tags=["hourly", "sites", "devices"],
)
def meta_data_big_query_update_sites_and_devices():
    import pandas as pd

    @task()
    def extract_sites() -> pd.DataFrame:
        from airqo_etl_utils.meta_data_utils import MetaDataUtils

        return MetaDataUtils.extract_sites_from_api()

    @task()
    def extract_sites_meta_data() -> pd.DataFrame:
        from airqo_etl_utils.meta_data_utils import MetaDataUtils

        return MetaDataUtils.extract_sites_meta_data_from_api()

    @task()
    def extract_devices():
        from airqo_etl_utils.meta_data_utils import MetaDataUtils

        return MetaDataUtils.extract_devices_from_api()

    @task()
    def load_sites_meta_data(data: pd.DataFrame):
        from airqo_etl_utils.bigquery_api import BigQueryApi

        BigQueryApi().update_sites_meta_data(dataframe=data)

    @task()
    def load_sites(data: pd.DataFrame):
        from airqo_etl_utils.bigquery_api import BigQueryApi

        big_query_api = BigQueryApi()
        big_query_api.update_sites_and_devices(
            dataframe=data,
            table=big_query_api.sites_table,
            component="sites",
        )

    @task()
    def load_devices(data: pd.DataFrame):
        from airqo_etl_utils.bigquery_api import BigQueryApi

        big_query_api = BigQueryApi()
        big_query_api.update_sites_and_devices(
            dataframe=data,
            table=big_query_api.devices_table,
            component="devices",
        )

    devices = extract_devices()
    load_devices(devices)
    sites = extract_sites()
    load_sites(sites)
    sites_meta_data = extract_sites_meta_data()
    load_sites_meta_data(sites_meta_data)


@dag(
    "Update-Microservice-Sites-Meta-Data",
    schedule="@daily",
    default_args=AirflowUtils.dag_default_configs(),
    catchup=False,
    tags=["daily", "sites", "meta-data"],
)
def meta_data_update_microservice_sites_meta_data():
    @task()
    def update_nearest_weather_stations() -> None:
        from airqo_etl_utils.meta_data_utils import MetaDataUtils
        from airqo_etl_utils.constants import Tenant

        MetaDataUtils.update_nearest_weather_stations(tenant=Tenant.ALL)

    @task()
    def update_distance_measures() -> None:
        from airqo_etl_utils.meta_data_utils import MetaDataUtils
        from airqo_etl_utils.constants import Tenant

        MetaDataUtils.update_sites_distance_measures(tenant=Tenant.ALL)

    update_nearest_weather_stations()
    update_distance_measures()


meta_data_big_query_update_sites_and_devices()
meta_data_update_microservice_sites_meta_data()
