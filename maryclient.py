#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import httplib, urllib

import StringIO
import wave

import ctypes
import wave
import sys

#
# A simple MARY TTS client in Python, using pulseaudio for playback
#
# based on Code from Hugh Sasse (maryclient-http.py)
#
# 2013 by G. Bartsch. License: LGPLv3

class maryclient:

    def __init__(self):

        self.host = "127.0.0.1"
        self.port = 59125
        self.input_type = "TEXT"
        self.output_type = "AUDIO"
        self.audio = "WAVE_FILE"
        self.locale = "en_US"
        self.voice = "cmu-bdl-hsmm"

    def set_host(self, a_host):
        """Set the host for the TTS server."""
        self.host = a_host

    def get_host(self):
        """Get the host for the TTS server."""
        self.host

    def set_port(self, a_port):
        """Set the port for the TTS server."""
        self.port = a_port

    def get_port(self):
        """Get the port for the TTS server."""
        self.port

    def set_input_type(self, type):
        """Set the type of input being 
           supplied to the TTS server
           (such as 'TEXT')."""
        self.input_type = type

    def get_input_type(self):
        """Get the type of input being 
           supplied to the TTS server
           (such as 'TEXT')."""
        self.input_type

    def set_output_type(self, type):
        """Set the type of input being 
           supplied to the TTS server
           (such as 'AUDIO')."""
        self.output_type = type

    def get_output_type(self):
        """Get the type of input being 
           supplied to the TTS server
           (such as "AUDIO")."""
        self.output_type

    def set_locale(self, a_locale):
        """Set the locale
           (such as "en_US")."""
        self.locale = a_locale

    def get_locale(self):
        """Get the locale
           (such as "en_US")."""
        self.locale

    def set_audio(self, audio_type):
        """Set the audio type for playback
           (such as "WAVE_FILE")."""
        self.audio = audio_type

    def get_audio(self):
        """Get the audio type for playback
           (such as "WAVE_FILE")."""
        self.audio

    def set_voice(self, a_voice):
        """Set the voice to speak with
           (such as "dfki-prudence-hsmm")."""
        self.voice = a_voice

    def get_voice(self):
        """Get the voice to speak with
           (such as "dfki-prudence-hsmm")."""
        self.voice

    def generate(self, message):
        """Given a message in message,
           return a response in the appropriate
           format."""
        raw_params = {"INPUT_TEXT": message.encode('UTF8'),
                "INPUT_TYPE": self.input_type,
                "OUTPUT_TYPE": self.output_type,
                "LOCALE": self.locale,
                "AUDIO": self.audio,
                "VOICE": self.voice,
                }
        params = urllib.urlencode(raw_params)
        headers = {}

        # Open connection to self.host, self.port.
        conn = httplib.HTTPConnection(self.host, self.port)

        #conn.set_debuglevel(5)
        
        conn.request("POST", "/process", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            print response.getheaders()
            raise RuntimeError("{0}: {1}".format(response.status,
                response.reason))
        return response.read()

#
# pulseaudio / playback stuff
#

pa = ctypes.cdll.LoadLibrary('libpulse-simple.so.0')
 
PA_STREAM_PLAYBACK = 1
PA_SAMPLE_S16LE = 3
BUFFSIZE = 1024

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

class pulseplayer:
        def __init__(self, name):
                self.name = name

        def play(self, a_sound):

            buf = StringIO.StringIO(a_sound)
                
            wf = wave.open(buf, 'rb')

            ss = struct_pa_sample_spec()
            ss.rate = wf.getframerate()
            ss.channels = wf.getnchannels()
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
                raise Exception('Could not create pulse audio stream: {0}!'.format(
                    pa.strerror(ctypes.byref(error))))

            while True:
                #latency = pa.pa_simple_get_latency(s, error)
                #if latency == -1:
                #    raise Exception('Getting latency failed!')
            
                #print('{0} usec'.format(latency))
            
                # Reading frames and writing to the stream.
                buf = wf.readframes(BUFFSIZE)
                if buf == '':
                    break

                #print "len: %d" % len(buf)
            
                if pa.pa_simple_write(s, buf, len(buf), error):
                    raise Exception('Could not play file!')
            
            wf.close()
           
            #print "drain..."
 
            # Waiting for all sent data to finish playing.
            #if pa.pa_simple_drain(s, error):
            #    raise Exception('Could not simple drain!')
            
            #print "free..."

            # Freeing resources and closing connection.
            pa.pa_simple_free(s)

if __name__ == "__main__":

    client = maryclient()

    client.set_locale ("en_US")
    #client.set_locale ("de")

    # english, male
    #client.set_voice ("dfki-spike")
    #client.set_voice ("dfki-obadiah")
    client.set_voice ("dfki-obadiah-hsmm")
    #client.set_voice ("cmu-bdl-hsmm")
    #client.set_voice ("cmu-rms-hsmm")
    
    # english, female
    #client.set_voice ("dfki-poppy")
    #client.set_voice ("dfki-poppy-hsmm")
    #client.set_voice ("dfki-prudence")
    #client.set_voice ("dfki-prudence-hsmm")
    #client.set_voice ("cmu-slt-hsmm")
    
    # german, male
    #client.set_voice ("dfki-pavoque-neutral")
    #client.set_voice ("dfki-pavoque-neutral-hsmm")
    #client.set_voice ("dfki-pavoque-styles")
    #client.set_voice ("bits3")
    #client.set_voice ("bits3-hsmm")
    
    # german, female
    #client.set_voice ("bits1-hsmm")
    
    # telugu, female
    #client.set_voice ("cmu-nk-hsmm")
    
    # turkish, male
    #client.set_voice ("dfki-ot-hsmm")

    #the_sound = client.generate("I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.")
    the_sound = client.generate("Internet")
    #the_sound = client.generate("Der Atomkern ist der, im Vergleich zur AtomhÃ¦lle, winzig kleine Kern des Atoms.")

    player = pulseplayer("HAL 9000")
    player.play(the_sound)

