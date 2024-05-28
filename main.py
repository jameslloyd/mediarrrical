import os, requests
from dotenv import load_dotenv
import datetime, time
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from icalendar import Calendar, Event

load_dotenv()
GRAFANA_BEARER_TOKEN = os.getenv('GRAFANA_BEARER_TOKEN')
B2KEYNAME = os.getenv('B2KEYNAME')
B2KEYID = os.getenv('B2KEYID')
B2KEY = os.getenv('B2KEY')
B2ENDPOINT = os.getenv('B2ENDPOINT')
REPEATEVERY = os.getenv('REPEATEVERY') or 43200

def merge_icals(urls):
    """Fetches iCal data from multiple URLs, merges events, and returns a single Calendar."""
    merged_calendar = Calendar()

    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            cal = Calendar.from_ical(response.text)
            for component in cal.walk():
                if component.name == "VEVENT":
                    merged_calendar.add_component(component)
        else:
            print(f"Error fetching iCal from {url}: {response.status_code}")

    return merged_calendar

def save_to_ical(calendar, filename="mediarrr_ical.ics"):
    """Saves the merged Calendar to an iCal file."""
    with open(filename, "wb") as f:
        f.write(calendar.to_ical())

    upload_to_backblaze(filename, B2KEYNAME, filename)
    

# function to read the lines of a text file into a list
def read_lines(filename):
    with open(filename) as f:
        return f.read().splitlines()
    
def get_b2_client(endpoint = B2ENDPOINT, keyID = B2KEYID, applicationKey = B2KEY):
        b2_client = boto3.client(service_name='s3',
                                 endpoint_url=endpoint,                # Backblaze endpoint
                                 aws_access_key_id=keyID,              # Backblaze keyID
                                 aws_secret_access_key=applicationKey) # Backblaze applicationKey
        return b2_client

def upload_to_backblaze(local_file, bucket_name, s3_file):
    s3 = get_b2_client()
    try:
        if s3_file.endswith('.html'):
            s3.upload_file(local_file, bucket_name, s3_file, ExtraArgs={'ContentType': 'text/html'})
        else:
            s3.upload_file(local_file, bucket_name, s3_file)
            endpoint = B2ENDPOINT.split('//')[1]
            print(f"Upload Successful: https://{B2KEYNAME}.{endpoint}/{s3_file}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print("Error: ", e)
        return False
    except:
        print("Unknown error")
        return False
    return False

ical_urls = read_lines('config/config.txt')

while True:
    merged_cal = merge_icals(ical_urls)
    save_to_ical(merged_cal)
    # wait for 1 hour
    time.sleep(int(REPEATEVERY))
