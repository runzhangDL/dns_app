import requests, json, socket

r = requests.put("http://0.0.0.0:9090/register",
                  data=json.dumps({
                      "hostname": "fibonacci.com",
                      "ip": "172.17.0.5",
                      "as_ip": "172.17.0.4",
                      "as_port": "53533"
                  }),
                  headers={
                      "Content-Type":"application/json"
                })

# message = f"TYPE=A\nNAME=fibonacci.com\nVALUE=0.0.0.0\nTTL=10\n"

# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
#     print("start")
#     sock.sendto(message.encode(), ("0.0.0.0", 53533))
#     print("wait")
#     res, _ = sock.recvfrom(1024)
#     print("back")