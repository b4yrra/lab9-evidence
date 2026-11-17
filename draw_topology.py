# language: Python 3, file: draw_topology.py
# Зураг 0.5-ийн дагуу туршилтын сүлжээний топологийн диаграм.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1800, 1000
BG = (255, 255, 255)
DEVICE = (222, 235, 247)
DEVICE_EDGE = (70, 120, 180)
LINK = (55, 55, 55)
TXT = (30, 30, 30)
IP = (18, 88, 158)
PORT = (110, 110, 110)

F = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else F, size)


def link(d, p1, p2, port1="", port2=""):
    d.line([p1, p2], fill=LINK, width=3)
    if port1:
        d.text((p1[0] + (p2[0] - p1[0]) * 0.22, p1[1] + (p2[1] - p1[1]) * 0.22 - 15),
               port1, font=font(17), fill=PORT, anchor="ma")
    if port2:
        d.text((p1[0] + (p2[0] - p1[0]) * 0.80, p1[1] + (p2[1] - p1[1]) * 0.80 - 15),
               port2, font=font(17), fill=PORT, anchor="ma")


def pc(d, x, y, label, ip, face="h"):
    w, h = 116, 76
    d.rounded_rectangle([x - w // 2, y - h // 2, x + w // 2, y + h // 2], radius=6,
                        fill=DEVICE, outline=DEVICE_EDGE, width=3)
    d.rectangle([x - w // 2 + 9, y - h // 2 + 8, x + w // 2 - 9, y + h // 2 - 13],
                fill=(249, 251, 254), outline=DEVICE_EDGE, width=2)
    d.line([x - 24, y + h // 2 - 3, x + 24, y + h // 2 - 3], fill=DEVICE_EDGE, width=5)
    d.line([x, y + h // 2 - 3, x, y + h // 2 + 9], fill=DEVICE_EDGE, width=4)
    d.line([x - 28, y + h // 2 + 9, x + 28, y + h // 2 + 9], fill=DEVICE_EDGE, width=4)
    d.text((x, y - h // 2 - 44), label, font=font(20, True), fill=TXT, anchor="ma")
    d.text((x, y + h // 2 + 18), ip, font=font(19), fill=IP, anchor="ma")
    return (x + w // 2, y) if face == "r" else (x - w // 2, y)


def switch(d, x, y, name, subnet):
    w, h = 190, 92
    d.rounded_rectangle([x - w // 2, y - h // 2, x + w // 2, y + h // 2], radius=8,
                        fill=(214, 228, 241), outline=DEVICE_EDGE, width=3)
    for i in range(8):
        d.rectangle([x - w // 2 + 14 + i * 20, y + 12, x - w // 2 + 27 + i * 20, y + 26],
                    fill=(120, 160, 200), outline=DEVICE_EDGE)
    for i in range(3):
        d.polygon([(x - 40 + i * 20, y - 26), (x - 28 + i * 20, y - 14),
                   (x - 40 + i * 20, y - 2)], fill=(70, 120, 180))
    d.text((x, y - h // 2 - 46), name, font=font(20, True), fill=TXT, anchor="ma")
    d.text((x, y + h // 2 + 16), subnet, font=font(19), fill=IP, anchor="ma")


def router(d, x, y, name, p0, p1):
    r = 56
    d.ellipse([x - r, y - r, x + r, y + r], fill=DEVICE, outline=DEVICE_EDGE, width=3)
    d.line([x - 30, y - 13, x + 30, y - 13], fill=DEVICE_EDGE, width=4)
    d.line([x - 30, y + 5, x + 30, y + 5], fill=DEVICE_EDGE, width=4)
    d.polygon([(x + 30, y - 13), (x + 19, y - 21), (x + 19, y - 5)], fill=DEVICE_EDGE)
    d.polygon([(x - 30, y + 5), (x - 19, y + 13), (x - 19, y - 3)], fill=DEVICE_EDGE)
    d.text((x, y - r - 44), name, font=font(20, True), fill=TXT, anchor="ma")
    d.text((x, y + r + 14), p0, font=font(19), fill=IP, anchor="ma")
    d.text((x, y + r + 38), p1, font=font(19), fill=IP, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Туршилтын топологи — ARP / ICMP (Зураг 0.5-ийн дагуу)",
           font=font(26, True), fill=TXT)

    sw0 = (560, 470)
    r0 = (950, 470)
    sw1 = (1330, 470)
    pcs = {0: (200, 210), 1: (200, 400), 2: (200, 590), 3: (200, 780)}
    pc4 = (1660, 660)
    srv = (1660, 280)
    ports = {0: "Fa0/3", 1: "Fa0/4", 2: "Fa0/5", 3: "Fa0/2"}

    # холбооснууд
    for i, (x, y) in pcs.items():
        link(d, (x + 58, y), (sw0[0] - 95, sw0[1]), "Fa0", ports[i])
    link(d, (sw0[0] + 95, sw0[1]), (r0[0] - 56, r0[1]), "Fa0/1", "Gig0/0")
    link(d, (r0[0] + 56, r0[1]), (sw1[0] - 95, sw1[1]), "Gig0/1", "Fa0/1")
    link(d, (sw1[0] + 95, sw1[1]), (pc4[0] - 58, pc4[1]), "Fa0/2", "Fa0")
    link(d, (sw1[0] + 95, sw1[1]), (srv[0] - 58, srv[1]), "Fa0/3", "Fa0")

    for i, (x, y) in pcs.items():
        pc(d, x, y, f"PC{i}", ["192.168.1.3 / 24", "192.168.1.2 / 24",
                               "192.168.1.4 / 24", "192.168.1.5 / 24"][i], face="r")
    pc(d, *pc4, "PC4", "10.0.0.3 / 24", face="l")

    x, y = srv
    d.rounded_rectangle([x - 56, y - 56, x + 56, y + 56], radius=6, fill=(232, 240, 249),
                        outline=DEVICE_EDGE, width=3)
    for i in range(3):
        d.rectangle([x - 38, y - 38 + i * 26, x + 38, y - 22 + i * 26], fill=(210, 226, 242),
                    outline=DEVICE_EDGE, width=2)
    d.text((x, y - 100), "Server0", font=font(20, True), fill=TXT, anchor="ma")
    d.text((x, y + 74), "10.0.0.2 / 24", font=font(19), fill=IP, anchor="ma")

    switch(d, *sw0, "Switch0 (2960-24TT)", "LAN1: 192.168.1.0/24")
    switch(d, *sw1, "Switch1 (2960-24TT)", "LAN2: 10.0.0.0/24")
    router(d, *r0, "Router0 (2911)", "Gig0/0  192.168.1.1 / 24", "Gig0/1  10.0.0.1 / 24")

    d.rectangle([40, H - 96, W - 40, H - 28], outline=(185, 195, 205), width=2)
    d.text((62, H - 84),
           "PC0 -> PC4: IP хаяг өөрчлөгдөхгүй (192.168.1.3 -> 10.0.0.3), MAC хаяг hop бүрт солигдоно:",
           font=font(19), fill=TXT)
    d.text((62, H - 58),
           "PC0 MAC -> Switch0 -> Router0 Gig0/0 MAC | Router0 Gig0/1 MAC -> Switch1 -> PC4 MAC",
           font=font(19), fill=IP)
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "fig00_topology.png")
    img.save(p)
    print(p, img.size)


if __name__ == "__main__":
    main()
