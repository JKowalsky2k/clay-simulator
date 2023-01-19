import platform
import socket
import re
import uuid
import json
import psutil
from cryptography.fernet import Fernet

class Security:
    def __init__(self) -> None:
        self.secret_key = b'-d3XhZsvyvaUTsICb7TcyV-PBTDkOL3sLD8cQ_c4UCE='
        self.signature = 'gAAAAABjyY4EJ1O21xebM6dfei8ctOccUCKciCdw_Q6Wk2zuu85c-rIm_HNDKhCXPrrNwmKJYzqbgtjgbAqLvtKe5tdQU25y74bDWts56UXqPs74dq08xvOKHxhnB4P2tPxH7fnwrNzVDj387l7S6ZPXIxqQBW0GH5o5YJ0PPmRfPyRI2X50hbHcqc3Y4GcrILGDXifmE5bis81rZAMgQNu6rR1u7SdGWFlfvsvs1l07szTkZ0yWwarZXKk819XUbpBIQkTaj2SehBAhlSut_Sduz8SGgLNCHw=='
        self.security_engine = Fernet(self.secret_key) 
    
    def get_sys_info(self):
        try:
            info={}
            info['platform']=platform.system()
            info['architecture']=platform.machine()
            info['hostname']=socket.gethostname()
            info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']=platform.processor()
            info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            print(f'{info = }\n')
            print(f'{self.security_engine.decrypt(self.signature).decode() = }\n')
            return json.dumps(info)
        except Exception as error:
            print(f'{error = }')

    def check(self):
        print(f'{self.get_sys_info() = }')
        return self.get_sys_info() == self.security_engine.decrypt(self.signature).decode()

    