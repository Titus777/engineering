import requests
from bs4 import BeautifulSoup

# Supabase URL and API Key
SUPABASE_URL = "https://ailogxgeobaebkemxgho.supabase.co"  # Replace with your actual Supabase project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFpbG9neGdlb2JhZWJrZW14Z2hvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0NDAxNzEsImV4cCI6MjA0MTAxNjE3MX0.YJD16IimFgt2xfoYt5JoLUmYVtt37RlxTfYJmN4TMcQ"  # Replace with your actual Supabase API key
SUPABASE_TABLE = "engineering_works"  # Replace with your table name

# Function to insert data into Supabase
def insert_into_supabase(data):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Data inserted successfully")
    else:
        print(f"Failed to insert data: {response.status_code}, {response.text}")

# Function to call the delete function in Supabase
def delete_old_data():
    url = f"{SUPABASE_URL}/rest/v1/rpc/delete_old_data"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Old data deleted successfully")
    else:
        print(f"Failed to delete old data: {response.status_code}, {response.text}")

# URL of the webpage containing the HTML element
url = "https://www.nationalrail.co.uk/status-and-disruptions/"

try:
    # Call the delete function before inserting new data
    delete_old_data()
    
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the section containing planned engineering works using the class
    engineering_section = soup.find("div", class_="styled__StyledIncidentListGroups-sc-5kws0u-1 eLIyDc")

    if engineering_section:
        # Find all the list items within this section
        engineering_items = engineering_section.find_all("li", class_="styled__StyledNotificationListItem-sc-nisfz3-3 dZudnM")

        # Iterate through each item and extract details
        i = 0
        for item in engineering_items:
            i = i+1
            if i >= 8:
                # Extract the link
                link = item.find("a").get("href") if item.find("a") else "No link available"
                full_link = f"https://www.nationalrail.co.uk{link}"  # Prepend base URL if necessary

                # Extract the summary (main text)
                summary_tag = item.find("p", class_="styled__StyledParagraph-sc-1bdsaxr-1 dAAkXV")
                summary = summary_tag.text if summary_tag else "No summary available"

                # Create a data dictionary
                data = {
                    "headline": "Planned Engineering Works",
                    "link": full_link,
                    "summary": summary
                }

                # Insert the data into Supabase
                insert_into_supabase(data)

                # Print the extracted information (optional)
                print(f"Headline: Planned Engineering Works")
                print(f"Link: {full_link}")
                print(f"Summary: {summary}")
                print("-" * 30)
    else:
        print("Engineering works section element not found. Information might be unavailable or the website structure might have changed.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the webpage: {e}")
