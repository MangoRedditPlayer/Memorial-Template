import os
import json
import yaml # Requires PyYAML to be installed
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- Configuration from Environment Variables (passed by GitHub Actions) ---
# These secrets need to be set in your GitHub repository settings:
# GCP_SA_CREDENTIALS: The JSON string of your Google Cloud Service Account key
# GOOGLE_SHEET_ID: The ID of your Google Spreadsheet
# MEDIA_SHEET_NAME: The name of the sheet tab to read from (e.g., "Media_Gallery_Input")

GCP_SA_CREDENTIALS_JSON_STR = os.environ.get('GCP_SA_CREDENTIALS')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
MEDIA_SHEET_NAME = os.environ.get('MEDIA_SHEET_NAME') # Default sheet name if not set

# The specific range to read from your sheet.
# Assumes headers are in row 1, and data starts from row 2.
# Reads columns A to E (Type, URL, Caption, Submitter_Name, Submission_Date)
SHEET_RANGE = f"{MEDIA_SHEET_NAME}!A2:E" 
YAML_OUTPUT_FILE = '_data/media_gallery.yml' # Path relative to the repository root

def fetch_sheet_data():
    """Fetches data from the Google Sheet."""
    if not GCP_SA_CREDENTIALS_JSON_STR:
        print("Error: GCP_SA_CREDENTIALS environment variable is not set.")
        return None
    if not GOOGLE_SHEET_ID:
        print("Error: GOOGLE_SHEET_ID environment variable is not set.")
        return None
        
    try:
        creds_json = json.loads(GCP_SA_CREDENTIALS_JSON_STR)
        creds = service_account.Credentials.from_service_account_info(
            creds_json,
            scopes=['https_//www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        print(f"Fetching data from Spreadsheet ID: '{GOOGLE_SHEET_ID}', Range: '{SHEET_RANGE}'")
        result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID, range=SHEET_RANGE).execute()
        values = result.get('values', [])
        print(f"Successfully fetched {len(values)} rows from Google Sheet.")
        return values
    except json.JSONDecodeError:
        print("Error: Failed to parse GCP_SA_CREDENTIALS. Ensure it's a valid JSON string.")
        return None
    except Exception as e:
        print(f"Error fetching Google Sheet data: {e}")
        return None

def format_for_yaml(rows):
    """Formats the fetched rows into a list of dictionaries for YAML."""
    media_items = []
    if not rows:
        print("No data rows found in the sheet to process.")
        return media_items

    print(f"Formatting {len(rows)} data rows for YAML.")
    for row_index, row in enumerate(rows):
        # Ensure row has enough columns, pad with empty strings if not
        # Expecting: Type (0), URL (1), Caption (2), Submitter_Name (3), Submission_Date (4)
        expected_cols = 5
        current_cols = len(row)
        if current_cols < expected_cols:
            row.extend([''] * (expected_cols - current_cols))

        item_type = str(row[0]).strip().lower() if row[0] else None
        item_url = str(row[1]).strip() if row[1] else None
        item_caption = str(row[2]).strip() if row[2] else None
        item_submitter = str(row[3]).strip() if row[3] else None
        item_date_str = str(row[4]).strip() if row[4] else None # Expecting YYYY-MM-DD

        # Basic validation
        if not item_type or not item_url:
            print(f"Skipping row {row_index + 2} (original sheet row): 'Type' or 'URL' is missing. Row data: {row[:expected_cols]}")
            continue
        
        if item_type not in ["image", "video"]:
            print(f"Skipping row {row_index + 2}: Invalid 'Type' ('{item_type}'). Must be 'image' or 'video'. Row data: {row[:expected_cols]}")
            continue

        if not (item_url.startswith('http://') or item_url.startswith('https://')):
            print(f"Skipping row {row_index + 2}: Invalid 'URL' format for '{item_url}'. Row data: {row[:expected_cols]}")
            continue

        media_item = {'type': item_type, 'url': item_url}
        if item_caption:
            media_item['caption'] = item_caption
        if item_submitter:
            media_item['submitter_name'] = item_submitter
        if item_date_str: 
            media_item['submission_date'] = item_date_str # Assumes YYYY-MM-DD format
        
        media_items.append(media_item)
    
    # Optional: Sort data if needed, e.g., by submission_date.
    # Note: gallery.html also has a sort Liquid filter. Consistent sorting is good.
    # If submission_date might be empty or malformed, sorting needs careful error handling.
    # For simplicity, we'll let Liquid handle sorting for now, or assume dates are well-formed.
    # Example:
    # if any(item.get('submission_date') for item in media_items):
    #     media_items.sort(key=lambda x: x.get('submission_date', ''), reverse=True)

    return media_items

def write_yaml_file(data, filepath):
    """Writes the data to the YAML file."""
    # Ensure the _data directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    try:
        # Write an empty list if data is empty, otherwise dump the data
        yaml_content_to_write = data if data else [] 
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content_to_write, f, allow_unicode=True, sort_keys=False, indent=2, Dumper=yaml.SafeDumper)
        
        if yaml_content_to_write:
            print(f"Successfully wrote {len(yaml_content_to_write)} items to {filepath}")
        else:
            print(f"{filepath} written as an empty list or with no valid items.")
    except Exception as e:
        print(f"Error writing YAML file to {filepath}: {e}")

if __name__ == '__main__':
    print("Starting media gallery sync script...")
    if not all([GCP_SA_CREDENTIALS_JSON_STR, GOOGLE_SHEET_ID, MEDIA_SHEET_NAME]):
        print("Error: Missing one or more required environment variables (GCP_SA_CREDENTIALS, GOOGLE_SHEET_ID, MEDIA_SHEET_NAME). Script will not run.")
    else:
        sheet_rows = fetch_sheet_data()
        
        if sheet_rows is not None: # Proceed if fetch attempt was made (even if it returned empty list)
            yaml_data = format_for_yaml(sheet_rows)
            write_yaml_file(yaml_data, YAML_OUTPUT_FILE)
        else:
            # Fetch failed, write an empty YAML file to indicate data couldn't be retrieved
            # or to clear old data if that's the desired behavior on fetch failure.
            # Current behavior: fetch_sheet_data prints error and returns None, script ends.
            # If we want to clear the YAML on fetch failure, we could call:
            # write_yaml_file([], YAML_OUTPUT_FILE) 
            print("Failed to fetch sheet data. YAML file not updated by this run.")
    print("Media gallery sync script finished.")