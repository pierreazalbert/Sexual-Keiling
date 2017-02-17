import paho.mqtt.client as mqtt
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as dates
from termcolor import colored, cprint

# global dictionnary to access message from all functions easily
global data
data = {}

# global pandas dataframe to access data log from all functions easily
global df
df = pd.DataFrame()

# initialise live plot
fig, [ax1, ax2, ax3] = plt.subplots(3, 1, sharex=True, sharey=False)
fig.set_dpi(300)
fig.set_size_inches(15,8)
fig.suptitle('Tempo.o Demo', fontsize=20)
plt.subplots_adjust(left=0.1, right=0.85)
plt.style.use('bmh')
fig.patch.set_facecolor('white')

# runs when successful connection to server is made
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_prefix)
    print("subscribed to", topic_prefix)

# runs when message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    msg_string = msg.payload.decode('UTF-8')
    message = json.loads(msg_string)
    global data
    data = { message['datetime'] : {key: message[key] for key in ['humi', 'temp', 'max_accel']} }

print('\n******************************************')
print('Welcome to the Sexual Keiling MQTT monitor')
print('******************************************\n')
print('Are you connected to the EEERover wifi?')

broker_address = '192.168.0.10'
#broker_address = 'iot.eclipse.org' # test server
topic_prefix = 'esys/sexual-keiling'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# todo check paho doc for a way to save this from infinite loop if no connection is made
client.connect(broker_address)

# function to determine message to show according to humidity data received
def humidity_status():
    if df['humi'].iloc[-1] > 65:
        status = 'Too humid'
        color = 'red'
    elif df['humi'].iloc[-1] > 55:
        status = 'Slightly humid'
        color = 'orange'
    elif df['humi'].iloc[-1] > 45:
        status = 'OK'
        color = 'green'
    elif df['humi'].iloc[-1] > 35:
        status = 'Slightly dry'
        color = 'orange'
    else:
        status = 'Too dry'
        color = 'red'
    if df['humi_var'].iloc[-1] > 40:
        status = 'Unstable'
        color = 'orange'
    return status, color

# function to determine message to show according to accelerometer data received
def movement_status():
    if df['accel_var'].iloc[-1] < -50:
        status = 'Impact'
        color = 'red'
        text = ("IMPACT RECORDED AT " + str(df['accel_var'].index[-1]))
        text = colored(text, 'red', attrs=['bold', 'blink'])
        print(text)
    elif df['max_accel'].iloc[-1] > 60:
        status = 'Shaking'
        color = 'orange'
    else:
        status = 'OK'
        color = 'green'
    return status, color

# function to determine message to show according to temperature data received
def temperature_status():
    if df['temp'].iloc[-1] > 30:
        status = 'Too hot'
        color = 'red'
    elif df['temp'].iloc[-1] > 25:
        status = 'Slightly hot'
        color = 'orange'
    elif df['temp'].iloc[-1] > 20:
        status = 'OK'
        color = 'green'
    elif df['temp'].iloc[-1] > 15:
        status = 'Slightly cold'
        color = 'orange'
    else:
        status = 'Too cold'
        color = 'red'
    if df['temp_var'].iloc[-1] > 2:
        status = 'Unstable'
        color = 'orange'
    return status, color

# matplotlib function that will be used to update the graph
def animate(i):
    global df

    # get messages from mqtt broker with 1s timeout
    client.loop(1.0)

    # append each new message to pandas dataframe
    newline = pd.DataFrame.from_dict(data, orient='index')
    df = df.append(newline)
    df.index = pd.DatetimeIndex(df.index)

    # keep only last 24 hours of data
    if len(df.index) > 24*60*60*60:
        df.drop(df.iloc[0].name, inplace=True)

    if df.empty is False:
        
        df.drop_duplicates()
        
        # calculate instantaneous derivatives of each signal
        df['humi_var'] = df['humi'].diff().apply(lambda x: x**2).rolling(50).max()
        df['temp_var'] = df['temp'].diff().apply(lambda x: x**2).rolling(50).max()
        df['accel_var'] = df['max_accel'].diff()#.rolling(5).std()

        # clear whole figure before re-drawing
        ax1.clear()
        ax2.clear()
        ax3.clear()

        # plot dataframe containing humidity, temperature and acceleration data
        df['humi'].plot(ax=[ax1], subplots=True)
        df['max_accel'].plot(ax=[ax2], subplots=True)
        df['temp'].plot(ax=[ax3], subplots=True)
        #df['humi_var'].plot(ax=[ax1], subplots=True, secondary_y=True)
        #df['accel_var'].plot(ax=[ax2], subplots=True, secondary_y=True)
        #df['temp_var'].plot(ax=[ax3], subplots=True, secondary_y=True)

        # format axis 1 - humidity
        ax1.lines[0].set_linewidth(5)
        ax1.set_ylim(0,100)
        ax1.set_ylabel('Humidity (%)', fontsize=12)
        ax1.legend().set_visible(False)
        #ax1.right_ax.yaxis.set_visible(False)

        ax1.axhspan(0,35, facecolor='r', alpha=0.3)
        ax1.axhspan(35,45, facecolor='orange', alpha=0.3)
        ax1.axhspan(45,55, facecolor='g', alpha=0.3)
        ax1.axhspan(55,65, facecolor='orange', alpha=0.3)
        ax1.axhspan(65,100, facecolor='r', alpha=0.3)

        # format axis 2 - acceleration
        ax2.lines[0].set_linewidth(5)
        ax2.set_ylabel('Acceleration (%)', fontsize=12)
        ax2.legend().set_visible(False)
        #ax2.right_ax.yaxis.set_visible(False)

        ax2.axhspan(0,20, facecolor='green', alpha=0.3)
        ax2.axhspan(20,60, facecolor='orange', alpha=0.3)
        ax2.axhspan(60,ax2.get_ylim()[1], facecolor='red', alpha=0.3)

        # format axis 3 - temperature
        ax3.lines[0].set_linewidth(5)
        ax3.set_ylabel('Temperature (%)', fontsize=12)
        ax3.set_xlabel('Time', fontsize=15)
        ax3.legend().set_visible(False)
        #ax3.right_ax.yaxis.set_visible(False)

        ax3.axhspan(0,15, facecolor='r', alpha=0.3)
        ax3.axhspan(15,20, facecolor='orange', alpha=0.3)
        ax3.axhspan(20,25, facecolor='g', alpha=0.3)
        ax3.axhspan(25,30, facecolor='orange', alpha=0.3)
        ax3.axhspan(30,ax3.get_ylim()[1], facecolor='r', alpha=0.3)

        # display status message next to humidity subplot
        status, color = humidity_status()
        ax1.text(1.02, 0.6, 'Humidity',
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax1.transAxes,
                 color='black', fontsize=20)
        ax1.text(1.02, 0.4, status,
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax1.transAxes,
                 color=color, fontsize=20)

        # display status message next to movement subplot
        status, color = movement_status()
        ax2.text(1.02, 0.6, 'Movement',
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax2.transAxes,
                 color='black', fontsize=20)
        ax2.text(1.02, 0.4, status,
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax2.transAxes,
                 color=color, fontsize=20)

        # display status message next to temperature subplot
        status, color = temperature_status()
        ax3.text(1.02, 0.6, 'Temperature',
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax3.transAxes,
                 color='black', fontsize=20)
        ax3.text(1.02, 0.4, status,
                 verticalalignment='center', horizontalalignment='left',
                 transform=ax3.transAxes,
                 color=color, fontsize=20)

    else:
        print('Waiting for data...')

# animate plot by updating it using the animate() function every 0.5 seconds
ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()
