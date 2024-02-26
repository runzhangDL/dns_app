from flask import Flask, request, Response
import socket
import re
import requests

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    if hostname is None:
        return Response("Bad Request: Missing Parameter", status=400)
    fs_port = request.args.get('fs_port')
    if fs_port is None:
        return Response("Bad Request: Missing Parameter", status=400)
    number = request.args.get('number')
    if number is None:
        return Response("Bad Request: Missing Parameter", status=400)
    as_ip = request.args.get('as_ip')
    if as_ip is None:
        return Response("Bad Request: Missing Parameter", status=400)
    as_port = request.args.get('as_port')
    if as_port is None:
        return Response("Bad Request: Missing Parameter", status=400)
    
    message = f"TYPE=A\nNAME={hostname}\n"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), (as_ip, int(as_port)))
        res, _ = sock.recvfrom(1024)
        fs_ip = re.findall(r'VALUE=(.*)\n', res.decode())[0]
    
    print(fs_ip, fs_port)

    r = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")

    print(r, r.content)
    
    return Response(r.content.decode(), status=200)

app.run(host='0.0.0.0',
        port=8080,
        debug=True)