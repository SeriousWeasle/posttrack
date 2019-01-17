#import required modules for the script to work
from lxml import html
import requests
import time

#define needed variables
url_base = "https://derpibooru.org/pages/"
url_tags = url_base + "tags"
url_stats = url_base + "stats"

#define used tags
tags_list = ['safe', 'suggestive', 'questionable', 'explicit', 'semi-grimdark', 'grimdark', 'grotesque', 'total', 'timestamp', 'timestep']

#define an empty dict for the tags and the start value to be defined to
tags_startamount = dict()

#define the keys and values in the dict for start amounts
for tag in tags_list:
    with open ("variables/constant/" + tag + ".txt", 'r') as readStart:
        start_value = readStart.read()
        tags_startamount[tag] = start_value

#code that retrieves the variable every hour goes here
while 1:
    #get if this is the first run and store the variable
    with open ("variables/firstrun.txt", 'r') as firstRunChecker:
        isFirstRun = firstRunChecker.read()

    #if this is not the first run, get the results from the previous run
    if (isFirstRun == '0'):
        tags_previousamount = dict()
        for tag in tags_list:
            with open ("variables/temp/" + tag + ".txt", 'r') as readPrevious:
                previous_value = readPrevious.read()
                tags_previousamount[tag] = previous_value

    #get the data for the current run
    pagetags = requests.get(url_tags)
    treepagetags = html.fromstring(pagetags.content)
    tags_current_unformatted = treepagetags.xpath("//span[@class='tag__count']/text()")[0:7]

    #make sure that the currCleanIndex is 0 and the current dict is empty
    currCleanIndex = 0
    tags_currentamount = dict()

    for tag in tags_list[0:7]:
        #clean tags and put them in a dict
        current_cleantag = tags_current_unformatted[currCleanIndex][1:len(tags_current_unformatted[currCleanIndex])-1]
        tags_currentamount[tag] = current_cleantag
        currCleanIndex = currCleanIndex + 1

    #get the stats page and extract the total unremoved posts from it
    pagestats = requests.get(url_stats)
    treepagestats = html.fromstring(pagestats.content)
    tags_currentamount[tags_list[7]] = treepagestats.xpath("//span[@class='stat']/text()")[0].replace(",", "")

    #add the timestamp to the current data
    tags_currentamount[tags_list[8]] = float(time.time()) - float(tags_startamount[tags_list[8]])

    #if this is the first run, execute the following code block
    if (isFirstRun == '1'):
        tags_currentamount[tags_list[9]] = float(tags_currentamount[tags_list[8]])

        #write current stuff to temp variables folder
        for tag in tags_list:
            with open ("variables/temp/" +  tag + ".txt", 'w') as dcmt:
                dcmt.write(str(tags_currentamount[tag]))

        #calculate the difference between start of the measurement and now
        tags_sincestartamount = dict()
        for tag in tags_list:
            if (tag == 'timestamp' or tag == 'timestep'):
                tags_sincestartamount[tag] = float(tags_currentamount[tag])
            else:
                tags_sincestartamount[tag] = int(tags_currentamount[tag]) - int(tags_startamount[tag])

        #add the found data to the countup
        for tag in tags_list:
            with open("output/output_countup.txt", 'a') as dcmt:
                if (tag == 'timestep'):
                    dcmt.write(str(tags_sincestartamount[tag]) + "\n"
                    "")
                else:
                    dcmt.write(str(tags_sincestartamount[tag]) + ", ")
    
    #set the isFirstRun to 0 since the first run just happened
    with open ("variables/firstrun.txt", 'w') as dcmt:
        dcmt.write('0')
    
    #if it is not the first run, execute this instead
    if (isFirstRun == '0'):
        tags_currentamount[tags_list[9]] = float(tags_currentamount[tags_list[8]]) - float(tags_previousamount[tags_list[8]])
        #write current stuff to temp variables folder
        for tag in tags_list:
            with open ("variables/temp/" +  tag + ".txt", 'w') as dcmt:
                dcmt.write(str(tags_currentamount[tag]))
        
        #calculate the difference between start of the measurement and now
        tags_sincestartamount = dict()
        for tag in tags_list:
            if (tag == 'timestamp' or tag == 'timestep'):
                tags_sincestartamount[tag] = float(tags_currentamount[tag])
            else:
                tags_sincestartamount[tag] = int(tags_currentamount[tag]) - int(tags_startamount[tag])

        #add the found data to the countup
        for tag in tags_list:
            with open("output/output_countup.txt", 'a') as dcmt:
                if (tag == 'timestep'):
                    dcmt.write(str(tags_sincestartamount[tag]) + "\n"
                    "")
                else:
                    dcmt.write(str(tags_sincestartamount[tag]) + ", ")
        
        #declare a dict for the difference in tag amounts
        tags_differenceamount = dict()

        #calculate the difference in posts since last time
        for tag in tags_list:
            if (tag == 'timestamp' or tag == 'timestep'):
                tags_differenceamount[tag] = float(tags_currentamount[tag])
            else:
                tags_differenceamount[tag] = int(tags_currentamount[tag]) - int(tags_previousamount[tag])

        #add the tag difference output to the output_difference file

        for tag in tags_list:
            with open("output/output_difference.txt", 'a') as dcmt:
                if (tag == 'timestep'):
                    dcmt.write(str(tags_differenceamount[tag]) + "\n"
                    "")
                else:
                    dcmt.write(str(tags_differenceamount[tag]) + ", ")

    #prevent the code from running as fast as possible, causing the process to freeze and log the current output

    #output findings to the terminal in a user readable format:
    if (isFirstRun == '1'):
        print('#'*16)
        print("Amount of posts under each tag posted since start as of " + str(time.asctime(time.localtime(time.time()))) + ":")
        print("#"*16)
        for tag in tags_list:
            if (tag != 'timestamp' and tag != 'timestep'):
                print(str(tag) + ": " + str(tags_sincestartamount[tag]))
        print("")
        print("")
        print("")
    
    if (isFirstRun == '0'):
        print('#'*16)
        print("Amount of posts under each tag posted since start as of " + str(time.asctime(time.localtime(time.time()))) + ":")
        print("#"*16)
        for tag in tags_list:
            if (tag != 'timestamp' and tag != 'timestep'):
                print(str(tag) + ": " + str(tags_sincestartamount[tag]))
        print("")
        print('#'*8)
        print("Changes in posts under tag since last count:")
        print('#'*8)
        for tag in tags_list:
            if (tag != 'timestamp' and tag != 'timestep'):
                print(str(tag) + ": " + str(tags_differenceamount[tag]))
        print("")
        print("")
        print("")
    time.sleep(3600)