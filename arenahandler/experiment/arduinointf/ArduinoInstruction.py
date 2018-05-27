""" 
This module is going to be used as an Interface bewtween the Arduino and
the top layer application which is in charge of manage the LED strip.
The serial module is used to make the serial connection and the sleep
from the time module to enhace it.
"""
import serial
from time import sleep


class ArduinoInstruction:
    """ 
    This class abstracts the communication between the application and
    the Arduino. The communication is done via the serial port where
    the Arduino is connected, also the baud rate has to be setted.
    By default there is a timeout, to finish the communication if there
    is any problem and wait time that allows to wait until the 
    connection is ready.
    """
    TIMEOUT = 5
    START_WAIT_TIME = 2
    MESSAGE_WAIT_TIME = 0.0625

    def __init__(self, port, baud):
        """ 
        This is where the port and baud rate are setted.
        ----------
        port : string
            The serial port where the Arduino is connected.
        baud : int
            The baud rate used to transmi information.
        Returns
        -------
        new ArduinoInstruction Object
        """
        self.port = port
        self.baud = baud

    def start_connection(self):
        """Starts the serial connection with the Arduino."""
        try:
            self.arduino = serial.Serial(
                self.port, self.baud, timeout=self.TIMEOUT
            )
            sleep(self.START_WAIT_TIME)  # This is important
            print("Connection started: %s, rate: %s" % (self.port, self.baud))
        except Exception as e:
            print(e)

    def send_instrunction(self, instruction):
        """ This sends the instruction to the Arduino. """

        self.arduino.write(instruction.encode())
        sleep(self.MESSAGE_WAIT_TIME)
        response = ''
        while self.arduino.in_waiting:
            response += self.arduino.readline().decode()
        return response

    def close_connection(self):
        """ This closes the serial connection."""
        self.arduino.close()


if __name__ == "__main__":
    # Test to check if it works.
    inst = ArduinoInstruction('COM4', 57600)
    inst.start_connection()
    for i in range(0, 3):
        res = inst.send_instrunction("""
        {
            "block":""" + '"' + str(i) + """,2,0,0,255",
            "brightness": 25,
            "led": []
        }
        """)
        print("From Arduino: %s" % (res))
    inst.close_connection()
