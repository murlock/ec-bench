#!/usr/bin/env python

from __future__ import print_function

import time
from hashlib import md5
from oio.common.storage_method import STORAGE_METHODS, EC_SEGMENT_SIZE
from oio.api.ec import ec_encode


POLICIES = """ECISAL84D1=ec/k=8,m=4,algo=isa_l_rs_vand,distance=1
ERASURECODE=ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1
ECISAL42D1=ec/k=4,m=2,algo=isa_l_rs_vand,distance=1
ECISALC35D1=ec/k=3,m=5,algo=isa_l_rs_cauchy,distance=1
DUPONETHREE=plain/distance=1,nb_copy=3
ECLIBEC144D1=ec/k=14,m=4,algo=liberasurecode_rs_vand,distance=1
ECISAL144D1=ec/k=14,m=4,algo=isa_l_rs_vand,distance=1
ECISALC75D1=ec/k=7,m=5,algo=isa_l_rs_cauchy,distance=1
ECLIBEC123D1=ec/k=12,m=3,algo=liberasurecode_rs_vand,distance=1
ECLIBEC42D1=ec/k=4,m=2,algo=liberasurecode_rs_vand,distance=1
DUPONETWO=plain/distance=1,nb_copy=2
ECISAL63D1=ec/k=6,m=3,algo=isa_l_rs_vand,distance=1
ECLIBEC63D1=ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1
ECISAL123D1=ec/k=12,m=3,algo=isa_l_rs_vand,distance=1
DUPONEFOUR=plain/distance=1,nb_copy=4"""

# preload policies
for policy in POLICIES.split("\n"):
    algo = policy.split("=", 1)[1]
    if not algo.startswith("ec/"):
        continue
    method = STORAGE_METHODS.load(algo)

SIZE = 500 * EC_SEGMENT_SIZE
DATA = "A" * EC_SEGMENT_SIZE

# do_fragment_md5 = True
# do_object_md5 = True


def do_run(do_fragment_md5, do_object_md5):
    for policy in POLICIES.split("\n"):
        algo = policy.split("=", 1)[1]
        if not algo.startswith("ec/"):
            continue
        #print("algo", algo)

        method = STORAGE_METHODS.load(algo)
        start = time.time()
        ec_stream = ec_encode(method, method.ec_nb_data + method.ec_nb_parity )

        checksum_obj = md5()
        checksum_parts = [md5() for x in range(method.ec_nb_data + method.ec_nb_parity)]

        ec_stream.send(None)
        size = 0
        while True:
            fragments = ec_stream.send(DATA)
            if do_object_md5:
                checksum_obj.update(DATA)
            if do_fragment_md5:
                for idx, part in enumerate(fragments):
                    checksum_parts[idx].update(part)

            size += len(DATA)
            if size >= SIZE:
                fragments = ec_stream.send("")
                if do_fragment_md5:
                    for idx, part in enumerate(fragments):
                        checksum_parts[idx].update(part)
                break
        end = time.time()

        #print("consumed", end - start, "for", size)
        #print("Speed", size / (end-start) / 1024 / 1024, "MB/s")
        #print("")
        print(algo, do_fragment_md5, do_object_md5, "%5.2f" % (size / (end-start) / 1024 / 1024), "MB/s", sep=",")

for o in (True, False):
    for f in (True, False):
        do_run(do_fragment_md5=f, do_object_md5=o)
