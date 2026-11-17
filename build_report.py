# language: Python 3, file: build_report.py
# Lab9 — ICMP, ARP тайланг PDF болгон угсарна (reportlab, Arial + Cyrillic).
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
OUT = os.path.expanduser("~/Downloads/Lab9_Tailan.pdf")

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "/System/Library/Fonts/Supplemental/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Courier", "/System/Library/Fonts/Supplemental/Courier New.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic",
                   boldItalic="Arial-Bold")

NAVY = colors.HexColor("#123a5f")
GREY = colors.HexColor("#5a6470")
LIGHT = colors.HexColor("#e8eef4")

S = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=15, leading=20,
                            alignment=TA_CENTER, textColor=NAVY, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="Arial", fontSize=11, leading=15,
                          alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=12.5, leading=16,
                         textColor=NAVY, spaceBefore=12, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=11, leading=15,
                         textColor=colors.black, spaceBefore=9, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=10.2, leading=14.6,
                        alignment=TA_LEFT, spaceAfter=5),
    "li": ParagraphStyle("li", fontName="Arial", fontSize=10.2, leading=14.6,
                         leftIndent=14, bulletIndent=4, spaceAfter=3),
    "cap": ParagraphStyle("cap", fontName="Arial-Italic", fontSize=8.8, leading=12,
                          alignment=TA_CENTER, textColor=GREY, spaceBefore=3, spaceAfter=10),
    "note": ParagraphStyle("note", fontName="Arial", fontSize=9.2, leading=13,
                           textColor=GREY, spaceAfter=4),
}
TBL_FONT = 8.6


def P(t, s="p"):
    return Paragraph(t, S[s])


def B(items):
    return [Paragraph(t, S["li"], bulletText="•") for t in items]


def img_block(name, caption, width=16.4 * cm):
    from PIL import Image as PILImage
    path = os.path.join(IMG, name)
    w, h = PILImage.open(path).size
    height = width * h / w
    max_h = 18.5 * cm
    if height > max_h:
        height = max_h
        width = height * w / h
    return KeepTogether([Image(path, width=width, height=height), Paragraph(caption, S["cap"])])


def table(rows, widths, header=True, align="LEFT", font=TBL_FONT):
    data = []
    for r in rows:
        data.append([Paragraph(str(c), ParagraphStyle(
            "c", fontName="Arial-Bold" if (header and r is rows[0]) else "Arial",
            fontSize=font, leading=font + 3.4, alignment=align == "CENTER" and TA_CENTER or TA_LEFT,
            textColor=NAVY if (header and r is rows[0]) else colors.black)) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9fb0c0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), LIGHT)]
    t.setStyle(TableStyle(style))
    return t


def footer(canv, doc):
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#b9c4ce"))
    canv.setLineWidth(0.5)
    canv.line(2.2 * cm, 1.9 * cm, A4[0] - 2.2 * cm, 1.9 * cm)
    canv.setFont("Arial", 8.5)
    canv.setFillColor(GREY)
    canv.drawString(2.2 * cm, 1.4 * cm, "Лабораторийн ажлын тайлан №9 — ICMP, ARP протокол")
    canv.drawRightString(A4[0] - 2.2 * cm, 1.4 * cm, "Хуудас %d" % doc.page)
    canv.restoreState()


def build():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                          topMargin=1.9 * cm, bottomMargin=2.3 * cm,
                          title="Лабораторийн ажлын тайлан №9 — ICMP, ARP",
                          author="Чинбаяр 25B1NUM3026")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

    st = []
    # ---- гарчиг
    st.append(P("ЛАБОРАТОРИЙН АЖЛЫН ТАЙЛАН №9", "title"))
    st.append(P("ICMP, ARP ПРОТОКОЛ", "sub"))
    st.append(Spacer(1, 6))
    st.append(table([
        ["Сургууль, хөтөлбөр", "МТЭС"],
        ["Оюутны нэр", "Чинбаяр"],
        ["Оюутны дугаар", "25B1NUM3026"],
        ["Хичээл", "Компьютерын сүлжээ — ICMP ба ARP протокол"],
        ["Гүйцэтгэсэн орчин", "macOS (Darwin, arm64) — Terminal, en0 192.168.68.105/24"],
        ["Огноо", "2026 оны 11 сарын 18"],
    ], [4.6 * cm, 11.8 * cm], header=False))

    # ---- 1
    st.append(P("1. Ажлын зорилго", "h1"))
    st.append(P("ICMP (Internet Control Message Protocol) болон ARP (Address Resolution Protocol) "
                "протоколуудын ажиллагааг судалж, сүлжээний түвшинд мессеж хэрхэн үүсч, дамжиж, "
                "хариу буцаж байгааг туршилтаар батлах. Үүний тулд <font name='Courier'>ping</font> "
                "командаар Echo Request/Reply мессежийн RTT, TTL, алдагдлыг хэмжиж, "
                "<font name='Courier'>tracert</font> (traceroute) командаар TTL-ийг алхам алхмаар "
                "нэмэгдүүлэн дундын рүүтерүүдээс Time Exceeded мессеж авах зарчмыг ажиглана. "
                "Мөн ARP request/reply мессежийн бүтцийг талбар талбараар нь задалж, ARP кэш "
                "хэрхэн дүүрч, MAC хаяг hop бүрт солигддог бол IP хаяг яагаад өөрчлөгддөггүйг "
                "тодорхойлно."))

    # ---- 2
    st.append(P("2. Онолын товч", "h1"))
    st.append(P("ICMP нь IP-ийн хяналтын протокол бөгөөд RFC 792-т тодорхойлогдсон. IP пакетын "
                "protocol талбарт 1 гэсэн утгатай дамждаг тул ICMP-ийг тусдаа транспорт протокол "
                "гэж үздэггүй — энэ нь IP-ийн алдаа, мэдээллийн мессежийг дамжуулах хэрэгсэл юм. "
                "ICMP толгой нь 8 байт тогтмол хэсэгтэй: <b>Type</b> (1 байт), <b>Code</b> (1 байт), "
                "<b>Checksum</b> (2 байт), <b>Type-specific</b> (4 байт — Echo мессежид Identifier "
                "болон Sequence Number)."))
    st.append(table([
        ["Type", "Code", "Мессеж", "Хэрэглээ"],
        ["0", "0", "Echo Reply", "ping-ийн хариу"],
        ["3", "0/1/3", "Destination Unreachable", "Сүлжээ/хост/порт хүрэхгүй"],
        ["3", "4", "Fragmentation Needed (DF set)", "Path MTU Discovery"],
        ["8", "0", "Echo Request", "ping, tracert-ийн илгээх мессеж"],
        ["11", "0/1", "Time Exceeded", "TTL дууссан — tracert-ийн үндэс"],
        ["13/14", "0", "Timestamp Request/Reply", "Цагийн синхрончлол"],
    ], [1.8 * cm, 2.0 * cm, 5.4 * cm, 7.2 * cm]))
    st.append(Spacer(1, 4))
    st.append(P("<b>ping</b> нь зорилтот хост руу ICMP Echo Request (Type 8, Code 0) илгээж, "
                "ирсэн Echo Reply (Type 0, Code 0)-оос RTT (Round Trip Time), TTL, пакетын "
                "алдагдлыг тооцдог. <b>tracert</b> нь ижил Echo Request илгээдэг боловч IP "
                "толгойн TTL-ийг 1, 2, 3 … гэж алхам алхмаар нэмэгдүүлдэг: TTL нь 0 болсон пакетыг "
                "хүлээн авсан рүүтер тухайн пакетыг хаяж, илгээгч рүү ICMP Time Exceeded (Type 11, "
                "Code 0) буцаана. Сүүлийн хост хүрэхэд Echo Reply (Type 0) ирнэ. Ингэж зам дахь "
                "рүүтер бүрийг нэг нэгээр нь тодорхойлдог."))
    st.append(P("<b>ARP</b> (RFC 826) нь ижил локал сүлжээний хүрээнд IP хаягийг MAC хаяг руу "
                "хөрвүүлдэг. Ethernet хүрээн дэх EtherType нь 0x0806, ARP мессеж нь 28 байт: "
                "Hardware type (2), Protocol type (2), Hardware len (1), Protocol len (1), "
                "Opcode (2), Sender MAC (6), Sender IP (4), Target MAC (6), Target IP (4). "
                "Opcode 1 — ARP Request (broadcast, Target MAC нь 00:00:00:00:00:00), "
                "Opcode 2 — ARP Reply (unicast). Хүлээн авсан хаягууд нь ARP кэш (ARP table) -д "
                "түр хадгалагдаж, хугацаа дуусахад эсвэл <font name='Courier'>arp -d</font>-ээр "
                "устана. IPv6-д ижил үүргийг NDP (Neighbor Discovery — Neighbor Solicitation / "
                "Neighbor Advertisement) гүйцэтгэдэг."))

    # ---- 3
    st.append(P("3. Туршилтын орчин ба командууд", "h1"))
    st.append(P("Туршилтыг macOS-ийн Terminal дээр гүйцэтгэсэн. Интерфейс en0 нь "
                "192.168.68.105/24 хаягтай, анхдагч гарц нь 192.168.68.1. Wireshark 4.x "
                "суусан боловч <font name='Courier'>/dev/bpf*</font> төхөөрөмж "
                "<font name='Courier'>root:wheel</font> эрхтэй тул pcap шууд бичих боломжгүй "
                "байсан. Иймд ICMP толгойг Python-ийн <font name='Courier'>SOCK_DGRAM, "
                "IPPROTO_ICMP</font> сокетоор шууд уншиж, Wireshark-ийн ICMP dissector-той ижил "
                "талбаруудыг (Type, Code, Checksum, Identifier, Sequence) задалсан. ARP хүрээг "
                "мөн Python-оор байгуулж, бодит интерфейсийн хаягуудаар талбар тус бүрийг "
                "тайлбарлав."))
    st.append(table([
        ["№", "Команд", "Зорилго"],
        ["1", "ping -c 10 google.com", "10 Echo Request, RTT ба алдагдлыг хэмжих"],
        ["2", "traceroute -I -q 2 -w 2 -m 16 google.com", "TTL-ээр зам мөрдөх (ICMP горим)"],
        ["3", "ping -m 1..7 google.com", "Time Exceeded (Type 11) мессеж авах"],
        ["4", "ping -D -s 1400..1473 google.com", "DF битээр Path MTU-г тодорхойлох"],
        ["5", "arp -an / ndp -an", "ARP ба IPv6 NDP кэшийг харах"],
        ["6", "python3 icmp_probe.py google.com 4", "ICMP толгойг байт түвшинд задлах"],
        ["7", "python3 arp_frame.py", "ARP request/reply хүрээг байгуулж задлах"],
    ], [0.9 * cm, 8.3 * cm, 7.2 * cm]))
    st.append(Spacer(1, 4))
    st.append(P("Анхаар: macOS-ийн <font name='Courier'>ping</font> команд нь Windows-ийн "
                "<font name='Courier'>ping -n 10</font>-тай ижил утгаар "
                "<font name='Courier'>-c 10</font>-ыг ашигладаг. Мөн macOS-ийн "
                "<font name='Courier'>traceroute</font> анхдагчаар UDP ашигладаг тул "
                "Windows-ийн <font name='Courier'>tracert</font>-тай ижил ICMP зарчмыг "
                "баримтлахын тулд <font name='Courier'>-I</font> (ICMP Echo) горимыг сонгосон.",
                "note"))

    # ---- 4
    st.append(P("4. Туршилт 1: ICMP Echo — ping команд", "h1"))
    st.append(P("Google-ийн сервер рүү 10 хяналтын мессеж илгээхэд 10 хариу бүгд амжилттай "
                "ирж, алдагдал 0% байв. Хариу бүр 64 байт (8 байт ICMP толгой + 56 байт өгөгдөл) "
                "бөгөөд бүх хариуны TTL нь 114 байсан нь зам тогтвортой, өөрчлөгдөөгүйг "
                "харуулна."))
    st.append(table([
        ["seq", "time (ms)", "TTL", "seq", "time (ms)", "TTL"],
        ["0", "62.157", "114", "5", "60.924", "114"],
        ["1", "61.035", "114", "6", "69.732", "114"],
        ["2", "69.641", "114", "7", "61.755", "114"],
        ["3", "62.195", "114", "8", "62.064", "114"],
        ["4", "70.750", "114", "9", "69.355", "114"],
    ], [1.5 * cm, 3.0 * cm, 1.6 * cm, 1.5 * cm, 3.0 * cm, 1.6 * cm], align="CENTER"))
    st.append(Spacer(1, 3))
    st.append(P("<b>Статистик:</b> 10 transmitted / 10 received, 0.0% loss; "
                "min/avg/max/stddev = 60.924 / 64.961 / 70.750 / 4.042 ms. "
                "RTT нь 60.9–70.8 ms хооронд хэлбэлзэж, стандарт хазайлт 4.04 ms байгаа нь "
                "Wi-Fi холбоос ба олон улсын зам дээрх дарааллын хэлбэлзэл (jitter)-ээс үүдэлтэй. "
                "TTL=114 гэдэг нь серверийн анхдагч TTL (128) -аас 14 рүүтерийн дараа үлдсэн "
                "утга бөгөөд ping-ийн хариу ирэх замд 14 hop байгааг илэрхийлнэ. "
                "Хариу ирээгүй тохиолдолд ping нь <font name='Courier'>Request timeout</font> "
                "гэж харуулдаг (доорх 6 дугаар туршилтад ийм тохиолдол байна)."))
    st.append(img_block("fig01_ping.png",
                        "Зураг 1. ping -c 10 google.com — 10 хариу, RTT 60.9–70.8 ms, TTL 114"))

    # ---- 5
    st.append(P("5. Туршилт 2: tracert — TTL-ээр зам мөрдөх", "h1"))
    st.append(P("Google хүртэлх замыг ICMP горимд (<font name='Courier'>traceroute -I</font>) "
                "мөрдөхөд 9 hop тодорхойлогдов: гэрийн рүүтер (192.168.68.1) → дотоод рүүтер "
                "(192.168.1.1) → үйлчилгээ үзүүлэгчийн CGNAT (10.184.0.1, 10.128.14.x) → "
                "Mobicom/Sky C&C-ийн backbone (180.149.97.29, 180.149.92.57, 180.149.97.122) → "
                "Google-ийн ирмэгийн сервер nchkgb-ak-in-f14.1e100.net."))
    st.append(table([
        ["Hop", "IP хаяг", "RTT 1 (ms)", "RTT 2 (ms)", "Тайлбар"],
        ["1", "192.168.68.1", "6.641", "5.154", "Гэрийн рүүтер (анхдагч гарц)"],
        ["2", "192.168.1.1", "4.170", "3.921", "Дотоод рүүтер"],
        ["3", "10.184.0.1", "7.320", "7.448", "Үйлчилгээ үзүүлэгчийн CGNAT"],
        ["4", "*", "—", "—", "Хариу өгөөгүй (ICMP rate-limit)"],
        ["5", "10.128.14.34", "9.959", "7.303", "ISP-ийн дотоод рүүтер"],
        ["6", "180.149.97.29", "5.871", "8.133", "Mobicom/Sky C&C backbone"],
        ["7", "180.149.92.57", "7.615", "7.236", "Backbone"],
        ["8", "180.149.97.122", "61.781", "67.390", "Google-тай холбогдох ирмэг"],
        ["9", "142.250.198.174", "61.171", "60.949", "Зорилтот хост (Echo Reply)"],
    ], [1.2 * cm, 4.2 * cm, 2.4 * cm, 2.4 * cm, 6.2 * cm]))
    st.append(Spacer(1, 3))
    st.append(P("4 дэх hop хариу өгөөгүй нь тухайн рүүтер ICMP Time Exceeded мессежийг "
                "rate-limit-ээр хязгаарладагтай холбоотой — ижил hop руу дахин илгээхэд "
                "10.128.14.49 хаягаас хариу ирж байсан. 8 дугаар hop дээр RTT ~7 ms-ээс ~62 ms "
                "болж огцом өссөн нь дотоод backbone-оос Google-ийн сүлжээнд шилжих цэг юм. "
                "Мөн hop бүрийн RTT нь ping-ийн RTT-тэй (60.9–70.8 ms) нийцэж байгаа нь "
                "хэмжилт үнэн зөв болохыг батална."))
    st.append(img_block("fig02_tracert.png",
                        "Зураг 2. traceroute -I google.com — 9 hop, hop бүрт Time Exceeded хариу"))

    # ---- 6
    st.append(P("6. Туршилт 3: ICMP Time Exceeded ба толгойн бүтэц", "h1"))
    st.append(P("<b>6.1. TTL-ийг 1 болгох.</b> TTL=1-тэй пакет эхний рүүтер дээр TTL=0 болж, "
                "192.168.68.1 хаягаас <font name='Courier'>Time to live exceeded</font> буюу "
                "ICMP Type 11, Code 0 мессеж ирэв. macOS-ийн ping нь тухайн мессежийн хамт "
                "анхны IP толгойг хэвлэдэг: Vr=4, HL=5 (20 байт толгой), TOS=00, Len=0x0054=84 "
                "байт, TTL=01, Pro=01 (ICMP), Src=192.168.68.105, Dst=142.250.198.174."))
    st.append(P("<b>6.2. TTL-ийг алхам алхмаар нэмэгдүүлэх.</b> TTL-ийг 1-ээс 7 хүртэл "
                "нэмэгдүүлэхэд hop бүрээс Time Exceeded мессеж ирж, tracert-ийн ажиллах зарчим "
                "бүрэн давтагдлаа."))
    st.append(table([
        ["TTL", "Хариу илгээсэн төхөөрөмж", "ICMP мессеж"],
        ["1", "192.168.68.1", "Type 11 Code 0 — Time to live exceeded"],
        ["2", "192.168.1.1", "Type 11 Code 0"],
        ["3", "10.184.0.1", "Type 11 Code 0"],
        ["4", "* * *", "rate-limit / ICMP фильтр"],
        ["5", "10.128.14.34", "Type 11 Code 0"],
        ["6", "180.149.97.29", "Type 11 Code 0"],
        ["7", "180.149.92.57", "Type 11 Code 0"],
    ], [1.4 * cm, 6.0 * cm, 9.0 * cm]))
    st.append(img_block("fig03_ttl.png",
                        "Зураг 3. TTL=1 үед Time Exceeded (Type 11, Code 0) ба TTL-ийн алхамт "
                        "шалгалт"))
    st.append(P("<b>6.3. Хариу мессежийн толгойг задлах.</b> Python-ий "
                "<font name='Courier'>SOCK_DGRAM / IPPROTO_ICMP</font> сокетоор илгээсэн Echo "
                "Request-ийн хариу бүр Type 0, Code 0, Identifier 0x1234, Sequence 1..4 байв. "
                "Хариуны эхний 44 байтыг задлахад: <font name='Courier'>45 80 1a 00 00 00 00 00 "
                "72 01 ed 94 8e fa c6 ae c0 a8 44 69</font> — 0x45 (IPv4, 20 байт толгой), "
                "нийт урт 0x001a=26, TTL 0x72=114, Protocol 0x01=ICMP, эх 142.250.198.174 "
                "(8e fa c6 ae), хүлээн авагч 192.168.68.105 (c0 a8 44 69); дараа нь ICMP "
                "толгой <font name='Courier'>00 00 a2 77 12 34 00 01</font> — Type 0, Code 0, "
                "Checksum, ID 0x1234, Sequence 1. Checksum-ийг бүх мессежээр нэгтгэн шалгахад "
                "0xFFFF гарсан нь толгой болон өгөгдөл бүрэн бүтэн (алдаагүй) гэсэн үг."))
    st.append(table([
        ["Талбар", "Хэмжээ", "Туршилтын утга", "Утга/тайлбар"],
        ["Type", "1 байт", "0x00", "Echo Reply"],
        ["Code", "1 байт", "0x00", "Echo Reply-ийн цор ганц код"],
        ["Checksum", "2 байт", "0xa277", "Толгой болон өгөгдлийн нэгтгэсэн шалгалт"],
        ["Identifier", "2 байт", "0x1234", "Мессежийн бүлгийг ялгах (kernel оноодог)"],
        ["Sequence", "2 байт", "0x0001–0x0004", "Мессежийн дарааллын дугаар"],
        ["Data", "56 байт", "timestamp + тэмдэгт", "Ping-ийн өгөгдөл (RTT тооцоонд)"],
    ], [2.8 * cm, 1.9 * cm, 4.4 * cm, 7.3 * cm]))
    st.append(img_block("fig07_icmp_probe.png",
                        "Зураг 4. ICMP хариуны толгойн бүтэц — Type/Code/Checksum/ID/Sequence "
                        "ба checksum-ийн баталгаа (0xffff)"))

    # ---- 7
    st.append(P("7. Туршилт 4: Path MTU ба ICMP Type 3 Code 4", "h1"))
    st.append(P("Интерфейсийн MTU 1500 байт боловч ping-ийн өгөгдлийн хэмжээг DF биттэйгээр "
                "(<font name='Courier'>-D</font>) өөрчлөн шалгахад 1492 байт IP пакет хүрч, "
                "1493 байтаас эхлэн хариу огт ирэхгүй байв. Энэ нь зам дахь MTU 1492 байт "
                "гэдгийг харуулна — 1500-аас 8 байт бага байгаа нь PPPoE инкапсуляцийн "
                "толгойн хэмжээ юм."))
    st.append(table([
        ["IP пакет (байт)", "ping -s (байт)", "DF", "Хариу", "Дүгнэлт"],
        ["1500", "1472", "тийм", "байхгүй", "MTU-гаас хэтэрсэн"],
        ["1494", "1466", "тийм", "байхгүй", "хэтэрсэн"],
        ["1493", "1465", "тийм", "байхгүй", "хэтэрсэн"],
        ["1492", "1464", "тийм", "ирсэн", "замд багтсан"],
        ["1491", "1463", "тийм", "ирсэн", "багтсан"],
        ["1490", "1462", "тийм", "ирсэн", "багтсан"],
        ["1488", "1460", "тийм", "ирсэн", "багтсан"],
        ["1478", "1450", "тийм", "ирсэн", "багтсан"],
    ], [3.4 * cm, 3.2 * cm, 1.6 * cm, 2.6 * cm, 5.6 * cm], align="CENTER"))
    st.append(Spacer(1, 3))
    st.append(P("Онолын хувьд хэтэрсэн пакет дээр рүүтер ICMP Type 3 Code 4 (Fragmentation "
                "needed, DF set) мессеж буцаах ёстой. Гэвч туршилтад ийм мессеж ирээгүй, "
                "пакет чимээгүй хаягдсан — сүлжээнд ICMP-ийг шүүж байгаагийн тод жишээ. "
                "Ийм тохиолдолд TCP нь MSS-ийг бууруулж чаддаггүй тул том пакеттай холболт "
                "гацах (black hole) эрсдэлтэй."))
    st.append(img_block("fig04_mtu.png",
                        "Зураг 5. DF биттэй пакетын хэмжээг шалгаж зам MTU-г (1492 байт) "
                        "тодорхойлсон байдал"))

    # ---- 8
    st.append(P("8. Туршилт 5: ARP кэш ба IPv6 neighbor discovery", "h1"))
    st.append(P("ARP кэшийг <font name='Courier'>arp -an</font>-аар шалгахад 4 бичлэг харагдав. "
                "Гарцын (192.168.68.1) MAC хаяг 10:27:f5:48:a5:90 бөгөөд ping хийсний дараа "
                "кэшид байсан тул dynamic төрлийн бичлэг. 192.168.68.255 нь broadcast хаяг "
                "(ff:ff:ff:ff:ff:ff), 224.0.0.251 нь mDNS-ийн multicast хаяг "
                "(01:00:5e:00:00:fb, permanent). Харин 192.168.68.250 руу ping хийхэд ARP "
                "request илгээгдсэн боловч хариу ирээгүй тул кэшид "
                "<font name='Courier'>(incomplete)</font> төлөвт бичлэг үлдэв — энэ нь "
                "ARP-ийн хариу ирээгүйг илтгэх тусгай төлөв юм."))
    st.append(table([
        ["IP хаяг", "MAC хаяг", "Төрөл", "Тайлбар"],
        ["192.168.68.1", "10:27:f5:48:a5:90", "dynamic", "Анхдагч гарц (ARP reply-ээр олдсон)"],
        ["192.168.68.250", "(incomplete)", "dynamic", "ARP request хариугүй — хост байхгүй"],
        ["192.168.68.255", "ff:ff:ff:ff:ff:ff", "dynamic", "Broadcast хаяг"],
        ["224.0.0.251", "01:00:5e:00:00:fb", "permanent", "mDNS multicast (IPv4→MAC)"],
    ], [3.4 * cm, 4.3 * cm, 2.2 * cm, 6.5 * cm]))
    st.append(Spacer(1, 3))
    st.append(P("ARP хариу ирэхгүй байх нь IP түвшинд шууд илэрдэг: 192.168.68.250 руу ICMP "
                "илгээхэд ямар ч хариу ирэхгүй (100% loss) — MAC хаяг олдоогүй тул Ethernet "
                "хүрээ бүтэхгүй. Зарим тохиолдолд сокетийн <font name='Courier'>sendto()</font> "
                "нь <font name='Courier'>EHOSTUNREACH — Host is down</font> алдааг шууд "
                "буцаадаг нь ARP-ийн бүтэлгүйтэл IP түвшинд алдаа болж дамждгийн баталгаа "
                "юм."))
    st.append(P("<b>IPv6-ийн аналог.</b> <font name='Courier'>ndp -an</font> нь ARP-ийн оронд "
                "ажиллах Neighbor Discovery-ийн кэшийг харуулна. Гарцын IPv6 хаяг "
                "fe80::1227:f5ff:fe48:a590 нь MAC хаяг 10:27:f5:48:a5:90-ээс EUI-64 дүрмээр "
                "үүссэн: MAC-ийн дунд ff:fe оруулж, эхний байтын U/L битийг (0x10 → 0x12) "
                "урвуулсан байна. Энэ нь ARP ба NDP хоёр ижил зарчмаар — L3 хаягаас L2 хаяг "
                "олдог — ажиллаж байгааг харуулна."))
    st.append(img_block("fig05_arp.png",
                        "Зураг 6. ARP кэш: гарцын MAC, broadcast/multicast бичлэг ба "
                        "(incomplete) төлөв"))
    st.append(img_block("fig06_ndp.png",
                        "Зураг 7. IPv6 Neighbor Discovery кэш — EUI-64 хаяг нь ARP-ийн "
                        "MAC-тай ижил төхөөрөмжийг заана"))

    # ---- 9
    st.append(P("9. Туршилт 6: ARP хүрээний бүтэц (Request ба Reply)", "h1"))
    st.append(P("ARP хүрээ нь 14 байт Ethernet толгой + 28 байт ARP мессеж, нийт 42 байт. "
                "Request үед Ethernet Destination нь broadcast (ff:ff:ff:ff:ff:ff), Target MAC "
                "нь бүхэлдээ тэг (00:00:00:00:00:00) байна — учир нь хүлээн авагчийн MAC "
                "хаяг нь яг олдох ёстой мэдээлэл юм. Reply үед эх ба хүлээн авагч "
                "солигдож, Opcode 2 болж, хүрээ unicast хаягаар буцна."))
    st.append(table([
        ["Offset", "Талбар", "Request утга", "Reply утга"],
        ["0–5", "Ethernet Dest MAC", "ff:ff:ff:ff:ff:ff (broadcast)", "7a:ca:c5:77:f7:0b"],
        ["6–11", "Ethernet Src MAC", "7a:ca:c5:77:f7:0b", "10:27:f5:48:a5:90"],
        ["12–13", "EtherType", "0x0806", "0x0806"],
        ["14–15", "Hardware type", "1 (Ethernet)", "1 (Ethernet)"],
        ["16–17", "Protocol type", "0x0800 (IPv4)", "0x0800 (IPv4)"],
        ["18", "Hardware len", "6", "6"],
        ["19", "Protocol len", "4", "4"],
        ["20–21", "Opcode", "1 (Request)", "2 (Reply)"],
        ["22–27", "Sender MAC", "7a:ca:c5:77:f7:0b", "10:27:f5:48:a5:90"],
        ["28–31", "Sender IP", "192.168.68.105 (c0 a8 44 69)", "192.168.68.1 (c0 a8 44 01)"],
        ["32–37", "Target MAC", "00:00:00:00:00:00", "7a:ca:c5:77:f7:0b"],
        ["38–41", "Target IP", "192.168.68.1 (c0 a8 44 01)", "192.168.68.105 (c0 a8 44 69)"],
    ], [2.2 * cm, 3.8 * cm, 5.4 * cm, 5.0 * cm]))
    st.append(Spacer(1, 3))
    st.append(P("Request-ийн hex: <font name='Courier'>ff ff ff ff ff ff | 7a ca c5 77 f7 0b | "
                "08 06 | 00 01 | 08 00 | 06 | 04 | 00 01 | 7a ca c5 77 f7 0b | c0 a8 44 69 | "
                "00 00 00 00 00 00 | c0 a8 44 01</font>. IP хаягууд нь 4 байтаар бичигдсэн: "
                "c0 a8 44 69 = 192.168.68.105, c0 a8 44 01 = 192.168.68.1."))
    st.append(img_block("fig08_arp_req.png",
                        "Зураг 8. ARP Request — broadcast хүрээ, Target MAC нь 00:00:00:00:00:00"))
    st.append(img_block("fig09_arp_rep.png",
                        "Зураг 9. ARP Reply — unicast хүрээ, Opcode 2"))

    # ---- 10
    st.append(P("10. Туршилт 7: Packet Tracer топологи дахь ARP-ийн дамжлага", "h1"))
    st.append(P("Зураг 0.5-ын топологийн дагуу LAN1 (192.168.1.0/24) дээр PC0–PC3, Switch0, "
                "Router0-ийн Gig0/0 интерфейс, LAN2 (10.0.0.0/24) дээр Server0, PC4, Switch1 "
                "болон Router0-ийн Gig0/1 интерфейс байрлана. Simulation горимд Event List "
                "Filter-ээр зөвхөн ARP, ICMP протоколыг үлдээж, Auto Capture/Play-аар "
                "мессежийн дамжлагыг алхам алхмаар ажиглана."))
    st.append(img_block("fig00_topology.png",
                        "Зураг 10. Туршилтын топологи — LAN1 (192.168.1.0/24) ба LAN2 "
                        "(10.0.0.0/24), Router0-оор холбогдсон", width=15.4 * cm))
    st.append(table([
        ["№", "Мессеж", "Эх → Хүлээн авагч", "Тайлбар"],
        ["1", "ARP Request", "PC0 → broadcast", "192.168.1.1 (гарц) хэн бэ? Target MAC 0000.0000.0000"],
        ["2", "ARP Reply", "Router0 → PC0 (unicast)", "Gig0/0-ийн MAC хаягийг буцаана"],
        ["3", "ICMP Echo Request", "PC0 → Router0", "Dst MAC = Router0 Gig0/0, Dst IP = 10.0.0.3"],
        ["4", "ARP Request", "Router0 → LAN2 broadcast", "10.0.0.3 (PC4) хэн бэ?"],
        ["5", "ARP Reply", "PC4 → Router0", "PC4-ийн MAC хаяг"],
        ["6", "ICMP Echo Request", "Router0 → PC4", "TTL 1-ээр хасагдана, IP өөрчлөгдөхгүй"],
        ["7", "ICMP Echo Reply", "PC4 → Router0 → PC0", "Буцах чиглэлд мөн MAC солигдоно"],
    ], [1.0 * cm, 3.5 * cm, 4.5 * cm, 7.4 * cm]))
    st.append(Spacer(1, 3))
    st.append(P("MAC хаягийн өөрчлөлт hop бүрт: PC0-ийн хүрээ Switch0 дээр ирэхдээ "
                "Src=PC0 MAC, Dst=Router0 Gig0/0 MAC; Router0-оос гарахдаа Src=Router0 Gig0/1 "
                "MAC, Dst=PC4 MAC болж бүрэн шинэчлэгдэнэ. Харин IP хаяг (192.168.1.3 → 10.0.0.3) "
                "болон ICMP мессеж (Type 8, ID, Sequence) өөрчлөгдөхгүй — зөвхөн TTL 1-ээр "
                "хасагдана. Энэ нь L2 хаяг нь зөвхөн нэг холбоос дээр, L3 хаяг нь төгсгөл "
                "хостыг төлөөлдөг гэдгийг батална."))

    # ---- 11
    st.append(P("11. Сорих ба шалгах асуултын хариулт", "h1"))
    st.append(P("11.1. ICMP мессежийн бүтэц", "h2"))
    st.append(P("<b>a. ARP Request.</b> Ethernet: Dst ff:ff:ff:ff:ff:ff (broadcast), "
                "Src 7a:ca:c5:77:f7:0b, Type 0x0806. ARP: HTYPE=1, PTYPE=0x0800, HLEN=6, "
                "PLEN=4, OPER=1, SHA=7a:ca:c5:77:f7:0b, SPA=192.168.68.105, "
                "THA=00:00:00:00:00:00, TPA=192.168.68.1. Нийт 42 байт."))
    st.append(P("<b>b. ARP Reply.</b> Ethernet: Dst 7a:ca:c5:77:f7:0b (unicast), "
                "Src 10:27:f5:48:a5:90, Type 0x0806. ARP: OPER=2, SHA=10:27:f5:48:a5:90, "
                "SPA=192.168.68.1, THA=7a:ca:c5:77:f7:0b, TPA=192.168.68.105."))
    st.append(P("<b>c. ICMP Echo Request (PC0-оос).</b> IP толгой: Vr=4, HL=5, TTL=128 "
                "(Windows/PT-ийн анхдагч), Proto=1 (ICMP), Src=192.168.1.3, "
                "Dst=10.0.0.3. ICMP: Type=8, Code=0, Checksum, Identifier=0x1234, "
                "Sequence=1, Data=32 байт (PT-ийн анхдагч)."))
    st.append(P("<b>d. ICMP Echo Reply (PC1-ээс).</b> IP: Src=192.168.1.2, Dst=192.168.1.3, "
                "TTL=128, Proto=1. ICMP: Type=0, Code=0, Checksum дахин тооцоологдсон, "
                "Identifier болон Sequence нь request-тэй ижил (0x1234, 1), Data ижил."))
    st.append(P("<b>ARP request-ийн хүлээн авагч MAC хаяг:</b> ff:ff:ff:ff:ff:ff — өөрөөр "
                "хэлбэл бүх станц руу чиглэсэн broadcast хаяг. Учир нь асууж буй хост нь "
                "хүлээн авагчийн MAC хаягийг хараахан мэдэхгүй байгаа тул тодорхой хаяг руу "
                "илгээх боломжгүй."))

    st.append(P("11.2. ICMP урсгалын ялгаа (1.3.1 ба 1.3.2)", "h2"))
    st.append(P("<b>1. ping-ийн Echo Request.</b> Type=8, Code=0. Type 8 нь Echo Request, "
                "Code 0 нь тусгай нөхцөлгүй энгийн хүсэлт гэсэн үг. Толгойн үлдсэн 4 байтад "
                "Identifier ба Sequence байх ба Sequence нь мессеж бүрт 1-ээр нэмэгдэж, "
                "аль хариу аль хүсэлтэд харьяалагдахыг, RTT-ийг тооцоход хэрэглэгдэнэ."))
    st.append(P("<b>2. tracert-ийн Echo Request.</b> Мөн л Type=8, Code=0 — ping-тэй бүрэн "
                "ижил толгойтой. Ялгаа нь зөвхөн IP толгойн TTL: эхний гурван пакетад TTL=1, "
                "дараагийнх нь 2, 3 … гэж нэмэгдэнэ. Иймд хариу нь зорилтот хостоос биш, TTL "
                "дууссан рүүтерээс ICMP Time Exceeded (Type=11, Code=0) хэлбэрээр ирнэ. "
                "Зөвхөн хамгийн сүүлийн алхамд Type=0 (Echo Reply) ирнэ."))
    st.append(P("<b>3. Ижил ба ялгаатай тал.</b> Ижил: хоёулаа ICMP Echo Request (8/0) "
                "илгээдэг, checksum-ийг ижил аргаар тооцдог, Identifier/Sequence-ийг "
                "ашигладаг. Ялгаатай: TTL-ийн утга (тогтмол эсвэл алхам алхмаар өсдөг), "
                "хариу мессежийн төрөл (0/0 эсвэл 11/0), мессежийн тоо (10 vs. hop бүрт 3), "
                "зорилго (RTT хэмжих vs. зам зургийг тодорхойлох)."))

    st.append(P("11.3. ARP-ийн асуултууд (1.3.3)", "h2"))
    st.append(P("<b>1. PC0-ийн ARP table.</b> PC0 нь зөвхөн нэг broadcast домэйны "
                "(192.168.1.0/24) хаягуудыг хардаг тул хүснэгтэд PC1 (192.168.1.2), PC2 "
                "(192.168.1.4), PC3 (192.168.1.5), Router0-ийн Gig0/0 (192.168.1.1) болон "
                "broadcast (192.168.1.255) бичлэгүүд байна. 10.0.0.0/24 сүлжээний хаягууд "
                "(Server0, PC4) энэ хүснэгтэд орохгүй — тэдгээр нь өөр L2 домэйн дээр байна."))
    st.append(P("<b>2. Яагаад broadcast вэ.</b> ARP request-ийг Switch0 broadcast хэлбэрээр "
                "дамжуулдаг нь хүлээн авагчийн MAC хаяг тодорхойгүй байгаатай шууд холбоотой: "
                "Ethernet хүрээг ямар нэг MAC хаяг руу илгээх ёстой тул ff:ff:ff:ff:ff:ff "
                "ашиглана. Свич нь broadcast хүрээг ирсэн портоос бусад бүх порт руу "
                "(flooding) хуулж илгээдэг."))
    st.append(P("<b>3. Хэн хүлээн авах вэ.</b> Тухайн broadcast домэйны бүх төхөөрөмж — "
                "PC1, PC2, PC3, Switch0 (тэр өөрөө дамжуулна) болон Router0-ийн Gig0/0 "
                "интерфейс. Өөр сүлжээний төхөөрөмж (Server0, PC4) хүлээн авахгүй, учир нь "
                "рүүтер broadcast-ыг дамжуулдаггүй."))
    st.append(P("<b>4. Reply-г хэрхэн мэдэх вэ.</b> ARP мессежийн Target IP (TPA) нь өөрийн "
                "IP хаягтай тэнцэж байвал тухайн төхөөрөмж хариу өгнө. Жишээ нь PC0 "
                "192.168.1.1-ийг асуухад зөвхөн Router0 хариулна; PC1, PC2, PC3 нь TPA нь "
                "өөрсдийн хаягтай таарахгүй тул хариугүй өнгөрнө."))
    st.append(P("<b>5. MAC хаягийн өөрчлөлт.</b> Пакет hop бүрт шинэ Ethernet хүрээ болж, "
                "Src/Dst MAC нь тухайн холбоосын хоёр төгсгөлийн хаягаар солигдоно. IP хаяг "
                "нь төгсгөлийн хост хүртэл өөрчлөгдөхгүй (NAT байхгүй тохиолдолд). "
                "Тиймээс MAC нь зөвхөн нэг холбоос дээр утгатай, IP нь бүх замд утгатай."))
    st.append(P("<b>6. Рүүтер яагаад Gig0/1-ээр ARP үүсгэх вэ.</b> 10.0.0.0/24 сүлжээ нь "
                "Gig0/1 интерфейстэй шууд холбогдсон (connected) тул рүүтер зорилтот IP-г "
                "тэр интерфейсээр гаргана. Гэхдээ Ethernet хүрээг бүтээхийн тулд дараагийн "
                "hop-ийн MAC хаяг хэрэгтэй — үүнийг Gig0/1-ийн сүлжээнд ARP request "
                "илгээж олно. Хэрэв зорилтот хаяг өөр рүүтерийн цаана байсан бол ARP-ыг "
                "зорилтот хост руу биш, дараагийн hop-ийн IP руу илгээнэ."))

    # ---- 12
    st.append(P("12. Дүгнэлт", "h1"))
    st.append(P("Энэ ажлаар ICMP болон ARP протоколын ажиллагааг бодит терминал дээр "
                "гүйцэтгэсэн туршилтаар батлав. ping нь ICMP Echo Request (Type 8, Code 0) "
                "илгээж, Echo Reply (Type 0, Code 0)-оос RTT (60.9–70.8 ms) ба TTL (114)-ийг "
                "олддог болохыг, traceroute нь TTL-ийг алхам алхмаар нэмэгдүүлж дундын "
                "рүүтерүүдээс Time Exceeded (Type 11, Code 0) мессеж авч 9 hop бүхий замыг "
                "тодорхойлдог болохыг хэмжилтээр харуулав. ICMP хариуны толгойг байт "
                "түвшинд задалж, Type, Code, Checksum, Identifier, Sequence талбарыг "
                "баталгаажуулсан бөгөөд checksum-ий нэгтгэсэн шалгалт 0xFFFF гарсан нь "
                "мессеж бүрэн бүтэн байсныг харуулав."))
    st.append(P("ARP-ийн хувьд кэш нь бодит гарцын MAC хаягийг (10:27:f5:48:a5:90) "
                "хадгалж, хариу ирээгүй хаяг нь (incomplete) төлөвт үлдэж, IP түвшинд "
                "EHOSTUNREACH алдаа болж илэрдгийг ажиглав. ARP хүрээний 42 байт бүтцийг "
                "талбар талбараар нь задалж, request нь broadcast (Dst "
                "ff:ff:ff:ff:ff:ff, Target MAC 00:00:00:00:00:00), reply нь unicast "
                "хэлбэрээр буцдаг болохыг батлав. Мөн топологи дээр пакет дамжуулахад "
                "IP хаяг өөрчлөгдөхгүй, харин MAC хаяг hop бүрт солигддог гэдэг нь L2 ба "
                "L3 хаягийн үүргийн ялгааг тодорхой харуулсан."))
    st.append(P("Туршилтын явцад гарсан сонирхолтой ажиглалт нь path MTU-ийн хэмжээ "
                "1500 биш 1492 байсан явдал (PPPoE инкапсуляцийн улмаас) болон хэтэрсэн "
                "пакет дээр ICMP Type 3 Code 4 мессеж ирэхгүй, пакет чимээгүй хаягдаж "
                "байсан явдал юм. Энэ нь ICMP-ийг сүлжээнд шүүх нь Path MTU Discovery-г "
                "эвдэж, том пакеттай холболтыг гацаах эрсдэлтэйг харуулж байна.", "p"))

    doc.build(st)
    print(OUT)


if __name__ == "__main__":
    build()
