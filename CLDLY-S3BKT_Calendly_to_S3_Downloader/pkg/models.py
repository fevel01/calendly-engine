from nomnomdata.engine import Parameter, ParameterGroup
from nomnomdata.engine.connections import AWSTokenConnection, CalendlyConnection
from nomnomdata.engine.parameters import Boolean, Enum, String
from nomnomdata.engine.shared_configs import S3Bucket

pg_source = ParameterGroup(
    Parameter(
        name="calendly_connection",
        display_name="Calendly Connection",
        description="Personal Access Token to use to access Calendly.",
        type=CalendlyConnection,
        required=True,
        help_header_id="Calendly Connection",
    ),
    Parameter(
        name="data_type",
        display_name="Data Type",
        description="Select the type of data you want to download.",
        type=Enum(choices=["Event Types", "Scheduled Events", "Organization Invitations", "Organization Members"]),
        default="Scheduled Events",
        required=False,
        help_header_id="Data Type",
    ),
    Parameter(
        name="pointer",
        display_name="Next Run Start Point",
        description="Datetime stamp indicating the starting point of the data to download.  This field will be updated automatically after each successful Task execution. Formatted as YYYY-MM-DDTHH:MM:SS in UTC timezone.",
        type=String(),
        default="2021-09-01T00:00:00",
        required=True,
        help_header_id="Next Run Start Point",
    ),
    name="pg_source",
    display_name="Source Parameters",
)
  
pg_destination = ParameterGroup(
    Parameter(
        type=AWSTokenConnection,
        name="aws_token_storage",
        display_name="AWS Access Connection",
        description="Select the AWS Access Keys to use to access the S3 bucket where the cost metrics data will be stored.",
        required=False,
        help_header_id="AWS Access Connection",
    ),
    Parameter(
        type=S3Bucket,
        name="s3_bucket_config",
        display_name="S3 Bucket Configuration",
        description="Select the Shared Config that contains information about the S3 Bucket where the data will be stored.",
        required=False,
        help_header_id="S3 Bucket Configuration",
    ),
    Parameter(
        name="target_folder",
        display_name="Target Folder",
        description="Path from the starting folder in the S3 Bucket Configuration to the folder where the data will be stored.",
        type=String(),
        required=False,
        help_header_id="Target Folder",
    ),
    Parameter(
        type=Boolean(),
        name="allow_overwrite",
        display_name="Allow Overwrite",
        description="Enable to allow existing files with the same name to be overwritten.",
        required=False,
        default=False,
        help_header_id="Allow Overwrite",
    ),
    name="pg_destination",
    display_name="Destination Parameters",
)
