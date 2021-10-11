# Calendly to S3 Downloader

Calendly to S3 Downloader is used to download data about users or events from Calendly and store it in an S3 bucket.

## Download Data

The **Download Data** action will request data from the Calendly API and save the data returned in JSON format within files created in the specified S3 bucket and folder.  This Task requires you to provide a Calendly personal access token, an organization id, the type of data to download, a starting point date and time, AWS access credentials, shared configuration options for the S3 Bucket, a target folder to create files in and whether or not existing files can be overwritten.

### Calendly Connection

A Personal Access Token is a long string of characters used to authenticate with the Calendly's REST API.  This link contains more information about how to create a Personal Access Token for your Calendly account:

<https://developer.calendly.com/how-to-authenticate-with-personal-access-tokens>

Calendly API access information is stored in a **Calendly Access Token** Connection on your Nominode.  This link contains more information about creating a Connection on a Nominode:

<https://support.nomnomdata.com/portal/kb/articles/managing-connections-on-a-nominode#Creating_a_Connection>

A **Calendly Access Token** Connection has two fields, Alias and Personal Access Token.
- Set the **Alias** field to something meaningful like "Calendly as YourUser".
- Set the **Personal Access Token** field to the Personal Access Token text string that you obtained by following the steps in the first link.

Once the Connection is created, you can select its Alias from the drop down list for the Calendly Connection field on this Task.

### Data Type

Select the type of data that you want to download.

### Next Run Start Point

Only data that has been created or updated after the datetime stamp specified will be included.  After each successful Task execution, this field value will automatically be updated to the current datetime to allow the next run of the Task to begin at that point.  The value should be formatted as YYYY-MM-DDTHH:MM:SS in UTC timezone.  This field can be modified between Task runs, if desired.

### AWS Access Connection

AWS access information is stored in an **AWS:Token** Connection on your Nominode.  This link contains more information about creating a Connection on a Nominode:

<https://support.nomnomdata.com/portal/kb/articles/managing-connections-on-a-nominode#Creating_a_Connection>

An **AWS:Token** Connection has four fields.
- Set the **Alias** field to something meaningful like "AWS Credentials for Marketing".
- Set the **Access Key ID** field to the first part of your AWS access key.
- Set the **Secret Access Key** field to the second part of your AWS access key.
- Set the **Region** field to the default region when you log in.  For example, "us-east-1".

This link contains more information about AWS access keys:

<https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>

Once the Connection is created, you can select its Alias from the drop down list for the AWS Access Connection field on this Task.

### S3 Bucket Configuration

AWS S3 Bucket configuration information is stored in a **S3 Bucket** Shared Config on your Nominode.  This link contains more information about creating a Shared Config on a Nominode:

<https://support.nomnomdata.com/portal/en/kb/articles/managing-shared-configs-on-a-nominode#Creating_a_Shared_Config>

An **S3 Bucket** Shared Config has four fields.
- Set the **Alias** field to something meaningful like "YourS3BucketOptions".
- Set the **Bucket Name** field to the name of the S3 Bucket where the files will be stored.
- Set the **Path Prefix** field to a path that will be prepended to the path specified in a Task to form the full path where files will be stored within the Bucket.
- Set the **Temp Path** field to a path within the Bucket where temporary files can be written.

Once the Shared Config is created, you can select its Alias from the drop down list for the S3 Bucket Configuration field on this Task.

### Target Folder

Specify the path from the starting folder in the S3 Bucket Configuration to the folder where the downloaded data will be stored.  This path is appended to the Path Prefix in the S3 Bucket Configuration, so do not include that part of the path in this field value.  Folders in the path that do not exist will be created.

Files created in the Target Folder will be named based on the Data Type selected and the Next Run Start Point.  For example, scheduled events updated after 06/01/2021 would be stored in a file with this name:

         Calendly_scheduled_events_20210601.json

### Allow Overwrite

This field determines what this Task will do if a file exists in the Target Folder with the same name as the download file being created.  If this field is set to Enabled, that file will be overwritten.  If this field is set to Disabled, the Task run will fail.