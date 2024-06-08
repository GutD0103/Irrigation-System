import serial.tools.list_ports
import time

class RS485Communication:
    def get_port(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = "None"
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            if "USB Serial Device" in strPort:
                splitPort = strPort.split(" ")
                commPort = (splitPort[0])
                
        return commPort

    def __init__(self, baudrate=115200, timeout=1):
        self.mess = ""
        self.processData = None
        self.port = self.get_port()
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = serial.Serial(self.port, self.baudrate)
        print(self.serial_connection)

    def open_serial_connection(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"Serial connection opened on {self.port}")
        except serial.SerialException as e:
            print(f"Error: Unable to open serial connection on {self.port}. {e}")

    def close_serial_connection(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Serial connection closed on {self.port}")

    def process_data(self, data):
        # Add your data processing logic here
        if(self.processData == None):
            print(f"NO func to Processing data: {data}")
        else:
            self.processData(data)
        

    def read_serial(self):
        bytesToRead = self.serial_connection.inWaiting()
        if (bytesToRead > 0):
            self.mess = self.mess + self.serial_connection.read(bytesToRead).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                print(self.mess[start:end + 1])
                self.process_data(self.mess[start:end + 1])
                if (end == len(self.mess)):
                    self.mess = ""
                else:
                    self.mess = self.mess[end + 1:]
                    
    def send_data(self,data):
        # print(data)
        self.serial_connection.write((data))

if __name__ == "__main__":
    pass
    # Replace 'COM1' with your actual serial port
    # uart = UARTCommunication(baudrate=115200, timeout=1)
    # print(uart.get_port())
    # while True:
    #     try:
    #         uart.read_serial()
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         break
