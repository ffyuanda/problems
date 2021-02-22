# symptom_monitoring.py
# 
# ICS 32 Fall 2020
# Code Example
#
# This module provides functions that implement the UCI Symptom Monitoring Protocol. The UCI Symptom Monitoring Protocol is an example protocol developed for ICS 32, but inspired by the UCI Working Well Daily Symptom Check email. This module is designed to be used by both Symptom Monitoring client and server programs.
# 

import socket
from collections import namedtuple

class SMPProtocolError(Exception):
    pass

"""
Here we establish constant variables that will contain the keywords
used by the protocol.
"""
AUTH = "SMP_AUTH"
STATUS = "SMP_STATUS"
SYMPTOMS = "SMP_SYMPTOMS"
TESTED = "SMP_TESTED"
PROXIMITY = "SMP_PROXIMITY"

WELCOME = "WELCOME"
CONTINUE = "CONTINUE"
COMPLETE = "COMPLETE"
NOUSER = "NOUSER"
ERROR = "ERROR"

"""
A namedtuple conveniently encapsulates the objects we need to use to communicate over a socket connection in many of the functions in this module. Rather than pass multiple objects, it is cleaner to wrap them in a single namedtuple.
"""
SMPConnection = namedtuple('SMPConnection',['socket','send','recv'])

"""


"""
def init(sock:socket) -> SMPConnection:
    '''
    The init method should be called for every program that uses the SMP Protocol.
    The calling program should first establish a connection with a socket object,
    then pass that open socket to init. init will then create file objects
    to handle input and output.
    '''
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except:
        raise SMPProtocolError("Invalid socket connection")

    return SMPConnection(
        socket=sock,
        send=f_send,
        recv=f_recv
    )


def disconnect(smp_conn: SMPConnection):
    '''
    provide a way to close read and write file objects
    '''
    smp_conn.send.close()
    smp_conn.recv.close()

def listen(smp_conn: SMPConnection) -> str:
    '''
    listen will block until a new message has been received
    '''
    return _read_command(smp_conn)


def authenticate(smp_conn: SMPConnection, userid: str) -> str:
    '''
    a helper method to authenticate a userid with a server
    '''
    cmd = '{} {}'.format(AUTH, userid)
    _write_command(smp_conn, cmd)
    result = _read_command(smp_conn)
    
    return result

def report(smp_conn: SMPConnection, report: str, status: str) -> str:
    '''
    report will send the command specified by the parameters and return a response to the command using the SMP Protocol.

    report: one of the SMP_X commands provided by the module
    status: either 0 or 1 to indicate the status of the command specified in the report parameter
    '''
    cmd = '{} {}'.format(report, status)
    _write_command(smp_conn, cmd)
    return _read_command(smp_conn)


def nouser(smp_conn: SMPConnection):
    '''
    a send only wrapper for the NOUSER command
    '''
    _write_command(smp_conn, NOUSER)

def error(smp_conn: SMPConnection):
    '''
    a send only wrapper for the ERROR command
    '''
    _write_command(smp_conn, ERROR)

def welcome(smp_conn: SMPConnection):
    '''
    a send only wrapper for the WELCOME command
    '''
    _write_command(smp_conn, WELCOME)

def complete(smp_conn: SMPConnection):
    '''
    a send only wrapper for the COMPLETE command
    '''
    _write_command(smp_conn, COMPLETE)

def next(smp_conn: SMPConnection):
    '''
    a send only wrapper for the CONTINUE command
    '''
    _write_command(smp_conn, CONTINUE)

def _write_command(smp_conn: SMPConnection, cmd: str):
    '''
    performs the required steps to send a message, including appending a newline sequence and flushing the socket to ensure
    the message is sent immediately.
    '''
    try:
        smp_conn.send.write(cmd + '\n')
        smp_conn.send.flush()
    except:
        raise SMPProtocolError

def _read_command(smp_conn: SMPConnection) -> str:
    '''
    performs the required steps to receive a message. Trims the 
    newline sequence before returning
    '''
    cmd = smp_conn.recv.readline()[:-1]
    return cmd
