import multiprocessing
from pyomyo import Myo, emg_mode
import os
import socket

upd_ip          = "127.0.0.1"
udp_port        = 7000
sock            = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def cls():
    # Clear the screen in a cross platform way
    # https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
    os.system('cls' if os.name=='nt' else 'clear')


def msg_to_bytes(msg):
    return msg.encode('utf-8')
    
# ------------ Myo Setup ---------------
q = multiprocessing.Queue()



def worker(q):
    m = Myo(mode=emg_mode.FILTERED)
    m.connect()
    
    def add_to_queue_emg(emg, movement):
        q.put(emg)
        

    m.add_emg_handler(add_to_queue_emg)
    
    def add_to_queue_imu(quat, acc, gyro):
        imu_data = [quat, acc, gyro]
        q.put(imu_data)
    
    m.add_imu_handler(add_to_queue_imu)
    
    def print_battery(bat):
        print("Battery level:", bat)

    m.add_battery_handler(print_battery)

     # Orange logo and bar LEDs
    m.set_leds([128, 0, 0], [128, 0, 0])
    # Vibrate to know we connected okay
    m.vibrate(1)
    
    """worker function"""
    while True:
        m.run()
    print("Worker Stopped")

# -------- Main Program Loop -----------
if __name__ == "__main__":
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()

    try:
        while True:
            while not(q.empty()):
                emg_imu = list(q.get())
                
                #convert each int of list to string
                string_ints = [str(int) for int in emg_imu]
                
                #add strings back to one line seperated by comma
                str_of_ints = ",". join(string_ints)
                
                print(msg_to_bytes(str_of_ints))
                
                #send encoded string as bytes to udp ip + port
                sock.sendto(msg_to_bytes(str_of_ints), (upd_ip, udp_port))

                #cls()

    except KeyboardInterrupt:
        print("Quitting")
        quit()
