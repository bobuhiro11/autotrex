from trex_stl_lib.api \
        import Ether, IP, TCP, STLStream, STLTXCont, STLPktBuilder


class TCP_1PKT(object):

    def create_stream(self, pkt_size):
        payload_size = pkt_size
        payload_size -= 4  # FCS
        payload_size -= 20  # TCP
        payload_size -= 20  # IPv4
        payload_size -= 14  # ETH

        return STLStream(
            packet=STLPktBuilder(
                pkt=Ether()/IP(src="16.0.0.1", dst="48.0.0.1") /
                TCP(dport=12, sport=1025)/(payload_size*'x')
            ),
            mode=STLTXCont())

    # e.g. pkt_size = 64 - 1518
    def get_streams(self, pkt_size=64, **kwargs):
        return [self.create_stream(pkt_size)]


# dynamic load - used for trex console or simulator
def register():
    return TCP_1PKT()
