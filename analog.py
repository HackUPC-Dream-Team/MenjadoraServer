from pyfirmata import Arduino, util
import time

board = Arduino('/dev/ttyACM0')

it = util.Iterator(board)
it.start()

board.analog[5].enable_reporting()

input = '1'

while input != 'q':
    total = 0
    for i in range(3):
        read_1 = board.analog[5].read()
        
        if(read_1 == None):
            print "pin1: None"
        else:
            total = total + read_1
            print "pin1: " + str(read_1)

        time.sleep(0.5)
    print "Mitjana: " + str(total/3)
    input = raw_input("Next reading")
