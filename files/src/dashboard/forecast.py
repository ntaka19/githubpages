import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import bisect
from zoneinfo import ZoneInfo

url = 'https://api.open-meteo.com/v1/forecast?latitude=35.69&longitude=139.69&hourly=temperature_2m,rain,showers&timezone=Asia%2FTokyo'

response = requests.get(url)
data = json.loads(response.text)


def draw_chart(data):
    labels = data['hourly']['time']
    new_labels = ['-'.join(element.split("-")[1:]) for element in labels]
    rain = data['hourly']['rain']
    showers = data['hourly']['showers']
    temperature = data['hourly']['temperature_2m']

    df = pd.DataFrame({'Date': new_labels,
                       'Temperature': temperature,
                       'Rain': rain,
                       'Showers': showers})

    fig, ax = plt.subplots(figsize=(10, 4))

    # Set the background color to black
    fig.set_facecolor('white')
    ax.set_facecolor('white')

    # Set the tick and title color to white
    ax.tick_params(colors='black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.title.set_color('black')

    #mark current time (hours) on the graph
    #bisec is not very efficient we know index is at the beginning (within first day)
    current_time = datetime.now(ZoneInfo("Asia/Tokyo")).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M')
    index = bisect.bisect_left(labels, current_time)
    if index < len(labels) and labels[index] == current_time:
        # Match found at index
        marker = [index]
    else:
        # No match found
        marker = [0]

    updated_time = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%H:%M')
    # plot data
    ax.plot(new_labels, temperature, '-D',markevery = marker, color='red', label='Temperature \n ' + "(updated:" + updated_time +")" )
    ax2 = ax.twinx()
    ax2.bar(new_labels, rain, color='blue', label='Rain')
    ax2.bar(new_labels, showers, color='green', label='Showers')

    ax2.set_ylim(0, 5)
    #https://withbrides.co.jp/lady/precipitation_amount-1mm/

    x_labels = [datetime.fromisoformat(label).strftime('%m-%d %a') for label in labels]

    #working ticks
    ax.set_xticks(range(0, len(x_labels), 12))
    ax.set_xticklabels([x_labels[i * 12] if i%2==0 else "" for i in range(len(x_labels[::12]))])

    #date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    #day_of_week = date_obj.strftime("%A")
    
    # set background color of xticks
    for i in range(0, len(new_labels), 24):
        counter = int(i/24)
        
        date_str = labels[i]
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        day_of_week = date_obj.strftime('%A')
        
        if counter % 2 == 0:
            ax.axvspan(i, i+24, facecolor='grey', alpha=0.1)
        else :
            ax.axvspan(i, i+24, facecolor='blue', alpha=0.1)

        #ax.text( i, 0.5, day_of_week, color='black', ha='center', va='center')
    # set labels and title
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature')
    ax2.set_ylabel('mm')
    ax.set_title('Weather Forecast (TOKYO) ' + labels[0].split('-')[0])

    # set legend
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    #plt.savefig('forecast2.png')
    plt.savefig('./docs/_images/forecast.png')

    """
    # Generate a dictionary with the data
    data_dict = {
        'updated date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # Write the dictionary to a file in JSON format
    with open('./docs/_images/updatetime_dict.json', 'w') as f:
        json.dump(data_dict, f)
    """
draw_chart(data)

