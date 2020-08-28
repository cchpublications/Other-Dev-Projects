import os
import random
import time

from twilio.rest import Client
import pandas as pd
import numpy as np

# store sensitive information in .env file
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def date_to_int(date):
    return 10000 * date.year + 100 * date.month + date.day


def first_binary_search(message, low, high, start_date, n):
    if high >= low:
        mid = low + (high - low) // 2
        if (
            mid == 0 or start_date > date_to_int(message[mid - 1].date_created)
        ) and date_to_int(message[mid].date_created) == start_date:
            return mid
        elif start_date > date_to_int(message[mid].date_created):
            return first_binary_search(message, (mid + 1), high, start_date, n)
        else:
            return first_binary_search(message, low, (mid - 1), start_date, n)

    return -1


def last_binary_search(message, low, high, end_date, n):
    if high >= low:
        mid = low + (high - low) // 2
        if (
            mid == n - 1 or end_date < date_to_int(message[mid + 1].date_created)
        ) and date_to_int(message[mid].date_created) == end_date:
            return mid
        elif end_date < date_to_int(message[mid].date_created):
            return last_binary_search(message, low, (mid - 1), end_date, n)
        else:
            return last_binary_search(message, (mid + 1), high, end_date, n)

    return -1


def export(message, start, end):
    df = pd.DataFrame(columns=["From", "To", "Status", "Time", "Content", "Direction"])
    for m in message:
        new_row = pd.Series(
            {
                "From": m.date_created,
                "To": m.to,
                "Status": m.status,
                "Time": m.date_created,
                "Content": m.body,
                "Direction": m.direction,
            }
        )
        df = df.append(new_row, ignore_index=True,)

    print(df)

    hash = random.getrandbits(128)

    df.to_csv(str(hash) + "_example.csv", index=False, header=True)


def main():
    # start = 20200820
    # end = 20200821
    date_limit = 25000
    print("Date format is: 20200101")
    start = input("Enter start date:")
    end = input("Enter end date:")
    print("start")
    start = int(start)
    end = int(end)
    tic = time.perf_counter()
    while True:
        message = client.messages.list(limit=date_limit)
        message.reverse()
        date = message[0].date_created
        if date_to_int(date) < start:
            break
        date_limit += 10000
    message_length = len(message)
    x = first_binary_search(message, 0, message_length - 1, start, message_length)
    print("found lower date: " + str(x))
    y = last_binary_search(message, 0, message_length - 1, end, message_length)
    print("found upper date: " + str(y))
    message = message[x:y]
    export(message, x, y)
    toc = time.perf_counter()
    print(f"Export program execution time: {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()
