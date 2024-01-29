import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import numpy as np
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from sortedcontainers import SortedList

#note: most of the code here is taken from ChatGPT
#a decent amount of debugging and customization was required

def days_difference(date_string):
    target_date = datetime.strptime(date_string, '%Y-%m-%d')
    reference_date = datetime(2006, 4, 23)
    
    difference = target_date - reference_date
    return difference.days

# define player map
playermap={}
random.seed(69)

# URL of the website you want to scrape
url = 'https://liquipedia.net/smash/Five_Gods'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all elements with a specific class that contains article titles
    article_titles = soup.find_all(class_='template-box')
    
    # Loop through the found elements and extract the text (title)
    for title in article_titles:
        text=title.get_text()
        #print(text)

        # the gods loss counts appear in sections that can be edited
        if "[edit]" in text:
            god=text[1:text.find("[edit]")]
            #print(god)
            currentIndex=0
            nextIndex=text.find("20",0)
            while(nextIndex<len(text)):
                currentIndex=nextIndex
                nextIndex=text.find("20",currentIndex+10)
                if nextIndex==-1:
                    nextIndex=len(text)

                #playerProfileText is of the format "2017-10-08 | Plup x2"
                playerProfileText=text[currentIndex:nextIndex]
                #print(playerProfileText)

                #gets the date from the player profile
                dateText=playerProfileText[0:(playerProfileText.find("|")-1)]
                #print(dateText)

                #gets the player name from the player profile
                playerNameEndIndex=playerProfileText.find(" (")
                if playerNameEndIndex==-1:
                    # no "(Melee player in the name)"
                    playerNameEndIndex=playerProfileText.find(" x")
                playerName=playerProfileText[(playerProfileText.find("| ")+3):playerNameEndIndex]
                if playerName=="Mang0" or playerName=="Mew2King" or playerName=="Hungrybox" or playerName=="PPMD" or playerName=="Armada":
                    continue
                    #don't inclue the 5 gods
                #print(playerName)
                dateNumber=days_difference(dateText)
                if playerName not in playermap:
                    playermap[playerName]=[]
                playermap[playerName].append([dateNumber,god])
else:
    print('Failed to retrieve the page')

for playerName,data in playermap.items():
    data.sort()

# print(playermap)
# at this point in the code, playermap contains a full map of all the player who have defeated a god
# in the format 'Ken': [62,490]
# where the numbers are the number of days since M2k's first loss (07/22/2007)
                

noWords=True

# Create a new figure and axis
fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.set_box_aspect(0.5)


# Create a colormap
num_colors = len(playermap)
colors = cm.get_cmap('hsv', num_colors)

# Loop through the data and plot each SortedList
for index, (name, values) in enumerate(playermap.items(), start=1):
    x_values = list(values[0])
    y_values = list(range(1, len(x_values) + 1))
    color = colors(random.randint(0, len(playermap)))  # Get a color from the colormap
    if(len(x_values)>1):
        ax.plot(x_values, y_values, marker='o', color=color, label=name)
    else:
        ax.plot(x_values, y_values, marker='o', color=color)

    if( not noWords and len(x_values)>1):
        # Annotate the final point with the name above it
        final_point = (x_values[-1], y_values[-1])
        ax.annotate(name, final_point, textcoords="offset points", xytext=(0,10),
                    ha='center', fontsize=5, color='white')

# Add horizontal grid lines at each integer y-value
ax.set_yticks(np.arange(0.0, 6.0, 1.0))
ax.yaxis.grid(True, linestyle='dashed', color='gray', alpha=1)

# Set legend color and fontsize to white and smaller size
if(not noWords):
    legend = ax.legend()
    legend.set_draggable(True)

# Display the plot
if(not noWords):
    plt.show()
else:
    plt.savefig('5Gods_Plot.png',dpi=1000)


# This code writes the results to a CSV file

# Open a CSV file in write mode
with open('fivegodsdefeated.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Iterate through the map items
    for name, sorted_list in playermap.items():
        # Write a row with the key followed by each element in the SortedList
        row=[name]
        for date in sorted_list:
            row.append(date)
        csv_writer.writerow(row)




