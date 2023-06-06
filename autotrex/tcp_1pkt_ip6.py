import os
from trex_stl_lib.api \
        import Ether, IPv6, TCP, STLStream, STLTXCont, STLPktBuilder


class TCP_1PKT_IP6(object):

    def create_stream(self, pkt_size):
        payload_size = pkt_size
        payload_size -= 4  # FCS
        payload_size -= 20  # TCP
        payload_size -= 40  # IPv6
        payload_size -= 14  # ETH
        payload_size -= int(os.getenv("ENCAP_OVERHEAD", 0))

        return STLStream(
            packet=STLPktBuilder(
                pkt=Ether()/IPv6(src="aa::1", dst="bb::1") /
                TCP(dport=12, sport=1025)/(payload_size*'x')
            ),
            mode=STLTXCont())

    # e.g. pkt_size = 128 - 1518
    def get_streams(self, pkt_size=128, **kwargs):
        return [self.create_stream(pkt_size)]


# dynamic load - used for trex console or simulator
def register():
    return TCP_1PKT_IP6()
