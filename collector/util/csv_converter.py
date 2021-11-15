""" MongoDB to CSV Converter """
import csv
import os
import re
from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from collector.collector.enums import RmqQueueName

MONGO_CLIENT: MongoClient = MongoClient(host="localhost", port=27017)
MONGO_DB: Database = getattr(MONGO_CLIENT, "ldbot")
QUEUE_NAME = RmqQueueName.ORDERBOOK_1S.value
MONGO_COLLECTION: Collection = getattr(MONGO_DB, QUEUE_NAME)

FIELD_NAMES = [
    "symbol",
    "timestamp",
    "datetime",
    "bids[2]",
    "bids[1]",
    "bids[0]",
    "asks[0]",
    "asks[1]",
    "asks[2]",
]


def mongo_export_to_file():
    today = datetime.today()
    today = today.strftime("%m-%d-%Y")
    # make an API call to the MongoDB server
    num = MONGO_COLLECTION.count_documents({})
    print(f"# of docs: {num}")
    if num == 0:
        return

    mongo_cur: Cursor = MONGO_COLLECTION.find()

    # pre-process
    rows = []
    for cur in mongo_cur:
        row = {}
        for k in FIELD_NAMES:
            if k.startswith("bids"):
                index = int(re.findall(r"\d+", k)[0])
                row[k] = cur["bids"][index][0]
            elif k.startswith("asks"):
                index = int(re.findall(r"\d+", k)[0])
                row[k] = cur["asks"][index][0]
            else:
                row[k] = cur[k]
        rows.append(row)

    # compute the output file directory and name
    output_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), f"{QUEUE_NAME}_{today}.csv"
    )
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    mongo_export_to_file()
