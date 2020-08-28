import os
import pandas as pd
import numpy as np
import time


from twilio.rest import Client

# can either have the twilio.env in the same directory, or manually fill in the numbers here
# If you do manually fill in  your sid and token here, please make sure not to share this file with anyone!
# account_sid = 'your_account_sid'
# auth_token = 'your_auth_token'
# ^ if using this process, comment the two below lines.
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def main():

    # your csv file name goes here
    file_name = str(input("Please enter the name of your csv file. "))
    csv_file = pd.read_csv(file_name)

    tic = time.perf_counter()
    for index, row in csv_file.iterrows():
        try:
            message = client.messages.create(
                body="Hello " + str(row["FirstName"]) + ". " + str(row["Body"]),
                from_="+12132050662",
                to=int(row["Cell"]),
            )
        except:
            print(
                "Could not send message to "
                + str(row["FirstName"])
                + " "
                + str(row["LastName"])
                + "."
            )
    toc = time.perf_counter()
    print(f"SMS program execution time: {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()
