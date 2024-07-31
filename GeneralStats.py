from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

# General stuff
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
runner_url = "https://www.parkrun.us/rockcreektrail/parkrunner/8551393/"

race_start=input("Enter race number to start at (124?): ") #start at 126
race_end=input("Enter race number to end at:")
num_start=int(race_start)
num_end=int(race_end)
TotalDF=pd.DataFrame(columns=["Run Number","Position","parkrunner","Gender","Age Group","Club","Time"])
#TotalDF=pd.DataFrame(columns=["Run Date","Run Number","Position","Time","Age Grade","PB?"])


# Main loop
data= []
for i in range (num_start,num_end):
#    print ("Counter: ",i)
    location_url="https://www.parkrun.us/rockcreektrail/results/"+ str(i)

    response = requests.get(location_url, headers=headers)

    if response.status_code == 200:
        print("page accessed successfully")
        #print(response.text)  # Print the content of the response
    else:
        print(f'Request failed with status code: {response.status_code}')
    PageText=response.text
    soup = BeautifulSoup(PageText, "html.parser")

    # Use the find_all function in the BeautifulSoup object, with element type `table`
    # Assign the result to a list called `html_tables`
    html_tables = soup.find_all('table')

    # Let's print the first table and check its content
    overall_results_table = html_tables[0]
    #data=pd.read_html(str(overall_results_table))[0]
    converted_string=StringIO(str(overall_results_table)) #replacement for above line due to deprication of literal string
    data=pd.read_html(converted_string)[0]
    data.insert(0,'Run Number',i+1) #Adds the race number (+1 because i starts at 0)
    #print(type(TotalDF))
    TotalDF = pd.concat([TotalDF, data], axis=0,ignore_index=False)
    print("End of loop ", i)

#print(TotalDF.to_clipboard(excel=True))
today = str(date.today())
MyFilename=str("ParkrunResults"+today+".xlsx")
TotalDF.to_excel(MyFilename,sheet_name="RockCreek", index=False)

print("done")



