import os
from trex_stl_lib.api import \
    Ether, IP, TCP, STLStream, STLTXCont, STLPktBuilder, \
    IPv6, IPv6ExtHdrSegmentRouting


class TCP_1PKT_254FLOW(object):

    def create_stream(self, pkt_size, src):
        payload_size = pkt_size
        payload_size -= 4  # FCS (outer)

        payload_size -= 20  # TCP (inner)
        payload_size -= 20  # IPv4 (inner)

        payload_size -= 24  # SRH (outer)
        payload_size -= 40  # IPv6 (outer)
        payload_size -= 14  # ETH (outer)

        payload_size -= int(os.getenv("ENCAP_OVERHEAD", 0))

        return STLStream(
            packet=STLPktBuilder(
                pkt=Ether()/IPv6(src=src, dst="bb::1") /
                IPv6ExtHdrSegmentRouting(addresses=["bb::1"]) /
                IP(src="16.0.0.1", dst="48.0.0.1") /
                TCP(dport=12, sport=13)/(payload_size*'x')
            ),
            mode=STLTXCont())

    # e.g. pkt_size = 128 - 1518
    def get_streams(self, pkt_size=128, **kwargs):
        streams = []
        for i in range(254):
            src = "aa::"+hex(i+1).replace('0x', '')
            streams.append(self.create_stream(pkt_size,
                                              src=src))
        return streams


# dynamic load - used for trex console or simulator
def register():
    return TCP_1PKT_254FLOW()
