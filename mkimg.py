# language: Python 3, file: mkimg.py
# Terminal хэв маягтай PNG зураг үүсгэх (Menlo monospace, бараан цонх, 2x нягтрал).
import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
SCALE = 2
SIZE = 15 * SCALE
LH = 21 * SCALE
PAD = 22 * SCALE
CHROME = 40 * SCALE
BG = (24, 25, 29)
BAR = (39, 41, 47)
BORDER = (12, 13, 16)
TXT = (208, 212, 216)
CMD = (255, 255, 255)
GREEN = (110, 219, 145)
CYAN = (122, 204, 255)
GREY = (128, 134, 140)
YELLOW = (232, 200, 120)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
PROMPT = "raycharles@macbook-pro lab9_evidence % "


def fnt(index=0):
    return ImageFont.truetype(FONT_PATH, SIZE, index=index)


def wrap(text, max_chars):
    out = []
    for line in text.split("\n"):
        if len(line) <= max_chars:
            out.append(line)
        else:
            while len(line) > max_chars:
                out.append(line[:max_chars])
                line = "    " + line[max_chars:]
            out.append(line)
    return out


def render(name, blocks, title, max_chars=112):
    f, fb = fnt(0), fnt(1)
    cw = f.getlength("M")
    lines = []
    for kind, text in blocks:
        if kind == "cmd":
            lines.append(("cmd", text))
        elif kind == "note":
            for l in wrap(text, max_chars):
                lines.append(("note", l))
        else:
            for l in wrap(text, max_chars):
                lines.append(("out", l))
    longest = max([len(PROMPT) + len(t) if k == "cmd" else len(t) for k, t in lines] + [40])
    width = int(PAD * 2 + cw * longest)
    height = int(CHROME + PAD + LH * len(lines) + PAD)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, width - 1, CHROME], radius=12 * SCALE, fill=BAR)
    d.rectangle([0, CHROME - 14 * SCALE, width - 1, CHROME], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 22 * SCALE + i * 22 * SCALE
        r = 6 * SCALE
        d.ellipse([cx - r, CHROME // 2 - r, cx + r, CHROME // 2 + r], fill=c)
    d.text(((width - f.getlength(title)) / 2, CHROME // 2 - SIZE // 2 - 1), title, font=f,
           fill=(168, 173, 180))
    d.rectangle([0, CHROME, width - 1, height - 1], outline=BORDER, width=2)
    y = CHROME + PAD - 4
    for kind, text in lines:
        if kind == "cmd":
            pw = fb.getlength(PROMPT)
            d.text((PAD, y), PROMPT, font=fb, fill=CYAN)
            d.text((PAD + pw, y), text, font=fb, fill=CMD)
        elif kind == "note":
            d.text((PAD, y), text, font=f, fill=YELLOW)
        else:
            color = GREEN if text.startswith(("summary:", "checksum check")) else TXT
            d.text((PAD, y), text, font=f, fill=color)
        y += LH
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.save(path)
    return path


def read(name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def main():
    made = []
    made.append(render("fig01_ping.png",
                       [("cmd", "ping -c 10 google.com"), ("out", read("01_ping_google.txt"))],
                       "lab9 — ICMP Echo (ping)"))
    made.append(render("fig02_tracert.png",
                       [("cmd", "traceroute -I -q 2 -w 2 -m 16 google.com"),
                        ("out", read("02_tracert_google.txt"))],
                       "lab9 — ICMP TTL / traceroute"))
    made.append(render("fig03_ttl.png",
                       [("cmd", "ping -c 2 -m 1 google.com"),
                        ("out", read("09_ttl1_timeexceeded.txt")),
                        ("note", "# TTL-ийг 1-ээс 7 хүртэл нэмэгдүүлж давтвал:"),
                        ("cmd", "for t in 1 2 3 4 5 6 7; do ping -c 1 -m $t google.com; done"),
                        ("out", read("10_ttl_scan.txt"))],
                       "lab9 — ICMP Time Exceeded (type 11)"))
    made.append(render("fig04_mtu.png",
                       [("note", "# payload 1472 + IP/ICMP 28 = 1500 байт; -D нь DF бит тавина"),
                        ("out", read("08_path_mtu.txt")),
                        ("note", "# 1492 OK, 1493-аас эхлэн хариу байхгүй -> path MTU = 1492")],
                       "lab9 — Path MTU (DF бит) шалгалт"))
    made.append(render("fig05_arp.png",
                       [("cmd", "arp -an"), ("out", read("03_arp_before.txt")),
                        ("cmd", "ping -c 3 192.168.68.1 && arp -n 192.168.68.1"),
                        ("out", read("05_arp_gw.txt")),
                        ("cmd", "ping -c 2 -t 2 192.168.68.250"),
                        ("out", read("06_ping_unused.txt")),
                        ("cmd", "arp -an"), ("out", read("07_arp_after.txt"))],
                       "lab9 — ARP cache (IPv4)"))
    made.append(render("fig06_ndp.png",
                       [("cmd", "ndp -an"), ("out", read("13_ndp.txt"))],
                       "lab9 — IPv6 neighbor discovery (ARP-ийн аналог)"))
    made.append(render("fig07_icmp_probe.png",
                       [("cmd", "python3 icmp_probe.py google.com 4"),
                        ("out", read("11_icmp_probe.txt"))],
                       "lab9 — ICMP header decode (type/code/checksum)"))
    arp_txt = read("12_arp_frame.txt")
    head, _, tail = arp_txt.partition("ARP Reply (gateway -> PC, unicast)")
    made.append(render("fig08_arp_req.png",
                       [("cmd", "python3 arp_frame.py"), ("out", head.rstrip())],
                       "lab9 — ARP Request frame (42 байт)"))
    made.append(render("fig09_arp_rep.png",
                       [("out", "ARP Reply (gateway -> PC, unicast)" + tail)],
                       "lab9 — ARP Reply frame (unicast)"))
    for m in made:
        print(m, Image.open(m).size)


if __name__ == "__main__":
    main()
