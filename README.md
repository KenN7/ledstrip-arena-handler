# Dynamic lighting arena for swarm robotics

This project was developed as a handler of dynamic lighting polygonal arena 
which is compounded of blocks of leds built with the APA102 LED strip connected 
to an Arduino. The project consists in :

1. The Arduino firmware
2. An inteferface between the handler and the arduino
3. The arena handler 

## Getting Started

### Folder structure
```
├── firmwarearduino
│   ├── ledstriphandler.ino
├── arenahandler
│   ├── config
│   │   ├── config.json
│   ├── logs
│   │   ├── apiserver.log
│   │   ├── arduinocomm.log
│   │   ├── experimentctrl.log
│   ├── experiment
│   │   ├── arduinointf
│   │   │   │   ├── ArduinoInstruction.py
│   │   ├── component
│   │   │   │   ├── Arena.py
│   │   │   │   ├── Block.py
│   │   │   │   ├── BlockInstruction.py
│   │   │   │   ├── Color.py
│   │   │   │   ├── Edge.py
│   │   │   │   ├── Experiment.py
│   │   │   │   ├── Led.py
│   │   │   │   ├── State.py
│   │   ├── utils
│   │   │   │   ├── logger.py
│   │   │   │   ├── readconfig.py
│   │   ├── experimentctrl.py
│   ├── apiserver.py
├── README.md
```

### Prerequisites

- Python 3.6.4

#### Arduino libraries
- FastLED 3.1.6
- ArduinoJson 5.13.1

#### Python libraries

- aiohttp 3.2.1
- pyserial 3.4


### Installing

Python libraries intallation

aiohttp

```bash
pip install aiohttp
```

pyserial

```bash
pip install pyserial
```

## Deployment

The base command is:

```bash
api_server.py [--port] [--host]
```
`host` means the host where you want to bind the web server  
`port` means the port where you want to bind the web server  

Go to the `arenahandler` directory and execute the following command:

### Linux
```bash
./api_server.py --port=8080 --host=localhost
```
### Windows
```bash
python api_server.py --port=8080 --host=localhost
```
`note`: By default the host and port are `0.0.0.0`, `8080` respectively, however
 it is possible to change it using
the port and host argument at the time of execute the command.

## Built With

* [Anaconda](https://www.anaconda.com/download/) - The web framework used
* [Visual Studio Code](https://code.visualstudio.com/) - Dependency Management
* [Arduino IDE](https://www.arduino.cc/en/Main/Software?) - Upload firmware to Arduino

## How to use

This application essentially starts a HTTP API in which your are able to make
two type of requests: `execute a state` that will change the color of the arena
and `execute an experiment` that consists in a group of states and its time during
the experiment. So there are two services that can be consumed one for `state`
and one for `experiment` which are going to be described below.

### State

The url to execute the change of state is the following:

|              |                                                    |
|--------------|----------------------------------------------------|
| Name         | Execute State                                      |
| URL          | http://localhost:8080/arena-handler/api/v1.0/state |
| Method       | POST                                               |
| Content type | application/json                                   |
| Response     | application/json                                   |

#### Colored the arena

```json
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "red",
        "brightness": 5
    }
}
```
### Experiment

The url to execute the change of state is the following:

|              |                                                        |
|--------------|----------------------------------------------------    |
| Name         | Execute State                                          |
| URL          | http://localhost:8080/arena-handler/api/v1.0/experiment|
| Method       | POST                                                   |
| Content type | application/json                                       |
| Response     | application/json                                       |

## Authors

* **Keneth Ubeda**