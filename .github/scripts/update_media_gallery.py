import os
import json
import yaml # Requires PyYAML to be installed
from google.oauth2 import service_account
from googleapiclient.discovery import build
# from google.auth.exceptions import GoogleAuthError # Consider adding for specific auth error catching

# --- Configuration from Environment Variables (passed by GitHub Actions) ---
GCP_SA_CREDENTIALS_JSON_STR = os.environ.get('GCP_SA_CREDENTIALS')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
MEDIA_SHEET_NAME_FROM_ENV = os.environ.get('MEDIA_SHEET_NAME') 

YAML_OUTPUT_FILE = '_data/media_gallery.yml'
EFFECTIVE_MEDIA_SHEET_NAME = MEDIA_SHEET_NAME_FROM_ENV if MEDIA_SHEET_NAME_FROM_ENV else 'Media_Gallery_Input'
SHEET_RANGE = f"{EFFECTIVE_MEDIA_SHEET_NAME}!A2:E" # Assumes headers in row 1, data from A2:E

def fetch_sheet_data():
    """Fetches data from the Google Sheet with detailed logging."""
    print("Inside fetch_sheet_data function...")
    try:
        if not GCP_SA_CREDENTIALS_JSON_STR:
            print("Error: GCP_SA_CREDENTIALS_JSON_STR is empty or None.")
            return None
        
        print("Attempting to parse GCP SA Credentials JSON...")
        creds_json = json.loads(GCP_SA_CREDENTIALS_JSON_STR)
        print("Successfully parsed GCP SA Credentials JSON.")

        print("Attempting to create credentials from service account info...")
        creds = service_account.Credentials.from_service_account_info(
            creds_json,
            scopes=['https_//www.googleapis.com/auth/spreadsheets.readonly']
        )
        print("Successfully created credentials from service account info.")

        print("Attempting to build Google Sheets API service...")
        service = build('sheets', 'v4', credentials=creds)
        print("Successfully built Google Sheets API service.")
        
        sheet = service.spreadsheets()
        print(f"Fetching from Sheet ID: {GOOGLE_SHEET_ID}, Range: {SHEET_RANGE}")
        result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID, range=SHEET_RANGE).execute()
        print("Successfully executed sheet.values().get().")
        values = result.get('values', [])
        print(f"Retrieved {len(values)} rows of data.")
        return values

    except json.JSONDecodeError as json_e:
        print(f"Fatal Error: Could not decode GCP_SA_CREDENTIALS JSON. Ensure the GitHub secret contains the valid, complete JSON key. Error: {json_e}")
        return None
    # except GoogleAuthError as auth_e: # More specific error catching for auth
    #     print(f"Fatal Google Authentication Error: {auth_e}")
    #     return None
    except Exception as e: 
        print(f"Error during Google Sheets API interaction (inside fetch_sheet_data): {e}")
        return None

def format_for_yaml(rows):
    """Formats the fetched rows into a list of dictionaries for YAML."""
    media_items = []
    if not rows:
        print("No data rows to format for YAML (either sheet was empty or fetch returned no values).")
        return media_items

    print(f"Formatting {len(rows)} rows for YAML output.")
    for row_index, row in enumerate(rows):
        expected_cols = 5 # Type, URL, Caption, Submitter_Name, Submission_Date
        # Ensure row has enough columns, pad with empty strings if not
        current_row_len = len(row)
        if current_row_len < expected_cols:
            row.extend([''] * (expected_cols - current_row_len))

        item_type = str(row[0]).strip().lower() if row[0] else None
        item_url = str(row[1]).strip() if row[1] else None
        item_caption = str(row[2]).strip() if row[2] else "" # Default to empty string
        item_submitter = str(row[3]).strip() if row[3] else "" # Default to empty string
        item_date_str = str(row[4]).strip() if row[4] else "" # Default to empty string

        if not item_type or not item_url:
            print(f"Skipping row {row_index + 2} in sheet: 'Type' or 'URL' is missing. Row data: {row[:expected_cols]}")
            continue
        
        if item_type not in ["image", "video"]:
            print(f"Skipping row {row_index + 2} in sheet: Invalid 'Type' ('{item_type}'). Must be 'image' or 'video'. Row data: {row[:expected_cols]}")
            continue

        if not (item_url.startswith('http://') or item_url.startswith('https://')):
            print(f"Skipping row {row_index + 2} in sheet: Invalid 'URL' format for '{item_url}'. Row data: {row[:expected_cols]}")
            continue

        media_item = {'type': item_type, 'url': item_url}
        # Only add optional fields if they have content
        if item_caption:
            media_item['caption'] = item_caption
        if item_submitter:
            media_item['submitter_name'] = item_submitter
        if item_date_str: 
            media_item['submission_date'] = item_date_str
        
        media_items.append(media_item)
    return media_items


def write_yaml_file(data):
    """Writes the data to the YAML file."""
    os.makedirs(os.path.dirname(YAML_OUTPUT_FILE), exist_ok=True)
    
    try:
        with open(YAML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            if data: 
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2)
                print(f"Successfully wrote {len(data)} items to {YAML_OUTPUT_FILE}")
            else:
                f.write("# No valid media items processed to write to YAML.\n") 
                print(f"{YAML_OUTPUT_FILE} is empty or contains no valid items after processing.")
    except Exception as e:
        print(f"Error writing YAML file {YAML_OUTPUT_FILE}: {e}")

if __name__ == '__main__':
    print("Starting media gallery sync script...")
    
    missing_secrets = []
    if not GCP_SA_CREDENTIALS_JSON_STR:
        missing_secrets.append("GCP_SA_CREDENTIALS (JSON string is missing/empty)")
    if not GOOGLE_SHEET_ID:
        missing_secrets.append("GOOGLE_SHEET_ID (Sheet ID is missing/empty)")
    
    # MEDIA_SHEET_NAME uses a default in the script if the secret is not set or empty
    if not MEDIA_SHEET_NAME_FROM_ENV:
        print(f"Info: GitHub secret 'MEDIA_SHEET_NAME' not found or empty. Script will use default sheet name: '{EFFECTIVE_MEDIA_SHEET_NAME}'")
    else:
        print(f"Info: Using MEDIA_SHEET_NAME from GitHub secret: '{EFFECTIVE_MEDIA_SHEET_NAME}'")

    if missing_secrets:
        print(f"Fatal Error: Missing critical GitHub secrets: {', '.join(missing_secrets)}. Script cannot run.")
    else:
        print("All critical GitHub secrets (GCP_SA_CREDENTIALS, GOOGLE_SHEET_ID) appear to be present.")
        sheet_rows = fetch_sheet_data()
        if sheet_rows is not None: # fetch_sheet_data returns None on auth or critical fetch error
            yaml_data = format_for_yaml(sheet_rows)
            write_yaml_file(yaml_data)
        else:
            print("Failed to fetch sheet data (returned None). YAML file not updated.")
    
    print("Media gallery sync script finished.")