# language: Python 3, file: icmp_probe.py, target: macOS (unprivileged SOCK_DGRAM ICMP)
# ICMP Echo Request илгээж, ирсэн хариултын IP болон ICMP толгойг (type/code/checksum/id/seq) задална.
import socket, struct, time, select, sys

ICMP_ECHO_REQUEST = 8
TYPE_NAME = {
    0: "Echo Reply", 3: "Destination Unreachable", 5: "Redirect",
    8: "Echo Request", 11: "Time Exceeded", 13: "Timestamp Request", 14: "Timestamp Reply",
}
CODE_NAME = {
    (0, 0): "Echo reply", (3, 0): "Net unreachable", (3, 1): "Host unreachable",
    (3, 3): "Port unreachable", (3, 4): "Frag needed, DF set",
    (8, 0): "Echo request", (11, 0): "TTL expired in transit",
    (11, 1): "Fragment reassembly timeout",
}


def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def build_echo_request(seq: int, payload: bytes) -> bytes:
    raw = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, 0x1234, seq) + payload
    return struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum(raw), 0x1234, seq) + payload


def hexdump(data: bytes, width: int = 16) -> str:
    out = []
    for off in range(0, len(data), width):
        chunk = data[off:off + width]
        hexpart = " ".join(f"{b:02x}" for b in chunk).ljust(width * 3 - 1)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        out.append(f"  {off:04x}  {hexpart}  |{ascii_part}|")
    return "\n".join(out)


def probe(host: str, count: int = 4, timeout: float = 2.0) -> None:
    ip = socket.gethostbyname(host)
    print(f"probe -> {host} ({ip})   count={count} timeout={timeout}s")
    print(f"{'seq':>3} {'ttl':>4} {'type':>4} {'code':>4} {'id':>6} {'cksum':>7} {'rtt_ms':>8}  meaning")
    print("-" * 80)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
    sock.setblocking(False)
    rx = 0
    for seq in range(1, count + 1):
        payload = struct.pack("!d", time.time()) + b"VANTA-lab9"
        t0 = time.perf_counter()
        try:
            sock.sendto(build_echo_request(seq, payload), (ip, 0))
        except OSError as e:
            print(f"{seq:>3} {'-':>4} {'-':>4} {'-':>4} {'-':>6} {'-':>7} {'-':>8}  "
                  f"{e.strerror}: ARP reply байхгүй -> EHOSTUNREACH")
            continue
        deadline = t0 + timeout
        got = False
        while time.perf_counter() < deadline:
            r, _, _ = select.select([sock], [], [], max(0.0, deadline - time.perf_counter()))
            if not r:
                break
            data, _ = sock.recvfrom(2048)
            rtt = (time.perf_counter() - t0) * 1000
            # macOS SOCK_DGRAM ICMP нь IP толгойтой буцаана: version/IHL-ээр эхний offset-ыг тодорхойлно
            off = 0
            ttl = 0
            if data and (data[0] >> 4) == 4:
                ihl = (data[0] & 0x0F) * 4
                ttl = data[8]
                off = ihl
            icmp = data[off:off + 8]
            if len(icmp) < 8:
                continue
            typ, code, csum, ident, rseq = struct.unpack("!BBHHH", icmp)
            if rseq != seq:
                continue
            print(f"{rseq:>3} {ttl:>4} {typ:>4} {code:>4} {ident:>6} 0x{csum:04x} {rtt:>8.3f}  "
                  f"{TYPE_NAME.get(typ, '?')} / {CODE_NAME.get((typ, code), '-')}")
            if rx == 0:
                print("  reply bytes (IP + ICMP), first 44 bytes:")
                print(hexdump(data[:44]))
                body = data[off:]
                print(f"  checksum check: ones-complement sum over ICMP message = "
                      f"0x{checksum(body) ^ 0xFFFF:04x}  (0xffff => header + data intact)")
            rx += 1
            got = True
            break
        if not got:
            print(f"{seq:>3} {'-':>4} {'-':>4} {'-':>4} {'-':>6} {'-':>7} {'timeout':>8}  no ICMP reply")
    sock.close()
    print(f"summary: sent={count} received={rx} loss={100 * (count - rx) / count:.0f}%\n")


if __name__ == "__main__":
    probe(sys.argv[1] if len(sys.argv) > 1 else "google.com", 4)
    probe("192.168.68.250", 2, 1.5)
