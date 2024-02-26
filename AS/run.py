import socket
from multiprocessing import Process
import re

def registration():
    print("registration service start")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', 53533))
        while True:
            message, clientAddress = sock.recvfrom(2048)
            print("message received")
            if "NAME" in message.decode() and "VALUE" in message.decode():
                print("registration processing")
                name = re.findall(r'NAME=(.*)\n', message.decode())[0]
                value = re.findall(r'VALUE=(.*)\n', message.decode())[0]

                with open("./DNSRecord.txt", 'a') as f:
                    f.write(f"{name} {value}\n")

                print(f"Registration for {name} {value} succeed")
                sock.sendto('success'.encode(), clientAddress)
            elif "NAME" in message.decode():
                print("DNS query processing")
                name = re.findall(r'NAME=(.*)\n', message.decode())[0]

                with open("./DNSRecord.txt", 'r') as f:
                    for line in f:
                        record_name, record_ip = line.split()
                        if record_name == name:
                            print(f"DNS Query for {name} done")
                            response_message = f"TYPE=A\nNAME={record_name}\nVALUE={record_ip}\nTTL=10\n"
                            sock.sendto(response_message.encode(), clientAddress)

    pass

if __name__ == "__main__":
    # t1 = Process(target=registration)
    # t1.start()
    # t1.join()
    registration()