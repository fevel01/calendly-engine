from nomnomdata.engine import Parameter, ParameterGroup
from nomnomdata.engine.connections import AWSTokenConnection , CalendlyConnection
from nomnomdata.engine.parameters import Boolean, Enum, String
from nomnomdata.engine.shared_configs import S3Bucket

connection_cal = ParameterGroup(
    Parameter(
        name="calendly_connection",
        display_name="Calendly API Token Connection",
        description="API Token used to access Calendly",
        type=CalendlyConnection,
        required=True,
        help_header_id="Calendly API Token Connection",
    ),
    Parameter(
        name="uuid",
        display_name="Calendly UUID",
        description="Use the UUID of the organization, if not type 'me' to take information about your organization",
        type=String(),
        required=True,
        help_header_id="Calendly API Token Connection",
    ),
    name="connection_cal",
    display_name="Calendly Connection",
)
 
source_parameters = ParameterGroup(
    Parameter(
        name="pointer",
        display_name="Next Run Start Point",
        description="Datetime stamp indicating the starting point, based on updated date, of the data to download.  This field will be automatically after each order is uploaded. Formatted as YYYY-MM-DDTHH:MM:SS.ssZ in UTC timezone.",
        type=String(),
        default="2021-09-01T00:00:00.000000Z",
        required=True,
        help_header_id="Next Run Start Point",
    ),
    Parameter(
        name="data_type",
        display_name="Data Download",
        description="Select the type of data you want to download",
        type=Enum(choices=["Users", "Listed Events", "Scheduled list events", "Organization list invitation"]),
        default="Users",
        required=False,
        help_header_id="Data to download",
    ),
    name="source_parameters",
    display_name="Source Parameters",
)
 
s3_connection = ParameterGroup(
    Parameter(
        type=AWSTokenConnection,
        name="aws_token_storage",
        display_name="Destination AWS Access Connection",
        description="Select the AWS Access Keys to use to access the S3 bucket where the cost metrics data will be stored.",
        required=False,
        help_header_id="Destination AWS Access Connection",
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
    name="destination_parameters",
    display_name="Destination Parameters",
)
