# Irrigation System

## Introduction

Welcome to our Irrigation System repository! This system is designed to automate watering schedules for various applications such as gardening, agriculture, and landscaping. The system allows you to customize settings to suit your specific needs, ensuring efficient water usage and optimal plant growth.

## Features

- Automated watering schedules based on predefined settings.
- Customizable settings for baud rate and other parameters.
- Integration with RS485 communication for reliable data transmission.
- Expandable and adaptable for different irrigation setups.

## Installation

To install and run the Irrigation System, follow these steps:

1. Clone this repository to your local machine.
2. Install any required dependencies.
3. Modify the settings in `main.py` and `rs485.py` to match your system specifications.
4. Run the system by executing `python main.py` in your terminal.

## Usage

Once the system is running, it will automatically execute the watering schedule based on the configured settings. Monitor the system output for any status updates.

## Settings

To customize the behavior of your irrigation system, adjust the following settings:

### Baud Rate

Ensure optimal communication performance by setting the baud rate parameter in the RS485 communication settings. Open the `main.py` file and locate the initialization of the RS485 communication. Modify the baud rate value as necessary:

```python
rs485 = RS485Communication(baudrate=9600, timeout=1)
```

### Port Configuration

To specify the port for RS485 communication, navigate to the `rs485.py` file and locate the `get_port()` method. Update the return value to specify the desired port:

```python
def get_port(self):
    # Retrieve available ports
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    
    # Iterate through the available ports
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        
        # Check if the port matches the desired criteria
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    
    # Return the updated port information
    return "/dev/ttyUSB1"  # Change this line to specify the desired port. This is example
```
