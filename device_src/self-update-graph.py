import paho.mqtt.client as mqtt
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as dates

global data
data = {}

global df
df = pd.DataFrame()

fig, [ax1, ax2, ax3] = plt.subplots(3, 1, sharex=True, sharey=False)
fig.set_dpi(300)
fig.set_size_inches(15,10)
fig.suptitle('Tempo.o Demo', fontsize=20)

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
    dict_derulo = json.loads(msg_string)
    global data
    data = {datetime.datetime.now():dict_derulo}

print('\n******************************************')
print('Welcome to the Sexual Keiling MQTT monitor')
print('******************************************\n')
print('Are you connected to the EEERover wifi?')

broker_address = '192.168.0.10'
#broker_address = 'iot.eclipse.org' # test server
topic_prefix = 'esys/sexual-keiling/'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# todo check paho doc for a way to save this from infinite loop if no connection is made
client.connect(broker_address)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

def animate(i):
    global df
    
    # get messages from mqtt broker
    client.loop(1.0)
    
    # append each new message to pandas dataframe
    newline = pd.DataFrame(data).T
    df = df.append(newline)
    
    # keep only last 24 hours of data
    if len(df.index) > 24*60*60*60:
        df.drop(df.iloc[0].name, inplace=True)

    if df.empty is False:
        
        # clear whole figure before re-drawing
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        # plot dataframe containing humidity, temperature and acceleration data
        df.plot(ax=[ax1, ax2, ax3], subplots=True)
        
        # format axis 1 - humidity
        ax1.set_ylim(0,100)
        ax1.set_ylabel('Humidity (%)', fontsize=15)
        ax1.legend().set_visible(False)
        
        # format axis 2 - acceleration
        ax2.set_ylim(0,16)
        ax2.set_ylabel('Acceleration (%)', fontsize=15)
        ax2.legend().set_visible(False)
        
        # format axis 3 - temperature
        ax3.set_ylim(0,40)
        ax3.set_ylabel('Temperature (%)', fontsize=15)
        ax3.set_xlabel('Time', fontsize=15)
        ax3.legend().set_visible(False)
        
        # get reference to x-axis and format major xtick label
        xaxis = plt.gca().get_xaxis()
        xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    else:
        print 'Initialising live graph...'


#    plotly_fig = tls.mpl_to_plotly(fig)
#    if plotly_fig is not None:
#        print 'Figure is not empty!'
#        plotly.offline.plot_mpl(plotly_fig)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

