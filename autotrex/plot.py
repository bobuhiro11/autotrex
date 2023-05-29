import matplotlib.pyplot as plt


def plot_Gbps(packet_sizes, Gbpss, link_speed_bps):
    X = packet_sizes
    Y = Gbpss
    Y_max = []

    # Calc theoretical maximum throuput.
    for pkt_size in packet_sizes:
        # include preameble(8Bytes)+inter frame gap(12Bytes)
        n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8)
        # convert unit from bytes to Gbits.
        Y_max.append(n_pkts * pkt_size * 8 / 1e9)

    print("plot_Gbps:")
    print("packet_size, actual, theoretical")
    for i in range(len(packet_sizes)):
        print(packet_sizes[i], Y[i], Y_max[i], sep=", ")

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
        # include preameble(8Bytes)+inter frame gap(12Bytes)
        n_pkts = link_speed_bps / ((pkt_size + 8 + 12) * 8)
        Y_max.append(n_pkts / 1e6)

    print("plot_Mpps:")
    print("packet_size, actual, theoretical")
    for i in range(len(packet_sizes)):
        print(packet_sizes[i], Y[i], Y_max[i], sep=", ")

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
