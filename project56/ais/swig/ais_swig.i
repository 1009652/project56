/* -*- c++ -*- */

#define AIS_API

%include "gnuradio.i"			// the common stuff
%include "config.h"

//load generated python docstrings
%include "ais_swig_doc.i"


%{
#include "ais_invert10_bb.h"
#include "ais_nmea_decoder.h"
#include "ais_ais_nmea.h"
%}


GR_SWIG_BLOCK_MAGIC(ais,invert10_bb);
%include "ais_invert10_bb.h"

GR_SWIG_BLOCK_MAGIC(ais,nmea_decoder);
%include "ais_nmea_decoder.h"

GR_SWIG_BLOCK_MAGIC(ais,ais_nmea);
%include "ais_ais_nmea.h"
