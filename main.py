import requests
import time
import os
from twilio.rest import Client
import socket
import time


def create_magic_packet(macaddress: str):
    if len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, "")
    elif len(macaddress) != 12:
        raise ValueError("Incorrect MAC address format")
    payload = "F" * 12 + macaddress * 16
    payload = bytes.fromhex(payload)
    return payload

client = Client('AC542f3a28d53f0d826f21ef0b1030193f', '849df89b9112e53e22db833bc1072c20')
miner_address = "0x1cF084aB43De754c6405442F8eAcC872948B9A01"
mac = "24:4b:Fe:58:9e:8a"
ip = "255.255.255.255"
port = 9

while True:

    r = requests.get(f'https://api.ethermine.org/miner/{miner_address}/currentStats')
    reportedHashrate = dict(r.json())["data"]["reportedHashrate"]
    if reportedHashrate == 0:
        print(dict(r.json())["data"])
        message = client.messages.create(
                     body="<<<Sela, Worker is down>>>",
                     from_='+13234194750',
                     to='+85511249691'
                 ) 
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                packet = create_magic_packet(mac)
                if len(packet) != 102:
                    raise ValueError(
                        "Packet Byte Length Must be 102, instead, got {}".format(len(packet)))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(packet, (ip, port))
        except socket.gaierror as e:
            print(e)
            print("Connection failed")
        except ValueError as e:
            print(e)
        
        time.sleep(100)
    
    time.sleep(300)