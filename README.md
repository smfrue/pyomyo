# How to use PyoMyo in Touch Designer
Streaming Data to Touch Designer from Python module for the Thalmic Labs Myo armband. 

Cross platform and multithreaded and works without the Myo SDK. 

![Toggle data stream in Touch Designer](https://github.com/smfrue/pyomyo/blob/main/media/getEMGdataViaUDP_toggle.gif?raw=true "Touch Designer")

Checkout the [main repo from PerlinWarp](https://github.com/PerlinWarp/pyomyo) for full instructions and current tutorials on how to use pyomyo. 

### How to:

1. Switch to the examples directory from pyomyo and run: 
```
python3 myo_multithreading_examp.py
```
2. Drag and drop td-examples/getEMGdataViaUDP.tox to your TD Scene
3. Go into base1 and switch EMG toggle to activate/deactive data stream
4. Trail CHOP should visualize received data as a plot

## What I changed
I just show the important parts. Open getEMGdataViaUDP.tox and myo_multithreading_examp.py to see the full setup.

### myo_multithreading_examp.py
```
import socket

upd_ip          = "127.0.0.1"
udp_port        = 7000
sock            = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def msg_to_bytes(msg):
    return msg.encode('utf-8')
```
```
try:
	while True:
		while not(q.empty()):
			emg = list(q.get())
			#print(emg)
			
			#convert each int of list to string
			string_ints = [str(int) for int in emg]
			
			#add strings back to one line seperated by comma
			str_of_ints = ",". join(string_ints)
			print(msg_to_bytes(str_of_ints))
			
			#send encoded string as bytes to udp ip + port
			sock.sendto(msg_to_bytes(str_of_ints), (upd_ip, udp_port))
```

### getEMGdataViaUDP.tox DAT UDP in TouchDesigner
![td_udp1_connect](https://github.com/smfrue/pyomyo/blob/main/media/td_udp1_connect.png?raw=true "Touch Designer td_udp1_connect")
![td_udp1_received_data](https://github.com/smfrue/pyomyo/blob/main/media/td_udp1_received_data.png?raw=true "Touch Designer td_udp1_received_data")
![td_udp1_callbacks](https://github.com/smfrue/pyomyo/blob/main/media/td_udp1_callbacks.png?raw=true "Touch Designer udp1_callbacks")

