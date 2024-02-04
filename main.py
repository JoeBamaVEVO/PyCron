import sys
import time
import requests as req
import json
import os
from datetime import datetime, timedelta
import threading
import winsound



def createJsonFile():
    if not os.path.exists('jobs.json'):
        data = {
            "jobs": []
        }
        with open('jobs.json', 'w') as f:
            # Write updated data to file
            json.dump(data, f)

def displayChoices():
    print("please choose an option \n")
    print("1. Add a new cronjob")
    print("2. View all cronjobs")
    print("3. Delete a cronjob")
    print("4. Exit")
    option = input("Enter your option: ")
    print("\n")

    if option == "1":
        addCronjob()
    elif option == "2":
        viewCronjobs()
    elif option == "3":
        deleteCronjob()
    elif option == "4":
        exit()
    elif option == "":
        displayChoices()
    # return option

def addCronjob():
    url = input("Enter the url: ")
    if url == "":
        print("URL cannot be empty")
        addCronjob()
    interval = input("Enter the interval in minutes: ")
    if interval == "":
        print("Interval cannot be empty")
        addCronjob()
    print("Confirm the following details" + "\n" + "URL: " + url + "\n" + "Interval: " + interval + " minutes")
    confirm = input("Do you want to create a cronjob Y/n ?: ")
    if confirm == "n":
        print("Cronjob creation cancelled")
        displayChoices() 
    else:
        with open('jobs.json', 'r') as f:
            # Load JSON data from file
            data = json.load(f)
            data_length = len(data['jobs'])
            print("Number of cronjobs:", data_length)
            new_data = {
                str(data_length + 1): {
                    "url": url,
                    "interval": interval
                }
            }
            data['jobs'].append(new_data)
        with open('jobs.json', 'w') as f:
            # Write updated data to file
            json.dump(data, f)
        print("Cronjob added successfully \n")
        displayChoices()
            
def viewCronjobs():
    with open('jobs.json', 'r') as f:
        # Load JSON data from file
        data = json.load(f)
        data = data['jobs']
        num_of_job = len(data)
        i = 0
        longest_url_length = max(len(job[str(i + 1)]["url"]) for i, job in enumerate(data))
        print("{:<5} {:<{}} {:<10}".format("No.", "URL", longest_url_length + 10, "Interval"))
        for i in range(num_of_job):
            job = data[i][str(i + 1)]
            print("{:<5} {:<{}} {:<10}".format(str(i + 1), job["url"], longest_url_length + 10, job["interval"] + " minutes"))
            i += 1
        print("Press Enter to continue...")
        input()
        displayChoices()
            
def deleteCronjob():
    print("delete cronjob")
    id = input("Enter the id of the cronjob you want to delete: ")
    with open('jobs.json', 'r') as f:
        # Load JSON data from file
        data = json.load(f)
        data = data['jobs']
        data = {
            "jobs": [job for job in data if list(job.keys())[0] != id]
        }
        print(data)
    with open('jobs.json', 'w') as f:
        # Write updated data to file
        json.dump(data, f)
    print("Cronjob deleted successfully \n")
    input("Press Enter to continue...")
    displayChoices()

def exit():
    print("Goodbye!")
    stop_event.set()
    sys.exit()

def fetchCronjobs(): # Fetch cronjobs from the json file and calculate the next update time
    with open('jobs.json', 'r') as f:
        # Load JSON data from file
        data = json.load(f)
        data = data['jobs']
        joblist = []
        for job in data:
            job = list(job.values())[0]
            now = datetime.now()
            nextUpdate = now + timedelta(minutes=int(job["interval"]))
            data = {
                "url": job["url"],
                "interval": job["interval"], 
                "nextUpdate": nextUpdate
            }
            joblist.append(data)
        return joblist
    

def check_crontime(joblist, stop_event):
    while not stop_event.is_set():
        now = datetime.now()
        for job in joblist:
            if now >= job["nextUpdate"]:
                print("Time to update: ", job["url"])

                do_cronjob(job["url"])

                #Calculate new time for cronjob
                job["nextUpdate"] = now + timedelta(minutes=int(job["interval"]))
                print("Next update: ", job["nextUpdate"])

def do_cronjob(url):
    winsound.Beep(1000, 1000)
    print("Running cronjob: ", url)
    try:
        response = req.get(url)
        print(response.text)
    except:
        print("Failed to run cronjob: ", url)
    

if __name__ == "__main__":
    # Create a new json file if one does not exist
    createJsonFile()
    # Fetches all cronjobs from json, and calculates new update time
    # Returns a joblist with url, interval, and next execution time
    joblist = fetchCronjobs()
    # Prepares threading, create stop event
    stop_event = threading.Event()
    # start thread to check if it is time up do cronjob
    thread = threading.Thread(target=check_crontime, args=(joblist, stop_event,))
    thread.start()

    print("\n Welcome to kristian's cronjob mangement system \n")
    displayChoices()



# while True:
#     response = req.get('http://192.168.0.8/cron.php')
#     print(response.text + ' ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#     time.sleep(300)