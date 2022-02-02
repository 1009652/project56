#!/usr/bin/env python

from gnuradio import gr, audio, blks2, gru, digital
import ais
import sys,os,math


fg = gr.top_block()

sample_rate = 50000
decimrate = 1
src = audio.source(sample_rate, "default")

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

fg.connect((src,0),audio_filter)
fg.connect((src,1),audio_filter2)
fg.connect(audio_filter,volum)
fg.connect(audio_filter2,volum2)

fg.connect(volum, lpfilter1,forsterk1,clockrec1,slicer1,diff1,invert1,datadec1,decoder1)
fg.connect(volum2,lpfilter2,forsterk2,clockrec2,slicer2,diff2,invert2,datadec2,decoder2)

#soundout = audio.sink(50000,"default")
#fg.connect(volum,(soundout,0))
#fg.connect(volum2,(soundout,1))

fg.start()
raw_input("AIS Receiver. (From audio input)")

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
