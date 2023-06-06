import os
from trex_stl_lib.api import \
    Ether, TCP, STLStream, STLTXCont, STLPktBuilder, \
    IPv6, IPv6ExtHdrSegmentRouting


class SRV6_1PKT_254FLOW_IP6(object):

    def create_stream(self, pkt_size, src):
        payload_size = pkt_size
        payload_size -= 4  # FCS (outer)

        payload_size -= 20  # TCP (inner)
        payload_size -= 40  # IPv6 (inner)

        payload_size -= 24  # SRH (outer)
        payload_size -= 40  # IPv6 (outer)
        payload_size -= 14  # ETH (outer)

        payload_size -= int(os.getenv("ENCAP_OVERHEAD", 0))

        if payload_size <= 0:
            raise Exception("packet size is too small", pkt_size)

        return STLStream(
            packet=STLPktBuilder(
                pkt=Ether()/IPv6(src=src, dst="bb::1") /
                IPv6ExtHdrSegmentRouting(addresses=["bb::1"]) /
                IPv6(src="dd::1", dst="ee::1") /
                TCP(dport=12, sport=13)/(payload_size*'x')
            ),
            mode=STLTXCont())

    # e.g. pkt_size = 256 - 1518
    def get_streams(self, pkt_size=256, **kwargs):
        streams = []
        for i in range(254):
            src = "aa::"+hex(i+1).replace('0x', '')
            streams.append(self.create_stream(pkt_size,
                                              src=src))
        return streams


# dynamic load - used for trex console or simulator
def register():
    return SRV6_1PKT_254FLOW_IP6()
