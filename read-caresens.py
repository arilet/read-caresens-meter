import serial
import codecs
import datetime

def parse(buffer):
	year = 2000 + ((buffer[1] & 0xf) << 4) + (buffer[2] & 0xf)
	month = ((buffer[4] & 0xf) << 4) + (buffer[5] & 0xf)
	day = ((buffer[7] & 0xf) << 4) + (buffer[8] & 0xf)
	hour = ((buffer[10] & 0xf) << 4) + (buffer[11] & 0xf)
	minute = ((buffer[13] & 0xf) << 4) + (buffer[14] & 0xf)
	second = ((buffer[16] & 0xf) << 4) + (buffer[17] & 0xf)
	mgdl = (((buffer[19] & 0xf) << 4) + (buffer[20] & 0xf) + ((buffer[23] & 0xf) << 8))
	#mmol = (((buffer[19] & 0xf) << 4) + (buffer[20] & 0xf)) * 0.0555

	d = datetime.datetime(year, month, day, hour, minute, second)
	#sample = '{:%d.%m.%Y;%H:%M;;}'.format(d) + str(round(mmol, 1)).replace('.',',') + ";;;;;;;"
	#sample = '{:%d.%m.%Y;%H:%M;;}'.format(d) + str(mgdl) + ";;;;;;;"
	sample = '{:%d.%m.%Y,%H:%M,}'.format(d) + "Glucose," + str(mgdl) + ",mg/dL"
	#print(sample)
	return sample

file = open('output.txt', 'w')
#file.write('DAY;TIME;KETONE;BG_LEVEL;CH_BE_KHE;BOLUS;BASAL;BLOODPRESSURE;Weight;Exercise;REMARK' + '\n')
file.write('Date,Time,Type,Value,Label' + '\n')
	
ser = serial.Serial('COM4', 9600, timeout=1)

ser.write(b"\x80")
buffer = ser.read(3)
print(codecs.encode(buffer, 'hex'))

for i in range(65,564):
	command = bytes([0x8B])
	command = command + bytes([0x1e + ((i & 0x0200) >> 9)])		# 1 bit
	command = command + bytes([0x20 + ((i & 0x01e0) >> 5)])		# 4 bits
	command = command + bytes([0x10 + ((i & 0x001e) >> 1)])		# 4 bits
	command = command + bytes([0x20 + ((i & 0x0001) << 3)])		# 1 bit
	command = command + bytes([0x10, 0x28])
	print(codecs.encode(command, 'hex'))
	
	ser.write(command)
	buffer = ser.read(24)
	print(codecs.encode(buffer, 'hex'))
	file.write(parse(buffer) + '\n')
	
#ser.write(b"\x8B\x1E\x22\x10\x28\x10\x28")
#buffer = ser.read(24)
#print(codecs.encode(buffer, 'hex'))

#parse(buffer)

ser.close()
