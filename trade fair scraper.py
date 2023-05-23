from nsdotpy.session import NSSession
import csv
from bs4 import BeautifulSoup

# Create a session
session = NSSession("Trade Fair Info Grabber", "1.0.0", "Sweeze", "Sweeze")

# get data from csv file
data = []
with open("trade_fair_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    data.extend(iter(reader))
url = "https://www.nationstates.net/template-overall=none/page=tradefair_log"

for i in range(len(data), 296525, 25):
    formdata = {
        "start": i,
    }
    print(f"Requesting page {i}")
    response = session.request(url, formdata)
    soup = BeautifulSoup(response.text, "lxml")
    # Get the list of trade fair events
    events = soup.find_all("li")
    # Iterate through the events
    for event in events:
        timestamp = event.find("time").attrs["data-epoch"]
        action = event.text.split(": ")[1]
        # Add the data to the list
        data.append((timestamp, action))
    # Write the data to a csv file to pick back up in case the program crashes somehow, only every 100 or so pages to avoid unnecessary disk writes
    if i % 10000 == 0:
        print("Writing to file")
        with open("trade_fair_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "action"])
            writer.writerows(data)

print("Writing to file")
with open("trade_fair_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "action"])
    writer.writerows(data)