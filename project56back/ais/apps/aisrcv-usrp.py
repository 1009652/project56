#!/usr/bin/env python

from gnuradio import gr, audio, uhd, blks2, gru, digital
import ais
import sys,os,math

try:
	frekvens = float(sys.argv[1])*1000000
except Exception:
	frekvens = 162.000e6
	print "Usage: ",sys.argv[0]," <frequency>"
	
try:
	dboard = os.environ['DBOARD']
	if int(dboard) > 1:
		 dboard = 0
except Exception:
	dboard = 0
try:
	antennaport = os.environ['ANTENNA']
except Exception:
	antennaport = "RX2"

fg = gr.top_block()
fg2 = gr.top_block()

u = uhd.usrp_source("",uhd.io_type.COMPLEX_FLOAT32,1)


u.set_samp_rate(64e6/128)
subdev_spec = (int(dboard),0)
subdev = u.get_dboard_iface()
u.set_subdev_spec("A:0")
u.set_antenna(antennaport)
u.set_gain(0)
u.set_center_freq(frekvens-100e3)
sample_rate=64000000/128
decimrate = 2
channel_coeffs = gr.firdes.low_pass (1.0, sample_rate, 10e3, 5e3, gr.firdes.WIN_HAMMING)
move1 = -26.5e3-100e3 
print str(-move1 + frekvens - 100e3)
move2 = 23.5e3-100e3
print str(-move2 + frekvens - 100e3)

selectfrequency  = gr.freq_xlating_fir_filter_ccf (decimrate, channel_coeffs, move1 , sample_rate)
selectfrequency2 = gr.freq_xlating_fir_filter_ccf (decimrate, channel_coeffs, move2 , sample_rate)

k = sample_rate/decimrate/(2*math.pi*5e6)
demod = gr.quadrature_demod_cf(k)
demod2 = gr.quadrature_demod_cf(k)
audio_decim = sample_rate/decimrate/50000 
audio_taps = gr.firdes.low_pass(1.0,sample_rate/decimrate,10000,2000,gr.firdes.WIN_HAMMING)
audio_filter  = gr.fir_filter_fff(audio_decim,audio_taps)
audio_filter2 = gr.fir_filter_fff(audio_decim,audio_taps)




volum = gr.multiply_const_ff(80)
volum2 = gr.multiply_const_ff(80)
lydut = audio.sink(50000,"default")

samplerate = 50000
pluss = gr.add_const_ff(0.0)
lpcoeffs = [   2.5959e-55, 2.9479e-49, 1.4741e-43, 3.2462e-38, 3.1480e-33, 1.3443e-28, 2.5280e-24, 2.0934e-20, 7.6339e-17, 1.2259e-13, 8.6690e-11, 2.6996e-08, 3.7020e-06, 2.2355e-04, 5.9448e-03, 6.9616e-02, 3.5899e-01, 8.1522e-01, 8.1522e-01, 3.5899e-01, 6.9616e-02, 5.9448e-03, 2.2355e-04, 3.7020e-06, 2.6996e-08, 8.6690e-11, 1.2259e-13, 7.6339e-17, 2.0934e-20, 2.5280e-24, 1.3443e-28, 3.1480e-33, 3.2462e-38, 1.4741e-43, 2.9479e-49, 2.5959e-55]

lpfilter1 = gr.fir_filter_fff(1,lpcoeffs)
lpfilter2 = gr.fir_filter_fff(1,lpcoeffs)

forsterk1 = gr.multiply_const_ff(5)
forsterk2 = gr.multiply_const_ff(5)
clockrec1 = digital.clock_recovery_mm_ff(float(samplerate)/9600,0.25*0.175*0.175,0.5,0.175,0.005)
clockrec2 = digital.clock_recovery_mm_ff(float(samplerate)/9600,0.25*0.175*0.175,0.5,0.175,0.005)
msg_queue1 = gr.msg_queue()
msg_queue2 = gr.msg_queue()
slicer1 = digital.binary_slicer_fb()
slicer2 = digital.binary_slicer_fb()
# Parameters: ([mysql-server],[database name],[database user],[database password])
datadec1 = ais.ais_nmea()
datadec2 = ais.ais_nmea()
nullsink1 = gr.null_sink(200)
nullsink2 = gr.null_sink(200)
decoder1 = ais.nmea_decoder("localhost","gnuais","ruben","elgelg")
decoder2 = ais.nmea_decoder("localhost","gnuais","ruben","elgelg")
# You should use the create_mysql.sql to create the necessary tables 
# in the database.
# See create_mysql.txt for help. Those files can be found in the root folder of
# the source tree.
diff1 = gr.diff_decoder_bb(2)
diff2 = gr.diff_decoder_bb(2)

invert1 = ais.invert10_bb()
invert2 = ais.invert10_bb()

fg.connect(u,selectfrequency,demod)
fg.connect(u,selectfrequency2,demod2)
fg.connect(demod,audio_filter,volum)
fg.connect(demod2,audio_filter2,volum2)

fg.connect(volum, lpfilter1,forsterk1,clockrec1,slicer1,diff1,invert1,datadec1,decoder1)
fg.connect(volum2,lpfilter2,forsterk2,clockrec2,slicer2,diff2,invert2,datadec2,decoder2)

#soundout = audio.sink(50000,"default")
#fg.connect(volum,(soundout,0))
#fg.connect(volum2,(soundout,1))

fg.start()
raw_input("AIS Receiver. "+ str(frekvens/1000000)+"MHz.")

#for i in range(0,10):
#	print "From queue: "+msg_queue1.delete_head().to_string()
fg.stop()
print("Receiver A:");
print msg_queue1.count()
for i in range (0,msg_queue1.count()):
	print msg_queue1.delete_head().to_string()
print "Receiver B:";
print msg_queue2.count()
for i in range (0,msg_queue2.count()):
	print msg_queue2.delete_head().to_string()
print "Received correctly A: ",datadec1.received()
print "Wrong CRC: ",datadec1.lost()
print "Wrong Size: ",datadec1.lost2()
print "Received correctly B: ",datadec2.received()
print "Wrong CRC: ",datadec2.lost()
print "Wrong Size: ",datadec2.lost2()
