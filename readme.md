# MQTTunneler

#### MQTTunneler helps you by creating a MQTT Tunnel for the transmission of data coming from UDP ~~(and/or OSC (maybe in the future))~~ to connect you and your non-mqtt-supported device/software with the world through the internet.

It truly helps in connecting deprecated/restricted technology to more modern ones, achieving it's goals in having a better IoT integration.
<br>

### Pre-requisites
The program requires Python3 and the module [Paho-mqtt](https://pypi.org/project/paho-mqtt/). You can install it by using:

```
pip3 install paho-mqtt
```

##### Origin
This software was developed by me (João Vitor Coelho) in Dec/2020 for the [**NANO - Núcleo de Arte e Novos Organismos**](https://nano.eba.ufrj.br), in the [**Escola de Belas Artes**](https://eba.ufrj.br/), at [**UFRJ - Universidade Federal do Rio de Janeiro**](https://ufrj.br/en), Brazil.

<br>

##### How it Works
MQTTunneler creates (and maintains it, while it's running) a local UDP connection at your network, which will be used internally to send and receive data.
- You must point your device/software to your proper localhost IP ADDRESS and PORT (which are two separated ones: Receiving and Sending PORTs) and send your data via UDP connection. With that set, the program will do rest in translating that to your MQTT broker.
- Receiveing data follows the same structure: data coming from the specific topic on your MQTT broker will be served on your local network, at the selected port (40301, by default, but it's customizable).

<br>

#### Credits
Developed by:  [João V. Coelho](https://github.com/joaovcoelho/MQTTunneler/)
