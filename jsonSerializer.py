import base64
import json
import zlib

import time


def serialize():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()

    start_time = time.time()
    bytes = json.dumps(data).encode('utf-8')
    print("encoding time for json in seconds: %s" % (time.time() - start_time))
    print(type(bytes))

    f_out = open('bytes_json', 'wb')
    f_out.write(bytes)
    f_out.close()

    # base64 the bytes_json
    encoded = base64.b64encode(bytes)
    f = open('bytes_base64_fromJson', 'wb')
    f.write(encoded)
    f.close()

    f_out_gzip = open('compressed_bytes_json', 'wb')

    compressed_data = zlib.compress(bytes)
    f_out_gzip.write(compressed_data)
    f_out_gzip.close()

    encoded = base64.b64encode(compressed_data)
    print(type(encoded))
    f = open('compressed_bytes_base64_fromJson', 'wb')
    f.write(encoded)
    f.close()

def serialize_noIMU():
    f = open('data_noIMU.json', 'r')
    data = json.load(f)
    f.close()

    bytes = json.dumps(data).encode('utf-8')
    f_out = open('bytes_noIMU_json', 'wb')
    f_out.write(bytes)
    f_out.close()

    # base64 the bytes_json
    encoded = base64.b64encode(bytes)
    f = open('bytes_noIMU_base64_fromJson', 'wb')
    f.write(encoded)
    f.close()

    bytes = json.dumps(data).encode('utf-8')
    f_out_gzip = open('compressed_bytes_noIMU_json', 'wb')

    compressed_data = zlib.compress(bytes)
    f_out_gzip.write(compressed_data)
    f_out_gzip.close()

serialize()
serialize_noIMU()