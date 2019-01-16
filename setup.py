#importing modules required for the code to run
from lxml import html
import time
import requests

#define variables needed for the script to work
url_base = "https://derpibooru.org/pages/"
url_tags = url_base + "tags"
url_stats = url_base + "stats"
postsCleaned = 0
current_variable = 0
tags_postamount_formatted = []

#define the url to retrieve the information from and get the page content
pagetags = requests.get(url_tags)
treepagetags = html.fromstring(pagetags.content)

#generate column headers for excel to label each number with the corresponding tag
tags_list = ['safe', 'suggestive', 'questionable', 'explicit', 'semi-grimdark', 'grimdark', 'grotesque', 'total', 'timestamp', 'timestep']

#retrieve all numbers from the URL defined above and declare them as the variable tags_postamount_unformatted
tags_postamount_unformatted_all = treepagetags.xpath("//span[@class='tag__count']/text()")

#remove unnessacary tags which do not really count toward the worksafe rating
tags_postamount_unformatted = tags_postamount_unformatted_all[0:7]

#remove brackets from array indexes in the tags_postamount_unformatted array and put the cleaned up versions in the tags_postamount array

for each in tags_postamount_unformatted:
    #get the current unsanitized array index and set it as a current working variable
    postamount_current_tag_unformatted = tags_postamount_unformatted[postsCleaned]
    #remove the first and last character from the current post amount and define this as a variable
    postamount_current_tag_formatted = postamount_current_tag_unformatted[1:len(postamount_current_tag_unformatted)-1]
    #add the sanitized output to the array of cleaned outputs
    tags_postamount_formatted.append(postamount_current_tag_formatted)
    #increment the tag array index number
    postsCleaned = postsCleaned + 1

#get the stats page
pagestats = requests.get(url_stats)
treepagestats = html.fromstring(pagestats.content)
#get the total unremoved posts stat and clean the variable
totalPosts = treepagestats.xpath("//span[@class='stat']/text()")[0].replace(",", "")
#add it to the formatted postamounts at the end
tags_postamount_formatted.append(totalPosts)

#add the current time as timestamp to the array
tags_postamount_formatted.append(str(time.time()))

#add a timestep of 0 to the starting point
tags_postamount_formatted.append('0')

#reset the output file to make sure it does not mess up
with open ("output/output_countup.txt", 'w') as dcmt:
    dcmt.write("")

with open ("output/output_difference.txt", 'w') as dcmt:
    dcmt.write("")

#create a document for each tag and the total amount, write the number associated with the tag and move on to the next
for tag in tags_list:
    with open ("variables/constant/" +  tag + ".txt", 'w') as dcmt:
        dcmt.write(tags_postamount_formatted[current_variable])
        current_variable = current_variable + 1 

    #check if the current tag is timestep, if not append a comma
    if (tag != 'timestep'):
        with open ("output/output_countup.txt", 'a') as dcmt:
            dcmt.write(tag + ",")
    
    #if current tag is timestep, append an enter
    else:
        with open ("output/output_countup.txt", 'a') as dcmt:
            dcmt.write(tag + "\n"
            "")
    
    #check if the current tag is timestep, if not append a comma
    if (tag != 'timestep'):
        with open ("output/output_difference.txt", 'a') as dcmt:
            dcmt.write(tag + ",")
    
    #if current tag is timestep, append an enter
    else:
        with open ("output/output_difference.txt", 'a') as dcmt:
            dcmt.write(tag + "\n"
            "")

writeStartTag = 0

for entry in tags_postamount_formatted:
    if (writeStartTag == len(tags_postamount_formatted)-1):
        with open ("output/output_countup.txt", 'a') as dcmt:
            dcmt.write(str(tags_postamount_formatted[writeStartTag]) + "\n"
            "")
    
    if (writeStartTag < len(tags_postamount_formatted) - 1):
        with open ("output/output_countup.txt", 'a') as dcmt:
            dcmt.write(str(tags_postamount_formatted[writeStartTag]) + ", ")
    
    writeStartTag = writeStartTag + 1
    
#make sure that firstrun is set to true
with open ("variables/firstrun.txt", 'w') as dcmt:
    dcmt.write("1")

print (tags_list)
print (tags_postamount_formatted)
print ("Successfully finished setup for postcounter v3.0")
print (len(tags_postamount_formatted))
#set the starting amount of posts to calculate the total amount of posts since start. This allows for interrupts and restarts