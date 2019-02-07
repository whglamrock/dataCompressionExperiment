import base64
import json
import msgpack
import zlib

import time


def dump():
    f = open('bytes_json', 'rb')
    data = json.load(f)
    f.close()

    f = open('msgpack_output', 'wb')

    start_time = time.time()
    binaries = msgpack.dumps(data)
    print("encoding time for mspack in seconds: %s" % (time.time() - start_time))

    f.write(binaries)
    f.close()

    f_out_gzip = open('compressed_bytes_msgpack', 'wb')
    compressed_data = zlib.compress(binaries)   # bytes/binary representation of string
    f_out_gzip.write(compressed_data)
    f_out_gzip.close()

    encoded = base64.b64encode(compressed_data)
    print(type(encoded))
    f = open('compressed_bytes_base64_fromMsgPack', 'wb')
    f.write(encoded)
    f.close()

    start_time = time.time()
    original_data = msgpack.loads(binaries)
    print("decoding time for mspack in seconds: %s" % (time.time() - start_time))
    print(type(original_data))

dump()