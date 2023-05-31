import os
from trex_stl_lib.api import \
    Ether, IP, TCP, STLStream, STLTXCont, STLPktBuilder, STLScVmRaw, \
    STLVmFlowVar, STLVmWrFlowVar, STLVmFixIpv4


class TCP_1PKT_RAND(object):

    def create_stream(self, pkt_size):
        payload_size = pkt_size
        payload_size -= 4  # FCS
        payload_size -= 20  # TCP
        payload_size -= 20  # IPv4
        payload_size -= 14  # ETH
        payload_size -= int(os.getenv("ENCAP_OVERHEAD", 0))

        vm = STLScVmRaw([
            STLVmFlowVar(name="ip_src",
                         min_value="16.0.0.0",
                         max_value="18.0.0.254",
                         size=4, op="random"),
            STLVmFlowVar(name="src_port",
                         min_value=1025,
                         max_value=65000,
                         size=2, op="random"),
            STLVmWrFlowVar(fv_name="ip_src", pkt_offset="IP.src"),
            STLVmFixIpv4(offset="IP"),  # fix checksum
            STLVmWrFlowVar(fv_name="src_port", pkt_offset="TCP.sport")])

        return STLStream(
            packet=STLPktBuilder(
                pkt=Ether()/IP(dst="1.0.0.1")/TCP(dport=12)/(payload_size*'x'),
                vm=vm,
            ),
            random_seed=0x1234,
            mode=STLTXCont())

    # e.g. pkt_size = 64 - 1518
    def get_streams(self, pkt_size=64, **kwargs):
        return [self.create_stream(pkt_size)]


# dynamic load - used for trex console or simulator
def register():
    return TCP_1PKT_RAND()
