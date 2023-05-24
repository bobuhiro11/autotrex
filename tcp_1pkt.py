from trex_stl_lib.api import *
import argparse

class UDP_1STREAM(object):

    def create_stream (self, pkt_size):
        payload_size = pkt_size
        payload_size -= 4  # FCS
        payload_size -= 20 # TCP
        payload_size -= 20 # IPv4
        payload_size -= 14 # ETH

        return STLStream(
            packet =
                    STLPktBuilder(
                        pkt = Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/
                                TCP(dport=12,sport=1025)/(payload_size*'x')
                    ),
             mode = STLTXCont())

    # e.g. pkt_size = 64 - 1518
    def get_streams (self, pkt_size=64, **kwargs):
        # parser = argparse.ArgumentParser(description='Argparser for {}'.format(os.path.basename(__file__)),
                                         # formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # args = parser.parse_args(tunables)
        # create 1 stream
        return [ self.create_stream(pkt_size) ]


# dynamic load - used for trex console or simulator
def register():
    return UDP_1STREAM()
