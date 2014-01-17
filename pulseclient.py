#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import StringIO
import wave

import ctypes
import sys

pa = ctypes.cdll.LoadLibrary('libpulse-simple.so.0')
 
PA_STREAM_PLAYBACK = 1
PA_STREAM_RECORD   = 2
PA_SAMPLE_S16LE    = 3

class struct_pa_sample_spec(ctypes.Structure):
    __slots__ = [
        'format',
        'rate',
        'channels',
    ]
 
struct_pa_sample_spec._fields_ = [
    ('format', ctypes.c_int),
    ('rate', ctypes.c_uint32),
    ('channels', ctypes.c_uint8),
]
pa_sample_spec = struct_pa_sample_spec  # /usr/include/pulse/sample.h:174

class struct_pa_buffer_attr(ctypes.Structure):
    __slots__ = [
        'maxlength',
        'tlength',
        'prebuf',
        'minreq',
        'fragsize',
    ]
struct_pa_buffer_attr._fields_ = [
    ('maxlength', ctypes.c_uint32),
    ('tlength', ctypes.c_uint32),
    ('prebuf', ctypes.c_uint32),
    ('minreq', ctypes.c_uint32),
    ('fragsize', ctypes.c_uint32),
]

pa_buffer_attr = struct_pa_buffer_attr         # /usr/include/pulse/def.h:221

REC_BUF_LEN = 32

class pulserecorder:
    def __init__(self, name):
        self.name = name
        self.buf = ctypes.create_string_buffer(REC_BUF_LEN)

    def start(self):
        ss = struct_pa_sample_spec()
        ss.rate = 48000
        ss.channels = 1
        ss.format = PA_SAMPLE_S16LE

        error = ctypes.c_int(0)

        ba = struct_pa_buffer_attr()
        ba.maxlength = -1
        ba.tlength   = -1 
        ba.prebuf    = -1
        ba.minreq    = -1
        ba.fragsize  = 48000/10 * 2 # 1/10th of a second

        self.s = pa.pa_simple_new(
            None,                # Default server.
            self.name,           # Application's name.
            PA_STREAM_RECORD,    # Stream for recording.
            None,                # Default device.
            'record',            # Stream's description.
            ctypes.byref(ss),    # Sample format.
            None,                # Default channel map.
            ctypes.byref(ba),    # buffering attributes.
            ctypes.byref(error)  # Ignore error code.
        )
        if not self.s:
            raise Exception('Could not create pulse audio stream: {0}!'.format(
                pa.strerror(ctypes.byref(error))))

    def stop(self):
        # Freeing resources and closing connection.
        pa.pa_simple_free(self.s)

    def record(self):
        error = ctypes.c_int(0)

        if pa.pa_simple_read(self.s, self.buf, REC_BUF_LEN, error):
            raise Exception('Pulseaudio: record failed (pa_simple_read)!')

        return (REC_BUF_LEN, self.buf)
        


class pulseplayer:
    def __init__(self, name):
        self.name = name

    def play(self, buf, len):

        ss = struct_pa_sample_spec()
        ss.rate = 48000
        ss.channels = 1
        ss.format = PA_SAMPLE_S16LE

        error = ctypes.c_int(0)
    
        s = pa.pa_simple_new(
            None,                # Default server.
            self.name,           # Application's name.
            PA_STREAM_PLAYBACK,  # Stream for playback.
            None,                # Default device.
            'playback',          # Stream's description.
            ctypes.byref(ss),    # Sample format.
            None,                # Default channel map.
            None,                # Default buffering attributes.
            ctypes.byref(error)  # Ignore error code.
        )
        if not s:
            raise Exception('Could not create pulse audio stream: {0}!'.format(pa.strerror(ctypes.byref(error))))

        if pa.pa_simple_write(s, buf, len, error):
            raise Exception('Could not play file!')
        
        # Waiting for all sent data to finish playing.
        if pa.pa_simple_drain(s, error):
            raise Exception('Could not simple drain!')
        
        # Freeing resources and closing connection.
        pa.pa_simple_free(s)

if __name__ == "__main__":

    #player = pulseplayer("HAL 9000")
    #player.play(the_sound)

    recorder = pulserecorder("HAL 9000")
    recorder.record()

