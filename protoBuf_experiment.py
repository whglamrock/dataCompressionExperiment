import base64

import LoadCell_pb2
import json
import time
import zlib

def dump():

    f = open('bytes_json', 'rb')
    read_bytes = f.read()
    start_time = time.time()
    data = json.loads(read_bytes)
    print('decoding time for json: is %s seconds' % (time.time() - start_time))
    f.close()

    loadCell = LoadCell_pb2.LoadCell()

    loadCell.recordId.timestamp = str(data['RecordId']['Timestamp'])    # convert bigDecimal(float) to string
    loadCell.recordId.sequenceNumber = data['RecordId']['SequenceNumber']

    loadCell.Id = data['ID']

    for lc_id in data['LC']:
        for timestamp in data['LC'][lc_id]:
            value = data['LC'][lc_id][timestamp]
            loadCell.lc[lc_id].timeStampToDeviceData[timestamp] = value

    loadCell.store = data['Store']

    loadCell.entity = data['Entity']

    for timestamp in data['IMU']:
        for orientationType in data['IMU'][timestamp]:
            for dimension in data['IMU'][timestamp][orientationType]:
                value = str(data['IMU'][timestamp][orientationType][dimension])    # convert bigDecimal to string
                loadCell.timestampToDeviceLocation[timestamp].orientationTypeToCoordinates[orientationType].dimensionToValue[dimension] = value

    start_time = time.time()
    bytes = loadCell.SerializeToString()
    print("encoding time for protoBuf in seconds: %s" % (time.time() - start_time))

    with open('proto_output', 'wb') as f:
        f.write(bytes)

    f_out_gzip = open('compressed_bytes_proto', 'wb')
    compressed_data = zlib.compress(bytes)  # bytes
    f_out_gzip.write(compressed_data)
    f_out_gzip.close()

    encoded = base64.b64encode(compressed_data)
    f = open('compressed_bytes_base64_fromProto', 'wb')
    f.write(encoded)
    f.close()

def read_proto_file():
    loadCell = LoadCell_pb2.LoadCell()
    f = open('proto_output', 'rb')
    read_bytes = f.read()
    start_time = time.time()
    loadCell.ParseFromString(read_bytes)
    print('decoding time for protoBuf: is %s seconds' % (time.time() - start_time))
    f.close()


dump()
read_proto_file()
