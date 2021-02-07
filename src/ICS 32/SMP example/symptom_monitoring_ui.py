import socket
import symptom_monitoring as smp
from symptom_monitoring import SMPConnection, SMPProtocolError


PORT = 2020
HOST = "127.0.0.1"

# Not a complete list, but you get the idea
SYMPTOM_LIST = "Fever\nChills\nMuscle aches\nCough\nShortness of breath\nUnexpected Fatigue\nSore throat"

def _run_program():

    print("Welcome to the UCI Working Well Daily Symptom Checker")
    print()
    print("To get started, enter your UCI provided email address")
    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    _smp_conn = smp.init(sock)
    
    try:
        while True:
            userid = input()

            res = smp.authenticate(_smp_conn, userid)
            if res == smp.NOUSER:
                print('Unable to find user. Check your ID and try again.')
            else:
                break
        
        while True:
            if _report_status(_smp_conn) == smp.COMPLETE:
                print('Thank you. No further action is required.')
                break
            
            if _report_symptoms(_smp_conn) == smp.COMPLETE:
                print('Thank you. No further action is required.')
                break
            
            if _report_tested(_smp_conn) == smp.CONTINUE:
                if _report_proximity(_smp_conn) == smp.COMPLETE:
                    print('Thank you. It is advised that you do not come to campus today.')
                    break
                else:
                    print('Thank you. No further action is required.')
                    break
            else:
                print('Thank you. No further action is required.')
                break
    except SMPProtocolError:
        print("An error occurred while attempting to communicate with the remote server.")    
    else:
        # only disconnect if an SMPProtocolError did not occur
        smp.disconnect(_smp_conn)
    finally:
        sock.close()

def _report_status(smp_conn: SMPConnection) -> str:
    # check for on-site work
    prompt = "Are you scheduled to work on site today (yes, no)? "
    return _report(smp_conn, smp.STATUS, prompt)

def _report_symptoms(smp_conn: SMPConnection) -> str:
    # check for symptoms
    prompt = '{}\r\n\r\n{}\r\n\r\n(yes, no)? '.format(
        'Are you experiencing any of the following symptoms: ',
        SYMPTOM_LIST)
    return _report(smp_conn, smp.SYMPTOMS, prompt)

def _report_tested(smp_conn: SMPConnection) -> str:
    # check if tested
    prompt = "Have you been tested for COVID-19 in thet past 14 days (yes, no)? "
    return _report(smp_conn, smp.TESTED, prompt)

def _report_proximity(smp_conn: SMPConnection) -> str:
    # check if near positive
    prompt = "Have you been within 6 feet of a COVID-19 infected person for at least 15 minutes within the last 14 days? (yes, no)? "
    return _report(smp_conn, smp.PROXIMITY, prompt)

def _report(smp_conn: SMPConnection, cmd: str, user_prompt: str) -> str:
    user_input = input(user_prompt)

    try:
        status = _parse_input(user_input)
        return smp.report(smp_conn, cmd, status)
    except ValueError:
        print("Please response with either 'yes' or 'no'")
        _report(smp_conn, cmd, user_prompt)


def _parse_input(val: str) -> int:
    if val == "yes":
        return 1
    elif val == "no":
        return 0
    else:
        raise ValueError

if __name__ == '__main__':
    _run_program()