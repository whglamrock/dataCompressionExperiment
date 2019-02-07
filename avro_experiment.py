import base64
import io
import json

import avro.schema as avroSchema
import avro.io as avroIo
import zlib

import time

test_schema = '''
{"namespace": "LoadCell.avro",
 "type": "record",
 "name": "LoadCell_avro",
 "fields": [
   {"name": "RecordId", "type": {
        "fields": [{"name": "Timestamp", "type": "string"}, {"name": "SequenceNumber", "type": "long"}],
        "name": "recordId_Inner",
        "type": "record"}
   },
   {"name": "ID", "type": "string"},
   {"name": "Store",  "type": "string"},
   {"name": "Entity", "type": "string"},
   {"name": "LC", "type": {"type": "map", "values": {"type": "map", "values": "long"}}},
   {"name": "IMU", "type": {"type": "map", "values": {"type": "map", "values": {"type": "map", "values": "string"}}}}
  ]
}
'''

schema = avroSchema.Parse(test_schema)
writer = avroIo.DatumWriter(schema)
reader = avroIo.DatumReader(schema)

def dump():

    f = open('bytes_json', 'rb')
    data = json.load(f)
    f.close()
    data['RecordId']['Timestamp'] = str(data['RecordId']['Timestamp'])

    for timestamp in data['IMU']:
        for orientationType in data['IMU'][timestamp]:
            for dimension in data['IMU'][timestamp][orientationType]:
                data['IMU'][timestamp][orientationType][dimension] = str(data['IMU'][timestamp][orientationType][dimension])

    bytes_writer = io.BytesIO()
    encoder = avroIo.BinaryEncoder(bytes_writer)
    start_time = time.time()
    writer.write(data, encoder)
    print("encoding time for avro in seconds: %s" % (time.time() - start_time))

    bytes = bytes_writer.getvalue()
    print(len(bytes))
    print(type(bytes))

    with open('avro_output', 'wb') as f:
        f.write(bytes)

    f_out_gzip = open('compressed_bytes_avro', 'wb')
    compressed_data = zlib.compress(bytes)  # bytes
    f_out_gzip.write(compressed_data)
    f_out_gzip.close()

    encoded = base64.b64encode(compressed_data)
    f = open('compressed_bytes_base64_fromAvro', 'wb')
    f.write(encoded)
    f.close()

    # decoding
    bytes_reader = io.BytesIO(bytes)
    decoder = avroIo.BinaryDecoder(bytes_reader)
    start_time = time.time()
    original_data = reader.read(decoder)
    print("decoding time for avro in seconds: %s" % (time.time() - start_time))



dump()