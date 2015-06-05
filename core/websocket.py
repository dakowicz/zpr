import struct
import base64
import hashlib


def handshake(client):
    data = client.recv(1024)
    headers = parse_headers(data)

    digest = create_hash(headers['Sec-WebSocket-Key'])
    shake = "HTTP/1.1 101 Web Socket Protocol\r\n"
    shake += "Upgrade: WebSocket\r\n"
    shake += "Connection: Upgrade\r\n"
    shake += "Sec-WebSocket-Accept: " + digest + "\r\n\r\n"

    return client.send(shake)


def create_hash(key):
    hash = hashlib.sha1(key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
    return base64.b64encode(str(hash.digest()))


def parse_headers(data):
    headers = {}
    lines = data.splitlines()
    for l in lines:
        parts = l.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    headers['code'] = lines[len(lines) - 1]
    return headers


def send_data(client, data):
    result = ""
    result += chr(129)
    length = len(data)
    if length <= 125:
        result += chr(length)
    elif 126 <= length <= 65535:
        result += chr(126)
        result += str(struct.pack(">H", length))
    else:
        result += chr(127)
        result += str(struct.pack(">Q", length))
    result += data
    client.send(result)


def recv_data(client, size=1024):
    """
        functions decodes receive data from HTML WebSocket client
        as a simple server, we expect to receive:
        - all data at one go and one frame
        - one frame at a time
        - text protocol
        - no ping pong messages
    :param client: Socket
    :raise: Exception
    :return: nothing
    """
    #
    data = bytearray(client.recv(size))

    if len(data) < 6:
        raise Exception("Error reading data")
    # FIN bit must be set to indicate end of frame

    if 0x1 != (0xFF & data[0]) >> 7:
        raise Exception("Only text frames can be received")
    # data must be a text frame

    if 0x1 != (0xF & data[0]):
        raise Exception("Connection closed")
    # 0x8 (close connection) is handled with assertion failure

    if 0x1 != (0xFF & data[1]) >> 7:
        raise Exception("Data is not masked")
    # assert that data is masked

    data_length = (0x7F & data[1])
    string_data = ''
    if data_length > 0:
        mask_key = data[2:6]
        masked_data = data[6:(6 + data_length)]
        unmasked_data = [masked_data[i] ^ mask_key[i % 4] for i in range(len(masked_data))]
        string_data = str(bytearray(unmasked_data))

    return string_data