/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */
#ifndef INCLUDED_AIS_nmea_decoder_H
#define INCLUDED_AIS_nmea_decoder_H

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ais_api.h>
#include <gr_sync_block.h>
#ifdef HAVE_MYSQL
#include <mysql/mysql.h>
#endif
#include <cstdio>
#include <iomanip>

class ais_nmea_decoder;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<ais_nmea_decoder> ais_nmea_decoder_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of ais_nmea_decoder.
 *
 * To avoid accidental use of raw pointers, ais_nmea_decoder's
 * constructor is private.  ais_make_nmea_decoder is the public
 * interface for creating new instances.
 */
AIS_API ais_nmea_decoder_sptr ais_make_nmea_decoder (const char *host,const char *database, const char *user, const char *password);

/*!
 * \brief square2 a stream of floats.
 * \ingroup block
 *
 * This uses the preferred technique: subclassing gr_sync_block.
 */
class AIS_API ais_nmea_decoder : public gr_block
{
private:
  // The friend declaration allows ais_make_nmea_decoder to
  // access the private constructor.
	void bokstavtabell(char,char *, int);
	void get_data(int );
	unsigned long henten(int from, int size, unsigned char *frame);
	unsigned char d_rbuffer[450];
	char *d_tbuffer;
#ifdef HAVE_MYSQL
	MYSQL d_conn;
#endif
	void nmea_decode(char *nmea);

  friend AIS_API ais_nmea_decoder_sptr ais_make_nmea_decoder (const char *host,const char *database, const char *user, const char *password);

  ais_nmea_decoder (const char *host,const char *database, const char *user, const char *password);  	// private constructor

 public:
  ~ais_nmea_decoder ();	// public destructor

  // Where all the action really happens

  int general_work (int noutput_items,
		gr_vector_int &ninput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_AIS_nmea_decoder_H */
