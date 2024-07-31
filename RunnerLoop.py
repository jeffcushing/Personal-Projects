import numpy as np


def RunnerStats(runnername, runnerid, runnernumber):
    """The function takes a RunnerName and RunnerNumber and populates an XLS with stats from Rock Creek Parkrun
    Passing the Parkrun name could all for non Rock Creek events. """
    from io import StringIO
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    import time

    # print(runnername, runnerid,runnernumber)

    # General stuff
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    runner_url = str("https://www.parkrun.us/rockcreektrail/parkrunner/" + str(
        runnernumber) + "/")  # modify this if other events besides Rock Creek are desired

    # RunnerDF=pd.DataFrame(columns=["Run Date","Run Number","Pos","Time","Age Grade","PB?"]) #THIS MIGHT BE NECESSARY

    response = requests.get(runner_url, headers=headers)

    if response.status_code == 200:
        print(runnername + " page accessed successfully")
        # print(response.text)  # Print the content of the response
    else:
        print(f'Request failed with status code: {response.status_code}')
    PageText = response.text
    soup = BeautifulSoup(PageText, "html.parser")

    # Use the find_all function in the BeautifulSoup object, with element type `table`
    # Assign the result to a list called `html_tables`
    html_tables = soup.find_all('table')

    # Get the third table and check its content
    runner_results_table = html_tables[2]
    converted_string = StringIO(str(runner_results_table))
    data = pd.read_html(converted_string)[0]
    minutes = {}
    seconds = {}
    pacetemp = {}
    paceminutes = {}
    paceseconds = {}

    # RunnerDF = pd.concat([RunnerDF, data], axis=0,ignore_index=False) # Unnecessary - was incorrectly applied from GeneralStats

    data['Run Date'] = pd.to_datetime(data['Run Date'], format='%d/%m/%Y')  # was RunnerDF
    # data['Formatted Time'] = pd.to_datetime(data['Time'], format='%M:%S').dt.time
    minutes = pd.to_datetime(data['Time'], format='%M:%S').dt.minute
    seconds = pd.to_datetime(data['Time'], format='%M:%S').dt.second
    data['Time in Minutes'] = round(minutes + (seconds / 60),2)
    # data['Pace (Minutes)']=data['Time in Minutes']/3.1 #convert 5K to miles #this works but not sure about efficiency
    pacetemp = ((minutes + (seconds / 60)) / 3.1)

    paceminutes = np.floor(pacetemp)
   # paceseconds = (((pacetemp) % 1) * 60) #working dont delete
    paceseconds = np.floor(((pacetemp) % 1) * 60)
    # data['Pace Minutes'] = paceminutes.astype("string").replace('\.0', '', regex=True)
    # data['Pace Seconds'] = paceseconds.astype("string").replace('\.0', '', regex=True)
    # data['Pace Seconds']=data['Pace Seconds'].str.zfill(2)
    # data['Pace (M:S)'] = data['Pace Minutes'] + ":" + data['Pace Seconds']


    paceminutes = paceminutes.astype("string").replace('\.0', '', regex=True)
    paceseconds = paceseconds.astype("string").replace('\.0', '', regex=True)
    paceseconds=paceseconds.str.zfill(2)
    data['Pace (M:S)'] = paceminutes + ":" + paceseconds
    data['Date']=data['Run Date'].dt.strftime('%-m/%-d/%Y')
    data['Pace (Minutes)'] = round(pacetemp,2)




    # paceminutes = paceminutes.astype("string").replace('\.0', '', regex=True)
    # paceseconds = paceseconds.astype("string")
    # data['Pace (M:S)'] = paceminutes + ":" + paceseconds



    # data['combined']=(str(data['Pace Minutes'])+"test"+str(data['Pace Seconds']))

    # if (data['Time']) < '00:60:00':  # was RunnerDF
    #     print("more than 1 hour")
    #     data['Formatted Time'] = pd.to_datetime(data['Time'], format='%M:%S').dt.time  # was RunnerDF
    # else:
    #     data['Formatted Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time  # UNCOMMENT THIS FOR PRODUCTION
    #     # data['Formatted Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time  # UNCOMMENT THIS FOR PRODUCTION

    # key data for analyzing outside of Excel
    # print('Earliest date= ',min(RunnerDF['Run Date']))
    # print('Latest run date= ',max(RunnerDF['Run Date']))
    # print(RunnerDF[['Run Date','Run Number','Time']])

    return data  # was RunnerDF
