import matplotlib.pyplot as plt
import datetime
import os
import csv


def get_prefix():
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    return now + "-" + str(os.getenv('TREX_INPUT_FILE')) + "-"


def plot_Gbps(packet_sizes, Mppss, link_speed_bps):
    prefix = get_prefix()

    X = packet_sizes
    Y = []
    Y_max = []

    # Calc actual throuput.
    for i, pkt_size in enumerate(packet_sizes):
        Mbps = pkt_size * Mppss[i] * 8
        Gbps = Mbps / 1e3
        Y.append(Gbps)

    # Calc theoretical maximum throuput.
    for pkt_size in packet_sizes:
        # include preameble(8Bytes)+inter frame gap(12Bytes)
        n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8)
        # convert unit from bytes to Gbits.
        Y_max.append(n_pkts * pkt_size * 8 / 1e9)

    X = [str(x) for x in list(reversed(X))]
    Y = list(reversed(Y))
    Y_max = list(reversed(Y_max))

    with open(prefix + "Gbps.csv", 'w') as f:
        w = csv.writer(f)
        w.writerow(['Gbps'])
        w.writerow(['packet_size', 'actual', 'theoretical'])
        for i, _ in enumerate(packet_sizes):
            w.writerow([X[i], Y[i], Y_max[i]])

    with open(prefix + "Gbps.csv", 'r') as f:
        print(f.read())

    plt.clf()
    plt.style.use('seaborn-whitegrid')
    plt.xlabel("Packet size (Bytes)")
    plt.ylabel("Throuput (Gbps)")
    plt.ticklabel_format(style='plain')
    plt.plot(X, Y_max, label="Theoretical", color="0.8")
    plt.bar(X, Y, label="Actual", width=0.5)
    plt.legend()
    plt.savefig(prefix + "Gbps.png")


def plot_Mpps(packet_sizes, Mppss, link_speed_bps):
    prefix = get_prefix()

    X = packet_sizes
    Y = Mppss
    Y_max = []

    # Calc theoretical maximum throuput.
    for pkt_size in packet_sizes:
        # include preameble(8Bytes)+inter frame gap(12Bytes)
        n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8)
        Y_max.append(n_pkts / 1e6)

    X = [str(x) for x in list(reversed(X))]
    Y = list(reversed(Y))
    Y_max = list(reversed(Y_max))

    with open(prefix + "Mpps.csv", 'w') as f:
        w = csv.writer(f)
        w.writerow(['Mpps'])
        w.writerow(['packet_size', 'actual', 'theoretical'])
        for i, _ in enumerate(packet_sizes):
            w.writerow([X[i], Y[i], Y_max[i]])

    with open(prefix + "Mpps.csv", 'r') as f:
        print(f.read())

    plt.clf()
    plt.style.use('seaborn-whitegrid')
    plt.xlabel("Packet size (Bytes)")
    plt.ylabel("Packet rate (Mpps)")
    plt.ticklabel_format(style='plain')
    plt.plot(X, Y_max, label="Theoretical", color="0.8")
    plt.bar(X, Y, label="Actual", width=0.5)
    plt.legend()
    plt.savefig(prefix + "Mpps.png")


if __name__ == '__main__':
    pkt_sizes = [1518, 1280, 1024, 512, 256, 128, 64]

    # Example Data.
    Mppss = [
        0.805452,
        0.961957,
        1.050022,
        1.168796,
        1.189449,
        1.214738,
        1.199097,
    ]
    plot_Gbps(pkt_sizes, Mppss, 10*1e9)
    plot_Mpps(pkt_sizes, Mppss, 10*1e9)
