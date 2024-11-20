import requests
import pandas as pd
import time
from tqdm import tqdm

# Replace with your actual email and API key
email = 'sanjaymythili2002@gmail.com'
key = 'mauvegazelle47'

# List of pollutant codes
pollutants = [42101, 42401, 42602, 44201, 88101, 45201, 81102, 85219, 14129]

# Base URL for the API
base_url = 'https://aqs.epa.gov/data/api/dailyData/byState'

# Year range for the data (2017 to 2021)
start_year = 2017
end_year = 2021

# State code for Colorado (08 in this case)
state_code = '08'

# Empty list to store the data
all_data = []

# Loop through each year first, then through pollutants
for year in tqdm(range(start_year, end_year + 1), desc="Year Progress"):
    for pollutant in pollutants:
        # Define the start and end date for the entire year
        bdate = f'{year}0101'
        edate = f'{year}1231'

        # Create the API request URL
        url = f"{base_url}?email={email}&key={key}&param={pollutant}&bdate={bdate}&edate={edate}&state={state_code}"

        # Make the API request
        response = requests.get(url)

        # Check if the response is valid
        if response.status_code == 200:
            data = response.json()
            if 'Data' in data and data['Data']:
                all_data.extend(data['Data'])
            else:
                print(f"No data found for pollutant {pollutant} in {year}")
        else:
            print(
                f"Failed to retrieve data for year {year} and pollutant {pollutant}: {response.status_code}")

        # Sleep for a second to avoid hitting the API too frequently
        time.sleep(1)

# Convert the list of data to a pandas DataFrame
df = pd.DataFrame(all_data)

# Display the first few rows of the DataFrame
print(df.head())

# Save the DataFrame to a CSV file
df.to_csv('all_pollutant_data_2017_2021.csv', index=False)
