from datetime import datetime
from datetime import timedelta
import boto3
from hvac import Client
from moto import mock_s3

from ..executable import get_first_users_link, first_request, get_page_token, get_scheduled_list_events, get_list_organization_invitation, pagination, write_to_s3

"""
def get_secret(
    secret_name, url="https://vault.nomnomdata.com/", mount_point="developers"
):
    vault = Client(url=url)
    return vault.secrets.kv.read_secret_version(secret_name, mount_point=mount_point)[
        "data"
    ]["data"]
"""

params = {
    "calendly_connection": "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjMwMDk4NzA4LCJqdGkiOiIxMjYzM2Q3Yi1kMWI2LTQ5NGUtOTBiNC0yNmNiYWQ2MGZkODQiLCJ1c2VyX3V1aWQiOiJDQkNCN0FQTk1SWTVGSVpIIn0.gjccgijKsAFz2NkgMFN5Ux9HIycU1__oExrp0D719Ok",
    #"calendly_connection": get_secret("calendly").get("api_token"),
    "s3_folder_path": "calendly_test",
    "data_type": "users",
    "pointer": "2021-09-02T20:34:08.000000Z",
    "allow_overwrite": False,
    "add_processed_column": False,
    "s3_bucket_config": {"path_prefix": "prefix", "bucket": "s3-nom-data-test-report",},
    "aws_token_storage": {
        "aws_access_key_id": "JUNK",
        "prefix": "prefix",
        "s3_temp_space": "temp",
        "aws_secret_access_key": "FAKE",
        "region": "LocationConstraint",
    },
}

url = "https://api.calendly.com"
headers = {"authorization": "Bearer" + " " + params["calendly_connection"]}
point = params.get("pointer")

def test_get_events():
    events = pagination(params, get_first_users_link(headers), headers)
    assert type(events) is dict or str and events != 0
    return events

def test_scheduled_events():
    scheduled_events = pagination(params, get_first_users_link(headers), headers)
    assert type(scheduled_events) is dict or str and scheduled_events != 0
    return scheduled_events

def test_organization_list():
    organization_list = pagination(params, get_first_users_link(headers), headers)
    assert type(organization_list) is dict or str and organization_list != 0
    return organization_list

@mock_s3
def test_write_s3():
    tested_events = test_get_events()
    bucket = params["s3_bucket_config"]["bucket"]
    s3_conn = boto3.client("s3", region_name="us-east-1")
    s3_conn.create_bucket(Bucket=bucket)
    write_to_s3(params, tested_events, name="test")
    s3_list = s3_conn.list_objects_v2(Bucket=params["s3_bucket_config"]["bucket"])
    data = s3_conn.get_object(Bucket=bucket, Key=s3_list["Contents"][0]["Key"])
    contents = data["Body"].read()
    assert contents != 0 or contents != None
