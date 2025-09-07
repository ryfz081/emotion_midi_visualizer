import rtmidi
def main():
    midiin = rtmidi.MidiIn()
    ports = range(midiin.get_port_count())
    if ports:
        for i in ports:
            print(midiin.get_port_name(i))
        print("Opening port 0!") 
        midiin.open_port(0)
        while True:
            m = midiin.get_message()
            if m:
                print(m)
    #             # print(m)
    #             if is_Note(m):
    #                 if is_On(m):
    #                     print("Note On @", m[0][1], " with Velocity of", m[0][2])
    #                 print("Note Off @", m[0][1])
    #             # else:

    #                 # if is_On(m):
    #                 #     print("Pedal On")
    #                 # print("Pedal Off")

    # else:
    #     print('NO MIDI INPUT PORTS!')
def is_Note(message):
    return message[0][0] == 144

def is_On(message):
    return message[0][2] != 0

main()
