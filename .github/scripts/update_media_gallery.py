import os
import json
import yaml # Requires PyYAML to be installed
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- Configuration from Environment Variables (passed by GitHub Actions) ---
# These secrets need to be set in your GitHub repository settings
GCP_SA_CREDENTIALS_JSON_STR = os.environ.get('GCP_SA_CREDENTIALS')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
MEDIA_SHEET_NAME = os.environ.get('MEDIA_SHEET_NAME', 'Media_Gallery_Input') # Default sheet name

# The specific range to read from your sheet. Assumes headers in row 1.
# Reads columns A to E (Type, URL, Caption, Submitter_Name, Submission_Date)
SHEET_RANGE = f"{MEDIA_SHEET_NAME}!A2:E" # Start from row 2 to skip headers
YAML_OUTPUT_FILE = '_data/media_gallery.yml'

def fetch_sheet_data():
    """Fetches data from the Google Sheet."""
    try:
        creds_json = json.loads(GCP_SA_CREDENTIALS_JSON_STR)
        creds = service_account.Credentials.from_service_account_info(
            creds_json,
            scopes=['https_//www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID, range=SHEET_RANGE).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"Error fetching Google Sheet data: {e}")
        return None

def format_for_yaml(rows):
    """Formats the fetched rows into a list of dictionaries for YAML."""
    media_items = []
    if not rows:
        print("No data found in the sheet or an error occurred.")
        return media_items

    print(f"Processing {len(rows)} rows from the sheet.")
    for row_index, row in enumerate(rows):
        # Ensure row has enough columns, pad with empty strings if not
        # Expecting: Type, URL, Caption, Submitter_Name, Submission_Date
        expected_cols = 5
        if len(row) < expected_cols:
            row.extend([''] * (expected_cols - len(row)))

        item_type = str(row[0]).strip().lower() if row[0] else None
        item_url = str(row[1]).strip() if row[1] else None
        item_caption = str(row[2]).strip() if row[2] else None
        item_submitter = str(row[3]).strip() if row[3] else None
        item_date_str = str(row[4]).strip() if row[4] else None # Expecting YYYY-MM-DD

        if not item_type or not item_url:
            print(f"Skipping row {row_index + 2}: 'Type' or 'URL' is missing. Row data: {row}")
            continue

        if item_type not in ["image", "video"]:
            print(f"Skipping row {row_index + 2}: Invalid 'Type' ('{item_type}'). Must be 'image' or 'video'. Row data: {row}")
            continue

        # Basic URL validation (very simple)
        if not (item_url.startswith('http://') or item_url.startswith('https://')):
            print(f"Skipping row {row_index + 2}: Invalid 'URL' format for '{item_url}'. Row data: {row}")
            continue

        media_item = {'type': item_type, 'url': item_url}
        if item_caption:
            media_item['caption'] = item_caption
        if item_submitter:
            media_item['submitter_name'] = item_submitter
        if item_date_str: # Date is optional, but if present, it's included
            media_item['submission_date'] = item_date_str

        media_items.append(media_item)

    # Optional: Sort by submission_date if you want a consistent order from the script
    # This assumes valid YYYY-MM-DD dates. Sorting is also done in gallery.html Liquid.
    # sorted_media = sorted(media_items, key=lambda x: x.get('submission_date', ''), reverse=True)
    # return sorted_media
    return media_items


def write_yaml_file(data):
    """Writes the data to the YAML file."""
    # Ensure the _data directory exists (GitHub Actions runner might need this)
    os.makedirs(os.path.dirname(YAML_OUTPUT_FILE), exist_ok=True)

    try:
        with open(YAML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            if data: # Only write if there's data, otherwise write an empty list or placeholder
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2)
                print(f"Successfully wrote {len(data)} items to {YAML_OUTPUT_FILE}")
            else:
                f.write("# No media items found or an error occurred.\n") 
                # Or f.write("[]\n") for an empty list
                print(f"{YAML_OUTPUT_FILE} is empty or contains no valid items.")
    except Exception as e:
        print(f"Error writing YAML file: {e}")


if __name__ == '__main__':
    if not all([GCP_SA_CREDENTIALS_JSON_STR, GOOGLE_SHEET_ID]):
        print("Error: Missing one or more required environment variables (GCP_SA_CREDENTIALS, GOOGLE_SHEET_ID).")
    else:
        print(f"Fetching data from Google Sheet ID: {GOOGLE_SHEET_ID}, Sheet Name/Range: {SHEET_RANGE}")
        sheet_rows = fetch_sheet_data()
        if sheet_rows is not None: # Proceed only if fetch was successful (even if it returned empty rows)
            yaml_data = format_for_yaml(sheet_rows)
            write_yaml_file(yaml_data)
        else:
            print("Failed to fetch sheet data. YAML file not updated.")