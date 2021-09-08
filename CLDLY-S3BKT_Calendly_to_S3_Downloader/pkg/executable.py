import io
import json
import logging
from datetime import datetime
from datetime import timedelta
import boto3
import requests
from botocore.exceptions import ClientError
from nomnomdata.engine import Engine
from .models import connection_cal, s3_connection, source_parameters

logger = logging.getLogger("engine.calendly")
 
engine = Engine(
    uuid="CLNDY-S3BKT",
    alias="Calendly to S3 Downloader",
    description="Demonstrates basic app structure and functionality.",
    icons={},
    categories=["general", "Calendly", "S3Bucket"],
)
BASE_URL = "https://api.calendly.com"
#UUID = "CBCB7APNMRY5FIZH"
URL_MAP = {
    "users": {"url": BASE_URL + "/users/",},
    "list_user_events": {"url": BASE_URL + "/event_types?organization=",},
    "scheduled_list_events":{"url": BASE_URL + "/scheduled_events?organization=",},
    "list_organization_invitation" : {"url": BASE_URL + "/organizations/"}
}

@engine.action(
    display_name="Calendly",
    description="Prints a greeting multiple times in the Task execution log.",
    help_md_path="",
)
@engine.parameter_group(s3_connection)
@engine.parameter_group(connection_cal)
@engine.parameter_group(source_parameters)

def upload_parameters(params):
    type_data = params.get("data_type").lower()
    start_date = params.get("pointer")
    header = {"authorization": "Bearer" + " " + params["calendly_connection"]['token']}
    uuid = uuid_control(params, header)  
    logger.debug(f"Getting information about {type_data}")
    if type_data == "users":
        url = URL_MAP["users"]["url"] + uuid
        filter_data = requests.get(url=url, headers=header).json()
        logger.debug(f"Getting information about {type_data}")

    if type_data == "list events":
        filter_data = pagination(params, get_first_users_link(header, uuid), header, uuid)
        logger.debug(f"Getting information about {type_data}")
    
    if type_data == "scheduled list events":
        
        filter_data = pagination(params, get_scheduled_list_events(header, start_date, uuid), header, uuid)
        logger.debug(f"Getting information about {type_data} from {start_date}")
    
    if type_data == "organization list invitation":
        filter_data = pagination(params, get_list_organization_invitation(header, uuid), header, uuid)
        
    logger.debug(f"Getting information about {type_data}")
    name = f"Calendly_{type_data}_{start_date}.json"
    n_days = str(max(get_dates_to_process(dates_control(params))))
    #end_end = datetime.strptime(n_days, "%Y-%m-%dT%H:%M:%S.%fZ")
    try:

        write_to_s3(params, filter_data, name)
        logger.info(f'Data uploaded!')
        
    except:
        logger.info("Problems uploading Data")
      
    engine.update_parameter(
        "pointer", n_days,
        )

def dates_control(params):
    start_date = params.get("pointer")
    try:
        return datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DDTHH:MM:SS.sssZ")

def uuid_control(params, headers):
    if params.get("uuid") == "me": 
        url = URL_MAP["users"]["url"] + "me"
        response = requests.get(url=url, headers=headers).json()
        uri = response.get("resource")["uri"]
        return uri.split('/')[-1]
    else: 
        try: 
            return params.get("uuid")
        except:
            logger.info("Insert a valid UUID")

def get_first_users_link(headers, uuid):
    
    url = URL_MAP["users"]["url"] + uuid
    response = requests.get(url=url, headers=headers).json()
    url_organization = response.get("resource")["current_organization"]
    url1 = URL_MAP["list_user_events"]["url"]
    final_url = url1 + url_organization
    return final_url

def first_request(x, headers):
  return requests.get(x, headers = headers).json()

def get_page_token(page_request):
  return page_request.get("pagination")["next_page"]

def get_scheduled_list_events(headers, start_date, uuid):
  url = URL_MAP["users"]["url"] + uuid
  response = requests.get(url=url, headers=headers).json()
  url_organization = response.get("resource")["current_organization"]
  url1 = URL_MAP["scheduled_list_events"]["url"]
  final_url = url1 + url_organization + '&min_start_time=' + start_date
  return final_url

def get_list_organization_invitation(headers, uuid):
  url = URL_MAP["users"]["url"] + uuid
  response = requests.get(url=url, headers=headers).json()
  url_organization = response.get("resource")["current_organization"]
  url1 = URL_MAP["list_organization_invitation"]["url"]
  final_url = url1 + url_organization.split('/')[-1] + "/invitations"
  return final_url

def pagination(params, link, headers, uuid):
  
  url_list = []
  first_url = get_first_users_link(headers, uuid)
  url_list.append(link)  
  a = first_request(url_list[0], headers)
  url_list.append(get_page_token(a))
  start_date = dates_control(params)
  n_days = len(get_dates_to_process(start_date))
  logger.debug(n_days)
  x = 1
  h=0
  if url_list[1] != None:
    while url_list[x] != None or url_list[x] != "null":
      a = first_request(url_list[x], headers)
      if get_page_token(a) != None:
        url_list.append(get_page_token(a))
        
      else:
        return url_list

      x += 1
      i = 0 
      h = 0
      las_list = []
      for i, progress in url_list:
        las_list.append(first_request(i, headers))
        h += 1
        progress = "%.2f" % min(100, (((i + 1) * 1.0 / len(las_list)) * 100))
        engine.update_progress(progress=progress)
        """
        five_percent = round(len(url_list) * 0.5)
        
        if h % five_percent == 0:
            percent = "%.2f" % ((h / len(url_list)) * 100)
            engine.update_progress(progress=percent)
            logger.info(f"Processed {percent}% of the data.")
      """
      return las_list
      
  else:
    return first_request(url_list[0], headers)

def get_dates_to_process(start):
    
    end = datetime.now()
    x = []
    while start < end:
        next_end = start + timedelta(1)
        if next_end > end:
            next_end = end
        x.append(start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        start = next_end
    return x


def write_to_s3(params, filter_data, name):
    
    data_to_upload = json.dumps(filter_data)
    jsonBinaryFileObj = io.BytesIO(bytes(data_to_upload, "utf-8"))
    # write in S3 Bucket
    configPrefix = params["s3_bucket_config"].get("path_prefix") or ""
    targetFolder = params.get("target_folder") or ""
    path_parts = [configPrefix, targetFolder, name]
    s3key = "/".join(
        filter(None, [x for y in [i.split("/") for i in path_parts] for x in y])
    )

    # Create the connection object for S3 API
    s3 = boto3.client(
        "s3",
        aws_access_key_id=params["aws_token_storage"]["aws_access_key_id"],
        aws_secret_access_key=params["aws_token_storage"]["aws_secret_access_key"],
    )

    # Repoint the S3 client to the region of the bucket, instead of the default region
    response = s3.get_bucket_location(Bucket=params["s3_bucket_config"]["bucket"])
    s3resource = boto3.resource(
        "s3",
        aws_access_key_id=params["aws_token_storage"]["aws_access_key_id"],
        aws_secret_access_key=params["aws_token_storage"]["aws_secret_access_key"],
        region_name=response["LocationConstraint"],
    )

    bucket = s3resource.Bucket(params["s3_bucket_config"]["bucket"])
    if params["allow_overwrite"]:
        bucket.upload_fileobj(jsonBinaryFileObj, s3key)
    else:

        try:
            s3.head_object(Bucket=params["s3_bucket_config"]["bucket"], Key=s3key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                bucket.upload_fileobj(jsonBinaryFileObj, s3key)




"""
def upload_parameters(params):

    type_data = params.get("data_type")
    point = params.get("pointer")
    header = {"authorization": "Bearer" + params["calendly_connection"]}
    start_date = datetime.strptime(point, "%Y-%m-%d")
    n_days = len(get_dates_to_process(start_date))
    i = 0
    time = datetime.now().date()
    while i <= n_days:
        i += 1
        five_percent = round(n_days * 0.05)
        if i % five_percent == 0:

            percent = "%.2f" % ((i / n_days) * 100)
            engine.update_progress(progress=percent)
            logger.info(f"Processed {percent}% of the data.")

        if type_data == "users":
            filter_data = get_users(header)
            logger.debug(f"Getting information about {type_data} in{time}")

        if type_data == "events":
            filter_data = get_events(start_date, header, time)
            logger.debug(f"Getting information about {type_data} in {time}")

        logger.debug(f"Uploading {type_data} of {i} to S3 bucket...")

    name = f"Calendly_{type_data}_{start_date}_to_{time}.json"

    try:

        write_to_s3(params, filter_data, name)
        logger.info("Data uploaded!")
        engine.update_parameter(
            "pointer", datetime.strftime(time, "%Y-%m-%d"),
        )
    except:
        logger.info("Problems uploading Data ")



"""