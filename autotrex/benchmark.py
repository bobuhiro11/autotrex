#!/usr/bin/env python3
import time
import os
from trex.stl.api import STLProfile, STLClient
from autotrex.plot import plot_Gbps, plot_Mpps

# FIXME: pkt -> eth
# e.g. pkg_size = 64 - 1518


def single_run(c, profile, mult, pkt_size):
    start_at = time.time()

    c.reset(ports=[0, 1])
    c.remove_all_streams()
    c.add_streams(profile.get_streams(), ports=[0, 1])

    c.start(ports=[0],
            mult=str(mult) + "%",
            duration=int(os.getenv("TREX_DURATION", 30)))
    c.wait_on_traffic(ports=[0, 1])
    s = c.get_stats()

    total = s["total"]
    tx_pkts = total["opackets"]
    rx_pkts = total["ipackets"]
    bps = total["tx_bps"]
    pps = total["tx_pps"]

    lossrate = max(0.0, (1 - rx_pkts / tx_pkts)) * 100.0  # percent
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
    profile = STLProfile.load_py("./autotrex/tcp_1pkt.py", pkt_size=pkt_size)

    ok = 1
    ng = 101
    for k in range(7):  # 7 is enough to cover [1-100] mult.
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


def main():
    c = STLClient(verbose_level='error')
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
        # Not use 2^N. use 10^N in networking.
        Gbpss.append(result['bps'] / 1e9)
        Mppss.append(result['pps'] / 1e6)

    plot_Gbps(pkt_sizes, Gbpss, link_speed_bps)
    plot_Mpps(pkt_sizes, Mppss, link_speed_bps)


if __name__ == '__main__':
    main()
