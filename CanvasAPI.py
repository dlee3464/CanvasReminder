import requests
import time
from datetime import datetime
from Reminder import *
from GoogleCalendar import makeEvent



user_id = "1093982"

token = "fHoASehTg5yse1anJ1bfUF6ZdImUyBlrjt4oOdSDuleitP9twEEeY2JEpMagI2Ow"

account_id = "45"

header = {"Authorization" : f"Bearer {token}"}

base_url = "https://gatech.instructure.com/api/v1/"

r = requests.get(base_url + "users/" + user_id + "/courses", headers=header)

data = r.json()

#today's date
today = datetime.now()

def toDateTime(due):
    dueList = due.split(" ")
    dateSpl = dueList[0]
    dateSpl = dateSpl.split("-")
    first = dateSpl[0]
    sec = dateSpl[1]
    third = dateSpl[2]

    dateSpl[0], dateSpl[1], dateSpl[2] = sec, third, first
    dateSpl[2] = dateSpl[2].replace("20", "")

    due = dateSpl[0] + "/" + dateSpl[1] + "/" + dateSpl[2] + " " + dueList[1]

    #due date to datetime object
    dateFormat = '%m/%d/%y %H:%M:%S'
    return datetime.strptime(due, dateFormat)

for elem in data:
    course_id = str(elem['id'])
    rAssign = requests.get(base_url + "courses/" + course_id + "/assignments", headers=header)
    dataAssign = rAssign.json()
    for assignment in dataAssign:
        if assignment['due_at'] == None or assignment['unlock_at'] == None:
            continue

        #due date as string
        due = assignment['due_at'].replace("T", " ")
        due = due.replace("Z", " ")

        #due date to datetime object
        newDue = toDateTime(due)


        unlocked = assignment['unlock_at'].replace("T", " ")
        unlocked = due.replace("Z", " ")
        newUnlocked = toDateTime(unlocked)

        if (today > newDue) or (datetime.now() + timedelta(minutes=59) < newUnlocked):
            continue


        unlock = assignment['unlock_at'].split("T")
        unlockDate = unlock[0]
        unlockTime = unlock[1].replace('Z', '')

        dateFormat = '%Y-%m-%d'
        newUnlock = datetime.strptime(unlockDate, dateFormat).date()

        dueStr = str(newDue).split(' ')
        endTime = dueStr[1]
        endTime = endTime.split(':')

        monthList = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        dueStr = dueStr[0].split('-')
        endDate = []
        for elem in dueStr:
            endDate.append(elem)

        dueStr[1] = monthList[int(dueStr[1]) - 1]
        dueStr = dueStr[1] + ' ' + dueStr[2] + ', ' + dueStr[0]

        startDate = unlockDate.split('-')
        startTime = unlockTime.split(':')


        due = "Due at " + dueStr + "!"
        notify(assignment['name'], 'REMINDER', due)

        startDate = [int(i) for i in startDate]
        startTime = [int(i) for i in startTime]
        endDate = [int(i) for i in endDate]
        endTime = [int(i) for i in endTime]

        makeEvent(startDate[0], startDate[1], startDate[2], startTime[0], startTime[1], endDate[0], endDate[1], endDate[2], endTime[0], endTime[1], assignment['name'], due, 'djlee3464@gmail.com')
