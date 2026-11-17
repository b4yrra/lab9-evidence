# language: Python 3, file: arp_frame.py, target: macOS en0
# Бодит интерфейсийн хаягуудаар ARP request / reply frame байгуулж, талбар талбараар нь задална.
import socket, struct, subprocess, re

BROADCAST = "ff:ff:ff:ff:ff:ff"
ZERO_MAC = "00:00:00:00:00:00"


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def local_ip_mac(ifname: str = "en0"):
    out = sh(f"ifconfig {ifname}")
    ip = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", out).group(1)
    mac = re.search(r"ether ([0-9a-f:]{17})", out).group(1)
    return ip, mac


def default_gateway() -> str:
    out = sh("route -n get default")
    return re.search(r"gateway: (\d+\.\d+\.\d+\.\d+)", out).group(1)


def aton(ip: str) -> bytes:
    return socket.inet_aton(ip)


def mac2b(mac: str) -> bytes:
    return bytes(int(x, 16) for x in mac.split(":"))


def b2mac(b: bytes) -> str:
    return ":".join(f"{x:02x}" for x in b)


def arp_table() -> dict:
    table = {}
    for line in sh("arp -an").splitlines():
        m = re.match(r"\? \((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-f:]+|\(incomplete\))", line)
        if m:
            table[m.group(1)] = m.group(2)
    return table


def build_frame(eth_dst, eth_src, op, sha, spa, tha, tpa):
    eth = mac2b(eth_dst) + mac2b(eth_src) + struct.pack("!H", 0x0806)
    arp = struct.pack("!HHBBH", 1, 0x0800, 6, 4, op)
    arp += mac2b(sha) + aton(spa) + mac2b(tha) + aton(tpa)
    return eth + arp


def hexdump(data: bytes, width: int = 16) -> str:
    out = []
    for off in range(0, len(data), width):
        chunk = data[off:off + width]
        hexpart = " ".join(f"{b:02x}" for b in chunk).ljust(width * 3 - 1)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        out.append(f"  {off:04x}  {hexpart}  |{ascii_part}|")
    return "\n".join(out)


def decode(frame: bytes, label: str) -> None:
    eth_dst, eth_src = b2mac(frame[0:6]), b2mac(frame[6:12])
    etype = struct.unpack("!H", frame[12:14])[0]
    htype, ptype, hlen, plen, op = struct.unpack("!HHBBH", frame[14:22])
    sha = b2mac(frame[22:28])
    spa = socket.inet_ntoa(frame[28:32])
    tha = b2mac(frame[32:38])
    tpa = socket.inet_ntoa(frame[38:42])
    print(f"\n{label}")
    print(f"  {'offset':>7} {'field':<20} value")
    print("  " + "-" * 62)
    rows = [
        ("0-5", "Ethernet Dest MAC", eth_dst),
        ("6-11", "Ethernet Src MAC", eth_src),
        ("12-13", "EtherType", f"0x{etype:04x} (ARP)"),
        ("14-15", "ARP Hardware type", f"{htype} (Ethernet)"),
        ("16-17", "ARP Protocol type", f"0x{ptype:04x} (IPv4)"),
        ("18", "Hardware len", f"{hlen} (MAC 6 байт)"),
        ("19", "Protocol len", f"{plen} (IP 4 байт)"),
        ("20-21", "ARP Opcode", f"{op} ({'Request' if op == 1 else 'Reply'})"),
        ("22-27", "Sender MAC", sha),
        ("28-31", "Sender IP", spa),
        ("32-37", "Target MAC", tha),
        ("38-41", "Target IP", tpa),
    ]
    for r in rows:
        print(f"  {r[0]:>7} {r[1]:<20} {r[2]}")
    print(f"  frame урт: {len(frame)} байт (14 Ethernet + 28 ARP)")
    print(hexdump(frame))


if __name__ == "__main__":
    ip, mac = local_ip_mac("en0")
    gw = default_gateway()
    table = arp_table()
    gw_mac = table.get(gw, "(incomplete)")
    print(f"local: en0 {ip} / {mac}")
    print(f"gateway: {gw} / {gw_mac}")
    print(f"arp cache ({len(table)} entries):")
    for k, v in table.items():
        print(f"   {k:<16} -> {v}")

    req = build_frame(BROADCAST, mac, 1, mac, ip, ZERO_MAC, gw)
    decode(req, "ARP Request (PC -> Switch -> broadcast)")

    if gw_mac != "(incomplete)":
        rep = build_frame(mac, gw_mac, 2, gw_mac, gw, mac, ip)
        decode(rep, "ARP Reply (gateway -> PC, unicast)")
    print("\nincomplete entry шалгах: 192.168.68.250 ->", table.get("192.168.68.250", "no entry"))
