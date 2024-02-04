import sys
import time
import requests as req
import json
import os

def createJsonFile():
    if not os.path.exists('jobs.json'):
        data = {
            "jobs": []
        }
        with open('jobs.json', 'w') as f:
            # Write updated data to file
            json.dump(data, f)

def displayChoices():
    print("please choose an option")
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
        pass
    # return option

def addCronjob():
    url = input("Enter the url: ")
    interval = input("Enter the interval in minutes: ")
    print("Confirm the following details" + "\n" + "URL: " + url + "\n" + "Interval: " + interval + " minutes")
    confirm = input("Do you want to create a cronjob Y/n ?: ")
    if confirm == "n":
        print("Cronjob creation cancelled") 
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
    sys.exit()
    
    
    
createJsonFile()
print("\n Welcome to kristian's cronjob mangement system \n")

displayChoices()



# while True:
#     response = req.get('http://192.168.0.8/cron.php')
#     print(response.text + ' ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#     time.sleep(300)