#!/usr/bin/env python3
import sys

sys.path.append(
    "/tmp/v3.02/automation/trex_control_plane" \
    + "/interactive/trex/examples/stl"
)

# FIXME: pkt -> eth

# I don't know why but if pkt is small, then duration is ignored.
DURATION = 1

import stl_path
from trex.stl.api import *
from trex.utils.text_opts import format_text
import matplotlib.pyplot as plt
import time

# e.g. pkg_size = 64 - 1518
def single_run(c, profile, mult, pkt_size):
    start_at = time.time()

    c.reset(ports = [0, 1])
    c.remove_all_streams()
    c.add_streams(profile.get_streams(), ports = [0, 1])

    c.start(ports = [0], mult = str(mult) + "%", duration = DURATION)
    c.wait_on_traffic(ports = [0, 1])
    s = c.get_stats()

    total = s["total"]
    tx_pkts = total["opackets"]
    rx_pkts = total["ipackets"]
    bps = total["tx_bps"]
    pps = total["tx_pps"]

    lossrate = max(0.0, (1 - rx_pkts / tx_pkts)) * 100.0 # percent
    success = lossrate <= 0.01

    end_at = time.time()

    result = {
        "success": success,
        "pkt_size": pkt_size,
        "mult_pct": mult,
        "lossrate_pct": lossrate,
        "bps": bps,
        "pps": pps,
        "tx_pkts": tx_pkts,
        "rx_pkts": rx_pkts,
        "duration": end_at - start_at,
    }
    print(result)

    return success, result


def run(c, pkt_size):
    profile = STLProfile.load_py("./tcp_1pkt.py", pkt_size = pkt_size)

    ok = 1
    ng = 101
    for k in range(7): # 7 is enough to cover [1-100] mult.
        if ok == ng - 1:
            break

        mid = int((ok + ng) / 2)
        success, _ = single_run(c, profile, mid, pkt_size)

        if success:
            ok = mid
        else:
            ng = mid

    _, result = single_run(c, profile, ok, pkt_size)
    return result


def plot_Gbps(packet_sizes, Gbpss, link_speed_bps):
   X = packet_sizes
   Y = Gbpss
   Y_max = []

   # Calc theoretical maximum throuput.
   for pkt_size in packet_sizes:
       n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8) # include preameble(8Bytes)+inter frame gap(12Bytes)
       Y_max.append(n_pkts * pkt_size * 8 / 1e9) # convert unit from bytes to Gbits.

   plt.clf()
   plt.style.use('seaborn-whitegrid')
   plt.xlabel("Packet size (Bytes)")
   plt.ylabel("Throuput (Gbps)")
   plt.xticks(X)
   plt.ticklabel_format(style='plain')
   plt.plot(X, Y_max, marker=".", label="Theoretical", color="0.8")
   plt.plot(X, Y, marker=".", label="Actual", linewidth=3)
   plt.legend()
   plt.savefig("Gbps.png")


def plot_Mpps(packet_sizes, Mppss, link_speed_bps):
   X = packet_sizes
   Y = Mppss
   Y_max = []

   # Calc theoretical maximum throuput.
   for pkt_size in packet_sizes:
       n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8) # include preameble(8Bytes)+inter frame gap(12Bytes)
       Y_max.append(n_pkts / 1e6)

   plt.clf()
   plt.style.use('seaborn-whitegrid')
   plt.xlabel("Packet size (Bytes)")
   plt.ylabel("Packet rate (Mpps)")
   plt.xticks(X)
   plt.ticklabel_format(style='plain')
   plt.plot(X, Y_max, marker=".", label="Theoretical", color="0.8")
   plt.plot(X, Y, marker=".", label="Actual", linewidth=3)
   plt.legend()
   plt.savefig("Mpps.png")


def main():
    c = STLClient(verbose_level = 'error')
    c.connect()

    link_speed_bps = c.ports[0].get_speed_bps()
    if link_speed_bps != c.ports[1].get_speed_bps():
        raise Exception("link speed not matched for port 0 and port 1.")

    pkt_sizes = [1518, 1280, 1024, 512, 256, 128, 64]
    # pkt_sizes = [1518, 1280]

    results = {}
    try:
        for pkt_size in pkt_sizes:
            results[pkt_size] = run(c, pkt_size)

    finally:
        c.disconnect()


    Gbpss = []
    Mppss = []
    print("pkt_size", "bps", "pps")
    for pkt_size, result in results.items():
        print(pkt_size, result['bps'], result['pps'])
        Gbpss.append(result['bps'] / 1e9) # Not use 2^N. use 10^N in networking.
        Mppss.append(result['pps'] / 1e6)

    plot_Gbps(pkt_sizes, Gbpss, link_speed_bps)
    plot_Mpps(pkt_sizes, Mppss, link_speed_bps)


if __name__ == '__main__':
    main()
