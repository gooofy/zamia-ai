#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2013, 2014 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
import subprocess
import json
import psycopg2
from cgi import parse_qs, escape
import pdb
from gutils import run_command, split_words

def hurl_submissions (environ, start_response):

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    #print "     parameters: %s" % repr(parameters)

    sql = 'SELECT id, cfn, prompt, reviewed FROM submissions'
    countsql = 'SELECT Count(*) FROM submissions'
    fcountsql = 'SELECT Count(*) FROM submissions'

    # full text search

    if ('sSearch' in parameters) and (parameters['sSearch'][0] != ''):
        searchstr = parameters['sSearch'][0]
        sql += ' WHERE (cfn LIKE \'%%%s%%\') OR (prompt LIKE \'%%%s%%\')' % (searchstr, searchstr)
        fcountsql += ' WHERE (cfn LIKE \'%%%s%%\') OR (prompt LIKE \'%%%s%%\')' % (searchstr, searchstr)

    # ordering

    if 'iSortCol_0' in parameters:
        col = int(parameters['iSortCol_0'][0])
        #print "     sort column: %s" % repr(col)
        if col == 1:
          sql += ' ORDER BY cfn ' + parameters['sSortDir_0'][0]
        elif col == 2:  
          sql += ' ORDER BY prompt ' + parameters['sSortDir_0'][0]
        elif col == 3:  
          sql += ' ORDER BY reviewed,cfn ' + parameters['sSortDir_0'][0]

    # paging

    if ('iDisplayStart' in parameters) and (parameters['iDisplayLength'][0] != '-1'):
        sql += ' OFFSET %s LIMIT %s' % (parameters['iDisplayStart'][0], parameters['iDisplayLength'][0])

    res = {}

    cur.execute (countsql)
    row = cur.fetchone()
    res['iTotalRecords'] = row[0]

    #print "     #1 res: %s" % repr(res)
    #print "     sql   : %s" % sql

    cur.execute (fcountsql)
    row = cur.fetchone()
    res['iTotalDisplayRecords'] = row[0]

    #print "     #2 res: %s" % repr(res)

    res['aaData'] = []
    cur.execute (sql)
    rows = cur.fetchall()
    for row in rows:
        res['aaData'].append ( [ row[0], row[1], row[2], row[3] ] )

    #print "     #3 res: %s" % repr(res)

    start_response('200 OK', [('Content-Type', 'application/json')])

    return json.dumps(res)

def hurl_wav (environ, start_response):

    global audiodir

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    #print "     parameters: %s" % repr(parameters)

    sql = 'SELECT dir, audiofn FROM submissions WHERE id=' + parameters['id'][0]

    cur.execute (sql)
    row = cur.fetchone()

    wavfn = audiodir + '/' + row[0] + '/wav/' + row[1] + '.wav'

    #print "Request for wav: %s" % wavfn

    len = os.path.getsize (wavfn)

    start_response('200 OK', [('Content-Type', 'audio/wav'), ('Content-Length', str(len))])

    with open (wavfn) as content_file:
        buf = [ content_file.read() ]

    return buf

def hurl_save (environ, start_response):

    global conn, cur

    #print "hurl_save environment:"
    #for k,v in sorted(environ.items()):
    #    print "    %-20s: %s" % (k, v)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    
    request_body = environ['wsgi.input'].read(request_body_size)

    #print "request_body = %s" % request_body

    data = json.loads(request_body)
    #print "     data: %s" % repr(data)
    
    cur.execute ('UPDATE submissions SET reviewed=true, noiselevel=%s, truncated=%s, comment=%s, audiolevel=%s, pcn=%s WHERE id=%s',
                 (data['noiselevel'], data['truncated'], data['comment'], data['audiolevel'], data['pcn'], data['sid']))


    # transcript
    cur.execute ('DELETE FROM transcripts WHERE sid=%s', (data['sid'],))
    for winfo in data['transcript']:
        #print "    winfo: %s" % repr(winfo)
        cur.execute ('INSERT INTO transcripts (sid,wid,pid) VALUES (%s, %s, %s)', 
                     (data['sid'], winfo['wid'], winfo['pid']))


    conn.commit()

    cur = conn.cursor()
            
    return "OK"

def hurl_setprompt (environ, start_response):

    global conn, cur

    parameters = parse_qs(environ.get('QUERY_STRING', ''))

    pd = parameters['data'][0]

    #print "     pd: %s" % repr(pd)

    data = json.loads(pd)
    #print "     sid: %s, prompt: %s" % (data['sid'], data['prompt'])

    cur.execute ('UPDATE submissions SET prompt=%s WHERE id=%s',
                 (data['prompt'].replace('\n',' ').replace('\r',' '), data['sid']))

    conn.commit()

    cur = conn.cursor()
            
    return "OK"

def hurl_submission_get_details (environ, start_response):

    global conn, cur

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    #print "     parameters: %s" % repr(parameters)

    sql = 'SELECT prompt, reviewed, noiselevel, truncated, comment, audiolevel, pcn FROM submissions WHERE id=' + parameters['id'][0]

    cur.execute (sql)
    row = cur.fetchone()
    res = {'prompt'      : row[0].decode('UTF8'), 
           'reviewed'    : row[1],
           'noiselevel'  : row[2],
           'truncated'   : row[3],
           'comment'     : row[4],
           'audiolevel'  : row[5],
           'pcn'         : row[6],
           'transcript'  : []
        }

    # do we have a transcript for this submission in our db?
    cur2 = conn.cursor()
    cur2.execute ('SELECT wid, pid FROM transcripts WHERE sid=%s ORDER BY id ASC',
                  (parameters['id'][0],))

    # collect dictionary entries for all the words

    words = split_words (res['prompt'])
    for word in words:

        wentry = { 'word': word, 'pronounciations': [] }

        # dict lookup

        cur.execute ('SELECT id FROM words WHERE word=%s', (word,))
        row = cur.fetchone()
        if row:
            wentry['wid'] = row[0]

            selpid = 0

            cur.execute ('SELECT phonemes, id FROM pronounciations WHERE wid=%s', (wentry['wid'],))
            rows = cur.fetchall()
            for row in rows:

                pentry = { 'pid': row[1],
                           'ipa': row[0].decode('UTF8') }

                wentry['pronounciations'].append(pentry)
                selpid = row[1]

            # matching pronounciation?
            row = cur2.fetchone()
            if row and row[0] == wentry['wid']:
                wentry['selpid'] = row[1]
            else:
                wentry['selpid'] = selpid

        res['transcript'].append(wentry)

    cur2.close()

    #print "Result: %s" % repr (res)

    start_response('200 OK', [('Content-Type', 'application/json')])

    return json.dumps(res)

def app(environ, start_response):

    global webroot    

    #print
    #print "-------------------------------------------------------------------------------"
    #print "GOT A REQUEST:" 
    #for f in [ 'REQUEST_METHOD', 'PATH_INFO', 'QUERY_STRING'] :
    #    print "     %-15s : %s"% (f, environ.get(f, ''))

    path = environ.get('PATH_INFO', '/')

    if path.startswith ('/submissions'):

        return hurl_submissions (environ, start_response)

    elif path.startswith ('/submission_get_details'):

        return hurl_submission_get_details (environ, start_response)

    elif path.startswith ('/wav'):

        return hurl_wav (environ, start_response)

    elif path.startswith ('/save'):

        return hurl_save (environ, start_response)

    elif path.startswith ('/setprompt'):

        return hurl_setprompt (environ, start_response)

    else:

        # for now, serve static files from here

        if path.endswith ('.js'):
            start_response('200 OK', [('Content-Type', 'application/javascript')])
        elif path.endswith ('.png'):
            start_response('200 OK', [('Content-Type', 'image/png')])
        elif path.endswith ('.css'):
            start_response('200 OK', [('Content-Type', 'text/css')])
        else:
            start_response('200 OK', [('Content-Type', 'text/html')])

        if path == '/':
            path = '/index.html'

        fn = path[1:].replace('/', '_')

        with open ("%s/%s" % (webroot, fn)) as content_file:
            buf = [ content_file.read() ]

        return buf

if __name__ == '__main__':

    os.system ('gunicorn -b localhost:8000 -w 1 audio-transcribe:app')

    sys.exit(0)


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

webroot   = config.get("speech", "webroot")

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

audiodir  = config.get("speech", "audiodir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()



