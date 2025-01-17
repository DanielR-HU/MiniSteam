import tkinter as tk
import random, os

try:
    from tkinter import ttk
except:
    os.system('pip install ttkthemes')
    from tkinter import ttk

try:
    from paho.mqtt import client as mqtt_client
except:
    os.system('pip install paho-mqtt==1.6.1')
    from paho.mqtt import client as mqtt_client


# broker
broker = 'broker.hivemq.com'
port = 1883
topic = "SteamIdSTeam"
client_id = f'publish-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'



# Functie om de GUI te sluiten
def close_app():
    root.destroy()

def SteamMini_Connection():
    steam_id = SteamID_entry.get()
    publish(mqtt_client_instance, steam_id)

def publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Hoofdvenster maken
root = tk.Tk()
root.overrideredirect(True)  # Verwijder de standaard titelbalk
root.geometry("400x300")
root.configure(bg='#C0C0C0')  # Windows 2000 achtergrondkleur

# Aangepaste titelbalk maken
title_bar = tk.Frame(root, bg='#0000FF', relief='raised', bd=2)
title_bar.pack(side='top', fill='x')

# Titel toevoegen aan de aangepaste titelbalk
title_label = tk.Label(title_bar, text="SteamID uploader", bg='#0000FF', fg='white', font=("MS Sans Serif", 12))
title_label.pack(side='left', padx=10)

# Sluitknop toevoegen aan de aangepaste titelbalk
close_button = tk.Button(title_bar, text='X', command=close_app, bg='#FF0000', fg='white', bd=0)
close_button.pack(side='right')

# Functie om venster te verplaatsen
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

title_bar.bind('<B1-Motion>', move_window)

# Frame maken met een rand
frame = tk.Frame(root, bg='#C0C0C0', bd=2, relief='solid')
frame.pack(padx=10, pady=10, fill='both', expand=True)

# Label toevoegen
label = tk.Label(frame, text="Vul de nieuwe Steam ID in:", bg='#C0C0C0', fg='black', font=("MS Sans Serif", 12))
label.pack(pady=10)

# Invoerveld toevoegen
SteamID_entry = tk.Entry(frame, width=30, font=("MS Sans Serif", 12))
SteamID_entry.pack(pady=10)


# Knop toevoegen
button = tk.Button(frame, text="Upload", font=("MS Sans Serif", 12), command=SteamMini_Connection, bg='#E0E0E0', fg='black', width=15)
button.pack(pady=10)

# Uitleg
Uitleg = tk.Label(frame, text="Op de Mini Steam device ga naar Kolom 3 Rij 3, Connect. Wacht tot het schermpje MQTT Data Check laat zien en stuur dan de nieuwe steam ID met de login button.", bg='#C0C0C0', fg='black', font=("MS Sans Serif", 12), wraplength=300)
Uitleg.pack(pady=10)

mqtt_client_instance = connect_mqtt()
mqtt_client_instance.loop_start()

# Hoofdloop starten
root.mainloop()