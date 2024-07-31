from RunnerLoop import RunnerStats
import pandas as pd
from datetime import date

#RunnerStats('Jeff Cushing','A8551393','8551393') #example for testing
df=pd.read_excel("RunnerLookupTable.xlsx")

today = str(date.today())
MyFilename = str("ParkrunCompiledResults" + today + ".xlsx")

#writer=pd.ExcelWriter("ParkrunCompiled.xlsx", engine="xlsxwriter")
with pd.ExcelWriter(MyFilename, engine="xlsxwriter") as writer:

    for i in range(len(df)):
        df_returned=RunnerStats(df.loc[i, "RunnerName"], df.loc[i, "RunnerID"], df.loc[i, "RunnerNumber"])
        #print(df_returned)
        df_returned.to_excel(writer,sheet_name=df.loc[i, "RunnerName"],index=False)

