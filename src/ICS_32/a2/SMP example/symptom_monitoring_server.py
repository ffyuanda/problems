import socket
import symptom_monitoring as smp
from symptom_monitoring import SMPConnection, SMPProtocolError

PORT = 2020
HOST = "127.0.0.1"

def authenticate(smp_conn: SMPConnection, cmd: str) -> bool:
    if cmd[:len(smp.AUTH)] == smp.AUTH:
        # valid auth request
        # TODO: validate user auth against a known addresses
        return True
    else:
        return False

def process_command(msg, cmd) -> int:
    print(msg[:len(cmd)])
    if msg[:len(cmd)] == cmd:
        # command matches expectation, so get status
        status = rec_msg[len(cmd)+1:]
        print(status)
        status_val = -1
        try:
            status_val = int(status)
        except:
            raise SMPProtocolError
        finally:
            if status_val == 0 or status_val == 1:
                return status_val
            else:
                raise SMPProtocolError
    else:
        raise SMPProtocolError



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.bind((HOST, PORT))
    srv.listen()

    print("server listening on port", PORT)
    while True:
        connection, address = srv.accept()

        with connection:
            print("client connected")
            _smp_conn = smp.init(connection)

            # First message should be attempt to authenticate
            rec_msg = smp.listen(_smp_conn)
            if authenticate(_smp_conn, rec_msg):
                print("client authenticated")
                smp.welcome(_smp_conn)
                while True:
                    rec_msg = smp.listen(_smp_conn)
                    print("message: ", rec_msg)
                    try:
                        if process_command(rec_msg, smp.STATUS) == 0:
                            smp.complete(_smp_conn)
                            break
                        
                        smp.next(_smp_conn)
                        rec_msg = smp.listen(_smp_conn)
                        if process_command(rec_msg, smp.SYMPTOMS) == 0:
                            smp.complete(_smp_conn)
                            break

                        smp.next(_smp_conn)
                        rec_msg = smp.listen(_smp_conn)
                        process_command(rec_msg, smp.TESTED) 
                            # record answer
                        smp.next(_smp_conn)
                        rec_msg = smp.listen(_smp_conn)
                        process_command(rec_msg, smp.PROXIMITY) 

                        smp.complete(_smp_conn)
                    except Exception as ex:
                        print(ex)
                        break
                        #smp.error(_smp_conn)
            else:
                smp.nouser(_smp_conn)
            print("client disconnected")

