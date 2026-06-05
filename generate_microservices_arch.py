from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 2400, 1450
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

font_candidates = ['/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf']
font_path = next((p for p in font_candidates if Path(p).exists()), None)
if not font_path:
    raise SystemExit('Arial font not found')

def font(size, bold=False):
    p = font_path
    if bold:
        bp = p.replace('Arial.ttf', 'Arial Bold.ttf')
        if Path(bp).exists():
            p = bp
    return ImageFont.truetype(p, size=size)

TITLE = font(60, True)
H1 = font(36, True)
H2 = font(25, True)
TXT = font(21)
TXT_B = font(22, True)
SM = font(17)
SM_B = font(18, True)
XS = font(15)

NAVY = '#10233d'
GRAY = '#667085'
LIGHT = '#f6f8fc'
AWS = '#ff9900'
DO = '#2b6cf6'
PURPLE = '#7c3aed'
BLUE = '#2563eb'
GREEN = '#16a34a'
TEAL = '#0f766e'
ORANGE = '#f97316'
RED = '#ef4444'
BORDER = '#cbd5e1'


def rr(box, outline, fill='white', width=3, radius=24):
    d.rounded_rectangle(box, radius=radius, outline=outline, fill=fill, width=width)


def text(x, y, value, f=TXT, fill=NAVY, anchor='la'):
    d.text((x, y), value, font=f, fill=fill, anchor=anchor)


def center_text(box, value, f=TXT, fill=GRAY, spacing=4):
    x1, y1, x2, y2 = box
    bb = d.multiline_textbbox((0, 0), value, font=f, spacing=spacing, align='center')
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.multiline_text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), value, font=f, fill=fill, spacing=spacing, align='center')


def simple_box(x, y, w, h, title, body, outline, fill='white', title_font=TXT_B):
    rr((x, y, x + w, y + h), outline, fill, 3, 18)
    text(x + w / 2, y + 21, title, title_font, NAVY, 'ma')
    center_text((x + 10, y + 38, x + w - 10, y + h - 10), body, SM, GRAY)


def service_box(x, y, w, h, title, body, color):
    rr((x, y, x + w, y + h), color, 'white', 3, 16)
    d.rounded_rectangle((x, y, x + w, y + 38), radius=16, fill=color)
    d.rectangle((x, y + 18, x + w, y + 38), fill=color)
    text(x + w / 2, y + 19, title, SM_B, 'white', 'ma')
    center_text((x + 8, y + 44, x + w - 8, y + h - 8), body, SM, GRAY)


def datastore(x, y, w, h, title, color):
    rr((x, y, x + w, y + h), color, 'white', 3, 15)
    text(x + w / 2, y + h / 2, title, SM_B, NAVY, 'mm')


def arrow_head(p1, p2, color, size=13):
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    aw = size * 0.42
    pts = [
        p2,
        (p2[0] - size * math.cos(ang) + aw * math.sin(ang), p2[1] - size * math.sin(ang) - aw * math.cos(ang)),
        (p2[0] - size * math.cos(ang) - aw * math.sin(ang), p2[1] - size * math.sin(ang) + aw * math.cos(ang)),
    ]
    d.polygon(pts, fill=color)


def routed(points, color, width=4, dashed=False):
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        if dashed:
            if p1[0] == p2[0]:
                length = abs(p2[1] - p1[1]); step = 24; dash = 14; sign = 1 if p2[1] >= p1[1] else -1
                for n in range(0, length, step):
                    y1 = p1[1] + sign * n
                    y2 = p1[1] + sign * min(n + dash, length)
                    d.line((p1[0], y1, p2[0], y2), fill=color, width=width)
            else:
                length = abs(p2[0] - p1[0]); step = 24; dash = 14; sign = 1 if p2[0] >= p1[0] else -1
                for n in range(0, length, step):
                    x1 = p1[0] + sign * n
                    x2 = p1[0] + sign * min(n + dash, length)
                    d.line((x1, p1[1], x2, p2[1]), fill=color, width=width)
        else:
            d.line((p1, p2), fill=color, width=width)
    arrow_head(points[-2], points[-1], color)


def lane_label(x, y, value, color=GRAY):
    text(x, y, value, XS, color)


def label_chip(x, y, value, color=GRAY):
    bb = d.textbbox((0, 0), value, font=XS)
    w = bb[2] - bb[0] + 18
    h = bb[3] - bb[1] + 10
    rr((x, y, x + w, y + h), BORDER, 'white', 1, 10)
    text(x + w / 2, y + h / 2 - 1, value, XS, color, 'mm')

text(W / 2, 58, 'VigileEye Microservices System Architecture', TITLE, NAVY, 'ma')

# Left / right shells
simple_box(35, 130, 295, 560, 'Actors', '', BORDER, LIGHT, H1)
simple_box(35, 735, 295, 510, 'Clients & Sources', '', BORDER, LIGHT, H1)
simple_box(1765, 130, 600, 620, 'External Providers', '', BORDER, LIGHT, H1)

simple_box(65, 215, 235, 110, 'Camera Owner', 'Owns cameras, zones,\nsubscriptions, and sharing', PURPLE, '#faf5ff')
simple_box(65, 360, 235, 110, 'Reader', 'Read-only access to\nshared cameras and evidence', GREEN, '#f0fdf4')
simple_box(65, 505, 235, 110, 'Writer', 'Edit-level access to\nshared cameras and settings', ORANGE, '#fff7ed')
simple_box(65, 825, 235, 120, 'Web & Mobile Client', 'React + Ionic + Capacitor\nREST, WebSocket, WebRTC/WHEP', PURPLE, '#faf5ff')
simple_box(65, 990, 235, 95, 'IP Cameras', 'RTSP feeds and\ncamera metadata', NAVY, 'white')
simple_box(65, 1120, 235, 95, 'Shared Trust Model', 'JWT access / refresh\nused across platform services', TEAL, '#f0fdfa')

# Core zones
rr((385, 130, 1710, 1185), AWS, '#fffdfa', 4, 28)
text(435, 175, 'AWS Core Platform', H1, AWS)
rr((1765, 820, 2365, 1185), DO, '#f8fbff', 4, 28)
text(1815, 865, 'DigitalOcean AI Runtime', H1, DO)

# Traefik
service_box(430, 520, 185, 105, 'Traefik', 'API gateway\nand ingress', PURPLE)

# Group containers
rr((690, 180, 1230, 360), BLUE, '#f8fbff', 2, 22); text(720, 210, 'Access & Identity', H2, BLUE)
rr((690, 395, 1570, 575), BLUE, '#f8fbff', 2, 22); text(720, 425, 'Surveillance Core', H2, BLUE)
rr((690, 610, 1570, 935), GREEN, '#f8fff9', 2, 22); text(720, 640, 'Intelligence & Operations', H2, GREEN)

# Services inside containers
service_box(730, 240, 200, 92, 'Auth Service', 'JWT, login, OTP,\nGoogle OAuth', BLUE)
service_box(970, 240, 220, 92, 'Members Service', 'Invitations, groups,\nreader/writer access', BLUE)

service_box(730, 455, 190, 92, 'Camera Management', 'Cameras, zones,\nhealth, permissions', BLUE)
service_box(955, 455, 170, 92, 'Streaming', 'Session control\nand playback setup', BLUE)
service_box(1160, 455, 170, 92, 'Storage', 'Recordings, retention,\nbackend routing', BLUE)
service_box(1365, 455, 170, 92, 'MediaMTX Control', 'Relay orchestration\nand media-plane control', TEAL)

service_box(730, 690, 190, 92, 'Object Detection', 'Sessions, alerts,\nwebsocket updates', GREEN)
service_box(955, 690, 170, 92, 'Notification', 'FCM dispatch\nand email fallback', GREEN)
service_box(1160, 690, 170, 92, 'Analytics', 'KPIs, dashboards,\nread models', GREEN)
service_box(1365, 690, 170, 92, 'AI Chatbot', 'Guarded analytics\nQ&A', GREEN)
service_box(1045, 825, 210, 92, 'Subscription', 'Plans, checkout,\nentitlements', GREEN)

# Datastores
text(1135, 982, 'Service-Owned Data Stores', H2, NAVY, 'ma')
datastore(710, 1040, 130, 55, 'Auth DB', BLUE)
datastore(865, 1040, 145, 55, 'Members DB', BLUE)
datastore(1035, 1040, 145, 55, 'Camera DB', BLUE)
datastore(1205, 1040, 155, 55, 'Recording DB', BLUE)
datastore(1385, 1040, 180, 55, 'Detection Core DB', GREEN)
datastore(1590, 1040, 145, 55, 'Billing DB', GREEN)

# Providers
simple_box(1795, 220, 530, 72, 'Google OAuth', 'Social sign-in provider', BLUE, '#f9fbff')
simple_box(1795, 320, 530, 72, 'Mail Service', 'Verification, OTP, reset, invitations', ORANGE, '#fff7ed')
simple_box(1795, 420, 530, 72, 'Firebase FCM', 'Push delivery to web/mobile devices', GREEN, '#f0fdf4')
simple_box(1795, 520, 530, 72, 'Stripe', 'Subscription checkout and billing', PURPLE, '#faf5ff')
simple_box(1795, 620, 530, 72, 'LLM Provider', 'Natural-language analytics assistance', TEAL, '#f0fdfa')
simple_box(1795, 720, 530, 72, 'MediaMTX', 'RTSP ingest and WebRTC / WHEP relay', TEAL, '#f0fdfa')

# DO runtime
service_box(1800, 930, 170, 90, 'Event Detection API', 'FastAPI ingress\nPOST /predict', DO)
service_box(1995, 930, 145, 90, 'Redis Broker', 'Queue / result\nbackend', ORANGE)
service_box(2165, 930, 145, 90, 'Celery Worker', 'Async clip\nclassification', GREEN)
datastore(1800, 1060, 170, 55, 'Event Detection DB', DO)
datastore(1995, 1060, 315, 55, 'ONNX Runtime + Models', PURPLE)

# Actors -> client -> gateway
for ay in (270, 415, 560):
    routed([(300, ay), (345, ay), (345, 885), (430, 885), (430, 572)], NAVY, 4)
lane_label(338, 845, 'HTTPS / REST + JWT')

# Real-time lanes from client
routed([(300, 885), (650, 885), (650, 735), (730, 735)], PURPLE, 4)
lane_label(392, 865, 'WebSocket alerts', PURPLE)
routed([(300, 915), (650, 915), (650, 500), (955, 500)], BLUE, 4)
lane_label(392, 932, 'WebRTC / WHEP requests', BLUE)
routed([(300, 1035), (650, 1035), (650, 500), (730, 500)], NAVY, 4)
lane_label(362, 1005, 'RTSP ingest')

# Gateway to group containers only
routed([(615, 572), (670, 572), (670, 270), (690, 270)], NAVY, 4)
routed([(615, 572), (670, 572), (670, 485), (690, 485)], NAVY, 4)
routed([(615, 572), (670, 572), (670, 760), (690, 760)], NAVY, 4)
lane_label(640, 316, 'identity APIs')
lane_label(640, 520, 'core APIs')
lane_label(640, 790, 'intelligence APIs')

# Internal service flows
routed([(920, 500), (955, 500)], NAVY, 4)
routed([(1125, 500), (1160, 500)], NAVY, 4)
routed([(920, 735), (955, 735)], GREEN, 4)
routed([(1125, 735), (1160, 735)], GREEN, 4)
routed([(1330, 735), (1365, 735)], GREEN, 4)
routed([(1150, 825), (1150, 782)], GREEN, 4)
label_chip(918, 390, 'camera context')
label_chip(1148, 390, 'recording path')
label_chip(900, 835, 'incident delivery', GREEN)
label_chip(1118, 835, 'analytics read model', GREEN)
label_chip(1320, 835, 'guarded analytics', GREEN)
label_chip(1180, 865, 'plan checks', GREEN)

# Providers aligned with services
routed([(930, 286), (1650, 286), (1650, 256), (1795, 256)], BLUE, 3)
label_chip(1510, 230, 'OAuth')
routed([(1190, 286), (1720, 286), (1720, 356), (1795, 356)], ORANGE, 3)
label_chip(1485, 320, 'SMTP / mail API')
routed([(1125, 735), (1685, 735), (1685, 456), (1795, 456)], GREEN, 3)
label_chip(1500, 414, 'FCM push')
routed([(1255, 870), (1710, 870), (1710, 556), (1795, 556)], PURPLE, 3)
label_chip(1495, 514, 'Stripe API')
routed([(1535, 735), (1700, 735), (1700, 656), (1795, 656)], TEAL, 3)
label_chip(1495, 614, 'LLM API')
routed([(1535, 500), (1680, 500), (1680, 756), (1795, 756)], TEAL, 3)
label_chip(1450, 708, 'RTSP + WebRTC relay')

# Persistence lines
for sx, sy, dx, color in [
    (830, 332, 775, BLUE),
    (1080, 332, 937, BLUE),
    (825, 547, 1107, BLUE),
    (1245, 547, 1282, BLUE),
    (825, 782, 1475, GREEN),
    (1150, 917, 1662, GREEN),
]:
    routed([(sx, sy), (sx, 1020), (dx, 1020), (dx, 1040)], color, 3)

# Cross-cloud AI
routed([(825, 735), (825, 905), (1735, 905), (1735, 975), (1800, 975)], RED, 4, dashed=True)
label_chip(1260, 874, 'Authenticated clip-level inference request', RED)
routed([(1800, 1087), (1735, 1087), (1735, 950), (1005, 950), (1005, 782)], RED, 4, dashed=True)
label_chip(1230, 918, 'Classification result + persisted event status', RED)

# DO internal links
routed([(1970, 975), (1995, 975)], ORANGE, 4)
routed([(2140, 975), (2165, 975)], GREEN, 4)
routed([(1885, 1020), (1885, 1060)], DO, 4)
routed([(2237, 1020), (2237, 1060)], PURPLE, 4)

# Legend
rr((430, 1230, 1280, 1400), BORDER, '#fbfdff', 2, 24)
text(1070, 1266, 'Legend', H2, NAVY, 'ma')
legend = [
    (NAVY, 'Synchronous REST / control-plane calls'),
    (PURPLE, 'Real-time delivery: WebSocket / WebRTC / WHEP'),
    (BLUE, 'Identity, ingress, and owned persistence links'),
    (GREEN, 'Operational outputs reused by alerts, analytics, and billing'),
    (RED, 'Cross-cloud AI inference exchange with the DigitalOcean runtime'),
]
ly = 1305
for color, value in legend:
    d.line((500, ly, 590, ly), fill=color, width=4)
    text(620, ly - 12, value, SM, NAVY)
    ly += 28

out = Path('/Users/mac/Desktop/PFE/report_final/casestudy/microservices_Arch.png')
img.save(out)
print(out)
