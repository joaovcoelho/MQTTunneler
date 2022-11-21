import random
import socket
from paho.mqtt.client import Client
from time import sleep

# MQTT SETTINGS ====
# Declaring credentials and address
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
unique = ''
for i in range(7):  # Creates a unique suffix
    unique += random.choices(chars)[0]

clientid = "MQTTunneler-" + unique  # Type your name at the first string

# SPLASH HEADER ====
print("-=" * 8, "MQTTunneler", "=-" * 8)
print("\n  | Version:  1.2  | Released on:  04/2022")
print("\n  | Launched on:  12/2020")
print("\n  | Dev. by:  João V. Coelho")
print("  | Contact:  j.v.coelho.v@poli.ufrj.br")
print("\n  | NANO - Núcleo de Arte e Novos Organismos | EBA - Escola de Belas Artes")
print("  | UFRJ - UNIVERSIDADE FEDERAL DO RIO DE JANEIRO\n")
print("-=-" * 15)

sleep(2.75)  # Shows the Splash Header for 2.75 seconds
print("\n\n")  # Line breaker to start the visualization

print(f'      Your ClientId will be:  {clientid} \n')

print("#=" * 5, 'MQTTunneler - IP Address and Port (BROKER)', "=#" * 5, '\n')
# MQTT broker - Setting IP and PORT
mqttIP = input((" "*5) + "Insert MQTT-Server's IP Address (example: 177.77.7.77): \n" +
               (" "*8) + "| IP Address => ")  # MQTT server's ip
mqttPORT = int(input((" "*5) + "Insert MQTT-Server's PORT:  \n" +
               (" "*8) + "| PORT => "))

# MQTT broker - Setting Credentials
credentials = input("\n" + (" "*5) + "Would you like to set the MQTT-Broker's Credentials (USER and PASSWORD)?" +
                    "\n" + (" "*8) + "| [Y/N] => ")
if credentials.lower() == 'y':
    mqttUSER = input((" " * 12) + 'User:  ')
    mqttPASS = input((" " * 12) + 'Password: ')

elif credentials.lower() != 'y':
    mqttUSER = None
    mqttPASS = None

# UDP SETTINGS ====
print('\n', "#=" * 5, 'MQTTunneler - Local Connection Settings', "=#" * 5)
bind_ip = 'localhost'

# Checks if the user wants to use custom ports
customPorts = input('\n' + (" "*5) + 'Would you like to use CUSTOM local ports for your program\n' +
                           (" "*5) + 'to send/receive data from this server? The default are as below:\n' +
                           (" "*8) + '[ sending: "40302" | receiving: "40301" ]\n' +
                           (" "*10) + '| Change? [Y/N] => ')
if customPorts.lower() == 'y':
    # Port to RECEIVE from
    bind_input_port = ''
    try:
        print('\n' + (" "*10) + 'Type port below for your program to RECEIVE data from the server.\n' +
                     (" "*10) + '(recommended: 40301)')
        bind_input_port = int(input((" "*14) + '| Insert the port to RECEIVE from:  '))
    except:
        type(bind_input_port) == int  # Can't remember the reason, but the program runs, so I won't change it yet
    if not isinstance(bind_input_port, int):
        print("\n" + (" "*12) + "[Type only  N U M B E R S!]\n")
        bind_input_port = int(input((" "*14) + '| Insert the port to RECEIVE from:  '))

    # Port to SEND to
    bind_output_port = ''
    try:
        print('\n' + (" "*10) + 'Type port below for your program to SEND data to the server.\n' +
                     (" "*10) + '(recommended: 40302)')
        bind_output_port = int(input((" "*14) + '| Insert the port to SEND to:  '))
    except:
        type(bind_output_port) == int  # Can't remember the reason, but the program runs, so I won't change it yet
    if not isinstance(bind_output_port, int):
        print("\n      [Type only  N U M B E R S!]\n")
        bind_output_port = int(input((" "*14) + '| Insert the port to SEND to:  '))

else:
    # Default ports
    bind_input_port = 40301
    bind_output_port = 40302

# SETS TOPIC to RECEIVE from
print('\n', "#=" * 5, 'MQTTunneler - Publish/Subscribe Settings', "=#" * 5)
print('\n' + (" "*5) + 'Type the TOPIC you want to RECEIVE data from')
mqttSub = input((" "*8) + "| Insert the Topic to RECEIVE from:  ")  # Type the topic to send and receive from

# SETS TOPIC to SEND to
print('\n' + (" "*5) + 'Type the TOPIC you want to SEND data to')
mqttPub = input((" "*8) + "| Insert the Topic to SEND to:  ")  # Type the topic to send and receive from


def function_not_being_used():  # only storages this piece of code for future use
    # ERROR: Currently getting only self ClientID
    """# SETS CLIENT_ID
    print('\nType a nickname. (e.g. joao-v-coelho)')
    clientid = input("\n    | Insert a nickname:  ")  # Type the topic to send and receive from
    clientid = clientid + '00' + unique  # Makes it unique
    print(f'Your ClientId is: "{clientid}". (The ending is to keep it unique!)\n')"""
    pass


codification = "ascii"  # Codification to be used on INPUT_DESTINATION for encoding/decoding

print("=" * 10, 'MQTTunneler - START', "=" * 10, '\n')

output_destination = (bind_ip, bind_output_port)  # From here to the world
input_destination = (bind_ip, bind_input_port)  # From the world to here

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPV4 connection, UDP - SERVER
client_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # CLIENT

server.bind(output_destination)
server.settimeout(1)

start_msg = "Initial data"  # By now, it's probably unuseful
msg = start_msg

# MQTT SERVER AND CLIENT ====
print(f'Listening to  "{bind_ip}"  on port  "{bind_input_port}" - To RECEIVE')
print(f'Listening to  "{bind_ip}"  on port  "{bind_output_port}" - To SEND')


def on_connect(client, userdata, flags, rc):
    # Presents session's first state and subscribes to topics
    '''print(f"Connected {client._client_id}")
    print(f"Connection result code: [{rc}]")'''
    client.subscribe(topic=mqttSub, qos=2)  # Subscribes to the topic


def on_message(client, userdata, message):
    # Continuously listens to show received data
    message.payload = message.payload.decode("utf-8")  # Decodes the received binary to Unicode UTF-8

    from_user = client._client_id.decode()  # Gets the Client_id from the sender
    client_mqtt_handler(message.topic, message.payload,
                        from_user)  # Calls the function that sends the incoming data to de local address

    # below is for debugging the data
    '''print("=" * 15, '\nRECEIVED - MQTT')
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload}")
    print(f"QoS: {message.qos}")'''


def on_publish(client, userdata, data):
    # Initializes connection and keeps it alive
    return ()


client_MQTT = Client(client_id=clientid, clean_session=False)  # Calls the class from the module


def mqtt_main():
    # Initializes and maintains the MQTT connection

    client_MQTT.on_connect = on_connect  # Instantiates the connection function
    client_MQTT.on_message = on_message  # Instantiates the data receiving function
    client_MQTT.on_publish = on_publish  # Instantiates the data sending function

    client_MQTT.username_pw_set(mqttUSER, mqttPASS)  # Inserts credentials for connection

    client_MQTT.connect_async(host=mqttIP, port=mqttPORT)  # Initiates the asynchronous connection
    client_MQTT.loop_start()  # Starts it


# UDP SERVER AND CLIENT ====
def server_handler():
    # It RECEIVES data from the local address and  SENDS to the MQTT server
    try:
        received, cliente = server.recvfrom(1024)
    except:
        received = None
    if received is not None:
        received = received.decode()
        client_MQTT.publish(mqttPub, received, qos=2)

        client_MQTT.publish("MQTTunneler", received.encode(codification, errors="replace"))  # DEBUGGING CODIFICATION

        print('))' + '==>' * 5, '\nSENT to MQTT', f'\nClientID: {cliente[1]}')
        print(f'Data: {received}', '\n))' + '==>' * 5, '\n')


def client_mqtt_handler(topic, data, user):
    # It RECEIVES data from the MQTT Server and  SENDS to the local address
    data = data.encode(codification, errors="replace")
    client_UDP.sendto(data, input_destination)
    print('\n', "<==" * 5 + '((', '\nRECEIVED from MQTT')
    print(f"Topic: {topic}")
    print(f'Data: {data.decode(codification, errors="replace")}', '\n', '<==' * 5 + '((\n')


# print(f"From: {user}", '\n', '<==' * 5 + '((')  # Suppressed, since doesn't properly work yet


# Starts and Maintains both Local UDP and external MQTT servers
while True:
    server_handler()  # UDP server  # Maybe it'll be replaced by threading
    mqtt_main()  # MQTT server x client

server_handler.close()
client_UDP.close()
client_MQTT.loop_stop()
