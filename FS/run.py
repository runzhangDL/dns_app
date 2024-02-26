from flask import Flask, request, Response
import json, socket

app = Flask(__name__)

def get_fibonacci(seq_number):
    if seq_number == 1:
        return 0
    if seq_number == 2:
        return 1
    a = 0
    b = 1
    res = 0
    for i in range(3, seq_number+1):
        res = a + b
        a = b
        b = res
    return res

@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    number = request.args.get('number')
    if number is None:
        return Response("Bad Request: Missing Parameter", status=400)
    try:
        number = int(number)
    except:
        return Response("Bad Format: Number is not integer", status=400)
    
    return Response(f"{get_fibonacci(number)}", status=200)

@app.route("/register", methods=["PUT"])
def register():
    content = request.get_json()
    message = f"TYPE=A\nNAME={content['hostname']}\nVALUE={content['ip']}\nTTL=10\n"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), (content['as_ip'], int(content['as_port'])))
        res, _ = sock.recvfrom(1024)
        if res.decode() == "success":
            return Response("success", status=201)
    
    return Response("Error", status=400)

app.run(host='0.0.0.0',
        port=9090,
        debug=True)