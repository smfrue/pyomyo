# PyoMyo with Touch Designer
Streaming Data to Tocuh Designer from Python module for the Thalmic Labs Myo armband. 

Cross platform and multithreaded and works without the Myo SDK. 

![Toggle data stream in Touch Designer](https://github.com/smfrue/pyomyo/blob/main/media/getEMGdataViaUDP_toggle?raw=true "Touch Designer")

Checkout the [main repo from PerlinWarp](https://github.com/PerlinWarp/pyomyo) for full instructions and current tutorials on how to use pyomyo. 

How to send EMG data via UDP to TouchDesigner:

1. Switch to the examples directory from pyomyo and run: 
```
python3 myo_multithreading_examp.py
```
2. Add "td-examples/getEMGdataViaUDP.tox" to your TD Scene
3. Go into base1 and switch toggle to activate/deactive data stream
4. Trail CHOP should visualize received data as a plot

## What I changed:
(I just explain the most important parts)

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

### udppin1
<b>Tab Connect:</b>
Port: 7000
Row/Callback Format: One per Message
Local Address: 127.0.0.1

<b>Tab Received Data:</b>
Maximum Lines: 1
Clamp Output: ON


### udppin1_callbacks
```
#onReceive split each value by comma and put it in seperate cells of table1
if rowIndex == 2:
	value = message.split(',')
	op('table1')[0,0] = value[0]
	op('table1')[0,1] = value[1]
	op('table1')[0,2] = value[2]
	op('table1')[0,3] = value[3]
	op('table1')[0,4] = value[4]
	op('table1')[0,5] = value[5]
	op('table1')[0,6] = value[6]
	op('table1')[0,7] = value[7]
	print(dat, rowIndex, message)
```
