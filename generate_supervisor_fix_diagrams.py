from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUTDIR = Path('/Users/mac/Desktop/PFE/report_final/generated_supervisor_diagrams')
OUTDIR.mkdir(parents=True, exist_ok=True)

REG = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

FONT_CACHE = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in FONT_CACHE:
        FONT_CACHE[key] = ImageFont.truetype(BOLD if bold else REG, size)
    return FONT_CACHE[key]

WHITE = '#ffffff'
BLACK = '#1f2937'
MUTED = '#4b5563'
LIGHT = '#f8fafc'
BORDER = '#cbd5e1'
BLUE = '#2563eb'
BLUE_L = '#dbeafe'
GREEN = '#15803d'
GREEN_L = '#dcfce7'
PURPLE = '#7c3aed'
PURPLE_L = '#ede9fe'
ORANGE = '#ea580c'
ORANGE_L = '#ffedd5'
RED = '#dc2626'
RED_L = '#fee2e2'
TEAL = '#0f766e'
TEAL_L = '#ccfbf1'
AMBER = '#d97706'
AMBER_L = '#fef3c7'
GRAYBOX = '#f1f5f9'
AWS_ORANGE = '#ff9900'
DO_BLUE = '#3b82f6'


def text_size(draw, text, f):
    if not text:
        return (0,0)
    bbox = draw.multiline_textbbox((0,0), text, font=f, spacing=4)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]


def wrap(draw, text, f, max_w):
    words = text.split()
    lines = []
    cur = ''
    for w in words:
        test = w if not cur else cur + ' ' + w
        if text_size(draw, test, f)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return '\n'.join(lines)


def box(draw, xy, title=None, body=None, fill=WHITE, outline=BORDER, title_fill=None, title_color=BLACK, body_color=BLACK, radius=22, title_h=42, title_font=None, body_font=None, align='center', body_pad=18):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3)
    if title:
        tf = title_font or font(26, True)
        if title_fill:
            draw.rounded_rectangle((x1,y1,x2,y1+title_h), radius=radius, fill=title_fill, outline=outline, width=0)
            draw.rectangle((x1,y1+title_h-radius,x2,y1+title_h), fill=title_fill)
        tw,th = text_size(draw, title, tf)
        draw.text(((x1+x2-tw)/2, y1 + (title_h-th)/2 - 2), title, font=tf, fill=title_color)
        content_top = y1 + title_h + 8
    else:
        content_top = y1 + body_pad
    if body:
        bf = body_font or font(22, False)
        max_w = (x2-x1) - 2*body_pad
        wrapped = []
        for para in body.split('\n'):
            wrapped.append(wrap(draw, para, bf, max_w))
        wrapped = '\n'.join(wrapped)
        bw,bh = text_size(draw, wrapped, bf)
        if align == 'center':
            tx = (x1+x2-bw)/2
        else:
            tx = x1 + body_pad
        ty = content_top + max(0, ((y2-content_top)-bh)/2)
        draw.multiline_text((tx,ty), wrapped, font=bf, fill=body_color, spacing=6, align=align)


def ellipse_label(draw, xy, text, fill='#f8fafc', outline=BORDER, color=BLACK, f=None):
    draw.ellipse(xy, fill=fill, outline=outline, width=3)
    f = f or font(22, False)
    wrapped = wrap(draw, text, f, xy[2]-xy[0]-20)
    tw,th = text_size(draw, wrapped, f)
    draw.multiline_text(((xy[0]+xy[2]-tw)/2, (xy[1]+xy[3]-th)/2-2), wrapped, font=f, fill=color, spacing=4, align='center')


def actor_box(draw, xy, title, subtitle, accent):
    box(draw, xy, fill=WHITE, outline=accent, radius=18)
    x1,y1,x2,y2 = xy
    # simple icon
    cx = x1 + 42
    cy = y1 + 38
    draw.ellipse((cx-12, cy-12, cx+12, cy+12), fill=accent)
    draw.rounded_rectangle((cx-18, cy+12, cx+18, cy+44), radius=10, fill=accent)
    tf = font(24, True)
    sf = font(20, False)
    title_w,title_h = text_size(draw, title, tf)
    sub_w,sub_h = text_size(draw, subtitle, sf)
    draw.text((x1+85, y1+20), title, font=tf, fill=BLACK)
    draw.text((x1+85, y1+58), subtitle, font=sf, fill=MUTED)


def service_box(draw, xy, title, subtitle='', fill=WHITE, outline=BLUE, accent_fill=None):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    tf = font(26, True)
    sf = font(21, False)
    title_wrapped = wrap(draw, title, tf, x2-x1-24)
    tw,th = text_size(draw, title_wrapped, tf)
    draw.multiline_text((x1+(x2-x1-tw)/2, y1+18), title_wrapped, font=tf, fill=BLACK, spacing=4, align='center')
    if subtitle:
        sub_wrapped = wrap(draw, subtitle, sf, x2-x1-24)
        sw,sh = text_size(draw, sub_wrapped, sf)
        draw.multiline_text((x1+(x2-x1-sw)/2, y1+22+th+8), sub_wrapped, font=sf, fill=MUTED, spacing=4, align='center')


def class_box(draw, xy, title, lines, header_fill, outline, title_color=WHITE):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=16, fill=WHITE, outline=outline, width=3)
    draw.rounded_rectangle((x1,y1,x2,y1+42), radius=16, fill=header_fill, outline=outline, width=0)
    draw.rectangle((x1,y1+22,x2,y1+42), fill=header_fill)
    tf = font(23, True)
    tw,th = text_size(draw, title, tf)
    draw.text((x1+(x2-x1-tw)/2, y1+8), title, font=tf, fill=title_color)
    draw.line((x1, y1+42, x2, y1+42), fill=outline, width=2)
    bf = font(18)
    yy = y1+54
    for line in lines:
        wrapped = wrap(draw, line, bf, x2-x1-24)
        draw.multiline_text((x1+12, yy), wrapped, font=bf, fill=BLACK, spacing=4)
        yy += text_size(draw, wrapped, bf)[1] + 8


def arrow(draw, p1, p2, color=BLACK, width=4, label=None, lf=None, label_fill=None, dashed=False):
    x1,y1 = p1; x2,y2 = p2
    if dashed:
        total = math.hypot(x2-x1, y2-y1)
        if total == 0:
            return
        dash = 16
        gap = 10
        dx = (x2-x1)/total
        dy = (y2-y1)/total
        pos = 0
        while pos < total-18:
            s = pos
            e = min(pos+dash, total-18)
            draw.line((x1+dx*s, y1+dy*s, x1+dx*e, y1+dy*e), fill=color, width=width)
            pos += dash + gap
    else:
        draw.line((x1,y1,x2,y2), fill=color, width=width)
    ang = math.atan2(y2-y1, x2-x1)
    ah = 14
    pts = [
        (x2, y2),
        (x2 - ah*math.cos(ang-math.pi/6), y2 - ah*math.sin(ang-math.pi/6)),
        (x2 - ah*math.cos(ang+math.pi/6), y2 - ah*math.sin(ang+math.pi/6))
    ]
    draw.polygon(pts, fill=color)
    if label:
        lf = lf or font(18)
        tx = (x1+x2)/2
        ty = (y1+y2)/2
        wrapped = wrap(draw, label, lf, 220)
        tw,th = text_size(draw, wrapped, lf)
        if label_fill:
            pad = 6
            draw.rounded_rectangle((tx-tw/2-pad, ty-th/2-pad, tx+tw/2+pad, ty+th/2+pad), radius=8, fill=label_fill, outline=None)
        draw.multiline_text((tx-tw/2, ty-th/2), wrapped, font=lf, fill=color if not label_fill else BLACK, spacing=4, align='center')


def cloud_boundary(draw, xy, title, color):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=28, outline=color, width=4)
    tf = font(32, True)
    draw.rounded_rectangle((x1+18, y1-12, x1+240, y1+48), radius=18, fill=WHITE, outline=None)
    draw.text((x1+34, y1+2), title, font=tf, fill=color)


def header(draw, W, title):
    tf = font(44, True)
    tw,th = text_size(draw, title, tf)
    draw.text(((W-tw)/2, 28), title, font=tf, fill='#0f172a')


def static_context():
    W,H = 2400,1400
    img = Image.new('RGB',(W,H),WHITE)
    d = ImageDraw.Draw(img)
    header(d,W,'VigileEye Static Context Diagram')
    cloud_boundary(d,(760,170,1640,1080),'VigileEye Platform',BLUE)
    box(d,(900,330,1500,840), title='VigileEye Platform', body='Unified surveillance application providing authentication, camera sharing, live monitoring, recordings, alerts, analytics, billing, and AI-assisted features.', fill='#f8fbff', outline=BLUE, title_fill=BLUE_L, title_color=BLACK, body_font=font(28), body_color=BLACK, align='center', title_h=56)

    # actors
    box(d,(70,180,520,690), title='Actors', fill='#fbfdff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    actor_box(d,(110,270,480,390),'Camera Owner','Full platform control',BLUE)
    actor_box(d,(110,430,480,550),'Reader','Read-only shared access',GREEN)
    actor_box(d,(110,590,480,710),'Writer','Editor-level shared access',ORANGE)

    # external systems
    box(d,(1810,170,2310,920), title='External Systems', fill='#fbfdff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    service_box(d,(1860,260,2260,345),'Google OAuth','Social sign-in and identity link', outline=BLUE)
    service_box(d,(1860,375,2260,460),'Mail Service','OTP, verification, reset, invitation email', outline=ORANGE)
    service_box(d,(1860,490,2260,575),'Firebase FCM','Push delivery to mobile/web clients', outline=GREEN)
    service_box(d,(1860,605,2260,690),'Stripe Gateway','Subscription checkout and billing', outline=PURPLE)
    service_box(d,(1860,720,2260,805),'MediaMTX','WebRTC / WHEP media relay', outline=TEAL)
    service_box(d,(1860,835,2260,920),'DigitalOcean Event Detection','Clip-level anomaly classification', outline=RED)

    # supporting systems bottom
    box(d,(70,830,520,1160), title='Operational Systems', fill='#fbfdff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    service_box(d,(110,930,480,1015),'Web & Mobile Client','React + Ionic + Capacitor', outline=PURPLE)
    service_box(d,(110,1040,480,1125),'IP Cameras','RTSP camera feeds and metadata', outline=BLACK)

    # arrows
    arrow(d,(480,330),(900,420),label='Authenticate, manage cameras, monitor, record, inspect alerts and analytics', color=BLACK, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(480,490),(900,520),label='Shared live viewing, recording access, alert timeline, analytics consultation', color=BLACK, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(480,650),(900,620),label='Shared editing on granted cameras, settings, and operational controls', color=BLACK, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(480,970),(900,710),label='HTTPS / REST, WebSocket alerts, WebRTC live playback', color=PURPLE, width=5, lf=font(18), label_fill=WHITE)
    arrow(d,(480,1085),(900,770),label='RTSP feeds, camera metadata', color=BLACK, width=4, lf=font(18), label_fill=WHITE)

    arrow(d,(1500,380),(1860,300),label='OAuth', color=BLUE, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(1500,460),(1860,420),label='SMTP / OTP / invitations', color=ORANGE, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(1500,570),(1860,530),label='FCM push', color=GREEN, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(1500,660),(1860,645),label='Payments / subscriptions', color=PURPLE, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(1500,750),(1860,760),label='WebRTC / WHEP media delivery', color=TEAL, width=4, lf=font(17), label_fill=WHITE)
    arrow(d,(1500,820),(1860,875),label='Cross-cloud AI requests and results', color=RED, width=4, lf=font(17), label_fill=WHITE)

    img.save(OUTDIR/'static_context_diagram_v2.png')


def global_use_case():
    W,H = 2400,1500
    img = Image.new('RGB',(W,H),WHITE)
    d = ImageDraw.Draw(img)
    header(d,W,'Global System Use Case Diagram')

    # actors
    box(d,(70,170,420,1320), title='Actors', fill='#fbfdff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    actor_box(d,(110,260,380,360),'Visitor','Public registration',BLUE)
    actor_box(d,(110,450,380,550),'Reader','Read-only shared user',GREEN)
    actor_box(d,(110,640,380,740),'Writer','Editor shared user',ORANGE)
    actor_box(d,(110,980,380,1080),'Camera Owner','Resource owner',PURPLE)

    # group boxes
    box(d,(470,170,1680,1320), title='VigileEye Use Cases', fill='#ffffff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    d.rounded_rectangle((520,245,1625,465), radius=18, outline='#c7d2fe', width=3, fill='#fafaff')
    d.text((560,255),'Public Access', font=font(24, True), fill=BLUE)
    d.rounded_rectangle((520,505,1625,1260), radius=18, outline='#fed7aa', width=3, fill='#fffaf5')
    d.text((560,515),'Authenticated Platform Features', font=font(24, True), fill=ORANGE)

    # public use cases
    ellipse_label(d,(620,300,980,380),'Register')
    ellipse_label(d,(1080,300,1450,380),'Request Password Reset')

    # shared use cases
    usecases = [
        ((620,575,1020,655),'Observe Live Streams'),
        ((620,700,1020,780),'Browse Recordings'),
        ((620,825,1020,905),'Inspect Alerts'),
        ((620,950,1020,1030),'Inspect Analytics'),
        ((1080,575,1490,655),'Coordinate Member Sharing'),
        ((1080,700,1490,780),'Plan Detection Zones'),
        ((1080,825,1490,905),'Control Recordings'),
        ((1080,950,1490,1030),'Run AI Detection'),
        ((850,1095,1250,1175),'Subscription and Billing'),
        ((850,1195,1250,1275),'Chat with AI'),
    ]
    for xy, text in usecases:
        ellipse_label(d, xy, text)

    # authentication note rather than repeated arrows
    box(d,(560,1080,760,1255), title='Authentication', body='JWT-based access is required for the private platform use cases.', fill=RED_L, outline=RED, title_fill=RED, title_color=WHITE, body_font=font(20), body_color=BLACK, align='center', title_h=48)

    # external systems
    box(d,(1770,170,2310,1320), title='External Services', fill='#fbfdff', outline=BORDER, title_fill=GRAYBOX, title_h=54)
    ext = [
        ((1840,265,2240,345),'Mail Service'),
        ((1840,390,2240,470),'Google OAuth'),
        ((1840,515,2240,595),'MediaMTX'),
        ((1840,640,2240,720),'Firebase FCM'),
        ((1840,765,2240,845),'Analytics Engine'),
        ((1840,890,2240,970),'Stripe Gateway'),
        ((1840,1015,2240,1095),'YOLO Engine'),
        ((1840,1140,2240,1220),'LLM Provider'),
    ]
    colors = [ORANGE, BLUE, TEAL, GREEN, TEAL, PURPLE, RED, GREEN]
    for (xy,txt), c in zip(ext, colors):
        service_box(d, xy, txt, outline=c)

    # actor associations
    for p in [(380,310),(380,500),(380,690),(380,1030)]:
        pass
    arrow(d,(380,310),(620,340),color=BLACK,width=4)
    arrow(d,(380,310),(1080,340),color=BLACK,width=4)
    arrow(d,(380,500),(620,615),color=BLACK,width=4)
    arrow(d,(380,500),(620,865),color=BLACK,width=4)
    arrow(d,(380,500),(620,990),color=BLACK,width=4)
    arrow(d,(380,690),(1080,615),color=BLACK,width=4)
    arrow(d,(380,690),(1080,740),color=BLACK,width=4)
    arrow(d,(380,690),(1080,865),color=BLACK,width=4)
    arrow(d,(380,1030),(1080,615),color=BLACK,width=4)
    arrow(d,(380,1030),(1080,740),color=BLACK,width=4)
    arrow(d,(380,1030),(1080,865),color=BLACK,width=4)
    arrow(d,(380,1030),(1080,990),color=BLACK,width=4)
    arrow(d,(380,1030),(850,1135),color=BLACK,width=4)
    arrow(d,(380,1030),(850,1235),color=BLACK,width=4)

    # register external services
    arrow(d,(980,340),(1840,305),label='verification email / OTP',color=ORANGE,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(980,360),(1840,430),label='social sign-in option',color=BLUE,width=4,lf=font(18),label_fill=WHITE)

    # external service links
    arrow(d,(1020,615),(1840,555),label='live media path',color=TEAL,width=4,lf=font(17),label_fill=WHITE)
    arrow(d,(1020,865),(1840,680),label='push notifications',color=GREEN,width=4,lf=font(17),label_fill=WHITE)
    arrow(d,(1020,990),(1840,805),label='dashboard metrics',color=TEAL,width=4,lf=font(17),label_fill=WHITE)
    arrow(d,(1250,1135),(1840,930),label='payments',color=PURPLE,width=4,lf=font(17),label_fill=WHITE)
    arrow(d,(1490,990),(1840,1055),label='object-level detection',color=RED,width=4,lf=font(17),label_fill=WHITE)
    arrow(d,(1250,1235),(1840,1180),label='natural-language analytics',color=GREEN,width=4,lf=font(17),label_fill=WHITE)

    # auth dependencies simplified
    for target in [(620,615),(620,740),(620,865),(620,990),(1080,615),(1080,740),(1080,865),(1080,990),(850,1135),(850,1235)]:
        arrow(d,(760,1165),(target[0]+60,target[1]),color=RED,width=2,dashed=True)

    note = 'Register now visibly involves Mail Service and Google OAuth.\nAuthentication dependencies are summarized once instead of being repeated across every use case.'
    box(d,(560,1340,1800,1460), body=note, fill='#f8fafc', outline=BORDER, radius=16, body_font=font(20), body_color=MUTED, align='center')

    img.save(OUTDIR/'global_use_case_v2.png')


def sprint2_class_grouped():
    W,H = 2600,1700
    img = Image.new('RGB',(W,H),WHITE)
    d = ImageDraw.Draw(img)
    header(d,W,'Sprint II Class Diagram Grouped by Owning Microservice')

    # package boundaries
    packages = {
        'Auth / Identity Reference': ((70,170,520,610), BLUE_L, BLUE),
        'Camera Management': ((600,170,1230,610), '#e0f2fe', '#0284c7'),
        'Object Detection Service': ((1310,170,2520,930), GREEN_L, GREEN),
        'Subscription Service': ((70,700,1230,1260), ORANGE_L, ORANGE),
        'Notification Service': ((1310,980,1840,1530), '#fef2f2', RED),
        'Analytics / AI Chatbot Read Side': ((1900,980,2520,1530), PURPLE_L, PURPLE),
    }
    for title,(xy,fill,stroke) in packages.items():
        box(d,xy,title=title,fill=fill,outline=stroke,title_fill=fill,title_color=stroke,title_h=52)

    # classes
    class_box(d,(110,250,480,560),'User',[
        'email', 'username', 'is_verified', 'failed_login_attempts', 'last_login'
    ], BLUE, BLUE)

    class_box(d,(650,250,930,600),'Camera',[
        'owner_user_id', 'name', 'stream_url', 'status', 'last_heartbeat'
    ], '#0284c7', '#0284c7')
    class_box(d,(960,250,1210,600),'Zone',[
        'camera_id', 'name', 'zone_type', 'severity', 'schedule_enabled'
    ], '#0284c7', '#0284c7')

    class_box(d,(1380,250,1640,610),'DetectionSession',[
        'camera_id', 'started_at', 'status', 'session counters'
    ], GREEN, GREEN)
    class_box(d,(1680,250,1970,750),'DetectionEvent',[
        'camera_id', 'session_id', 'zone_id', 'object_class', 'confidence', 'occurred_at'
    ], GREEN, GREEN)
    class_box(d,(2010,250,2310,640),'Alert',[
        'detection_event_id', 'severity', 'message', 'acknowledged', 'suppressed_until'
    ], GREEN, GREEN)
    class_box(d,(2060,690,2470,900),'EventRecord',[
        'evidence snapshot / history', 'downstream event timeline view'
    ], GREEN, GREEN)

    class_box(d,(160,780,420,1140),'Plan',[
        'plan_type', 'price', 'annual_price', 'limits', 'features'
    ], ORANGE, ORANGE)
    class_box(d,(470,780,770,1140),'UserSubscription',[
        'user_id', 'plan', 'started_at', 'expires_at', 'is_active'
    ], ORANGE, ORANGE)
    class_box(d,(820,780,1170,1180),'PaymentHistoryEntry',[
        'user_id', 'plan', 'status', 'amount_cents', 'created_at'
    ], ORANGE, ORANGE)

    class_box(d,(1390,1080,1760,1450),'NotificationLog',[
        'notification_type', 'status', 'channels', 'tokens_targeted', 'created_at'
    ], RED, RED)

    class_box(d,(1950,1080,2230,1380),'AnalyticsQueryFilters',[
        'date range', 'camera_id(s)', 'zone', 'type', 'top_n'
    ], PURPLE, PURPLE)
    class_box(d,(2260,1080,2480,1380),'AISQLChatAgent',[
        'schema_snapshot', 'llm_enabled', 'cache / memory', 'answer_question()'
    ], PURPLE, PURPLE)

    # arrows
    arrow(d,(480,405),(650,405),label='owns',lf=font(16),label_fill=WHITE)
    arrow(d,(930,425),(960,425),label='contains',lf=font(16),label_fill=WHITE)
    arrow(d,(1210,420),(1380,400),label='camera context',color='#0284c7',lf=font(16),label_fill=WHITE)
    arrow(d,(1085,600),(1680,430),label='zone context',color='#0284c7',lf=font(16),label_fill=WHITE)
    arrow(d,(1640,420),(1680,420),label='produces',color=GREEN,lf=font(16),label_fill=WHITE)
    arrow(d,(1970,470),(2010,430),label='triggers',color=GREEN,lf=font(16),label_fill=WHITE)
    arrow(d,(1680,620),(2060,790),label='historical evidence',color=GREEN,lf=font(16),label_fill=WHITE)
    arrow(d,(770,950),(160,950),label='subscribes to',color=ORANGE,lf=font(16),label_fill=WHITE)
    arrow(d,(770,980),(820,980),label='payments',color=ORANGE,lf=font(16),label_fill=WHITE)
    arrow(d,(1680,620),(1390,1180),label='dispatch trace',color=RED,lf=font(16),label_fill=WHITE)
    arrow(d,(1760,1260),(1950,1220),label='analytics queries',color=PURPLE,lf=font(16),label_fill=WHITE)
    arrow(d,(2230,1230),(2260,1230),label='guarded SQL',color=PURPLE,lf=font(16),label_fill=WHITE)
    arrow(d,(2310,470),(1950,1160),label='read-oriented reuse',color=PURPLE,lf=font(16),label_fill=WHITE)
    arrow(d,(1170,930),(1380,520),label='feature gating / entitlement context',color=ORANGE,lf=font(16),label_fill=WHITE)

    note = 'Logical business relationships across service boundaries — not one shared database schema.\nGrouping is by owning microservice to clarify that Sprint II spans several services at once.'
    box(d,(520,1390,2060,1610), title='Interpretation Note', body=note, fill=GRAYBOX, outline=BORDER, title_fill=GRAYBOX, title_color=BLACK, body_font=font(26), body_color=BLACK, align='center', title_h=48)

    img.save(OUTDIR/'sprint2_class_grouped_v2.png')


def ai_overview():
    W,H = 2400,1400
    img = Image.new('RGB',(W,H),WHITE)
    d = ImageDraw.Draw(img)
    header(d,W,'AI System Overview — Event Detection Service in the Global VigileEye Flow')

    cloud_boundary(d,(90,180,980,1160),'AWS-side VigileEye Modules',AWS_ORANGE)
    cloud_boundary(d,(1160,180,2310,1160),'DigitalOcean Event Detection Runtime',DO_BLUE)

    service_box(d,(170,290,470,410),'Clip Sources','recorded excerpts or uploaded video clips', outline=BLACK)
    service_box(d,(170,500,470,620),'Calling Module','frontend / monitoring / storage-backed workflow', outline=PURPLE)
    service_box(d,(170,710,470,830),'Downstream Consumers','monitoring, notification, analytics', outline=TEAL)
    service_box(d,(560,500,900,620),'AWS-side Guard Checks','permission, membership, subscription, JWT issuance', outline=GREEN)

    service_box(d,(1260,290,1600,410),'Event Detection API','FastAPI ingress\nPOST /predict, GET /events, health/status', outline=DO_BLUE)
    service_box(d,(1700,290,2010,410),'Redis Broker','Celery queue / result backend', outline=AMBER)
    service_box(d,(2070,290,2270,410),'Celery Worker','async classification task', outline=GREEN)
    service_box(d,(1260,560,1600,680),'Event Detection DB','queued/completed events\nstatus, label, confidence', outline=BLUE)
    service_box(d,(1700,560,2270,680),'ONNX Runtime + Model Artifacts','event_classifier.onnx\nmetadata sidecar', outline=PURPLE)
    service_box(d,(1260,850,2270,980),'Result Exposure','GET /events polling today\nfuture live-push channel possible', outline=RED)

    arrow(d,(470,350),(1260,350),label='clip / video input',color=BLACK,width=4,lf=font(20),label_fill=WHITE)
    arrow(d,(470,560),(560,560),label='submit classification request',color=PURPLE,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(900,560),(1260,350),label='async POST /predict over HTTPS + JWT',color=RED,width=5,lf=font(18),label_fill=WHITE)
    arrow(d,(1600,350),(1700,350),label='enqueue task',color=AMBER,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(2010,350),(2070,350),label='consume task',color=GREEN,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(2070,470),(1885,560),label='load model + run classification',color=PURPLE,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(1260,430),(1260,560),label='persist queued event',color=BLUE,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(2070,430),(1600,620),label='update status / label / confidence',color=GREEN,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(1600,620),(1260,915),label='classification result becomes retrievable',color=RED,width=4,lf=font(18),label_fill=WHITE)
    arrow(d,(1260,915),(470,770),label='downstream reuse: alerting, analytics, monitoring timeline',color=TEAL,width=5,lf=font(18),label_fill=WHITE)

    note = 'This overview now shows the full engineering loop requested by the supervisor: clip input, asynchronous call to the AI service, classification result, persisted event, and downstream notification / analytics reuse.'
    box(d,(220,1230,2180,1340), body=note, fill='#f8fafc', outline=BORDER, body_font=font(22), body_color=MUTED, align='center')

    img.save(OUTDIR/'ai_system_overview_v2.png')


def runtime_sequence():
    W,H = 2500,1400
    img = Image.new('RGB',(W,H),WHITE)
    d = ImageDraw.Draw(img)
    header(d,W,'Runtime Inference Sequence — Clip Submission, Async Classification, and Downstream Reuse')

    lanes = [
        ('AWS Caller', 140),
        ('Event Detection API', 600),
        ('Redis Broker', 1030),
        ('Celery Worker', 1410),
        ('Event Detection DB', 1810),
        ('Notification / Analytics', 2190),
    ]
    lane_w = 250
    top = 180
    bottom = 1260
    for title, x in lanes:
        box(d,(x,180,x+lane_w,250), title=title, fill=WHITE, outline=BORDER, title_fill=GRAYBOX, title_color=BLACK, title_h=58)
        cx = x + lane_w/2
        d.line((cx,250,cx,bottom), fill='#94a3b8', width=3)

    steps = [
        ((265,320),(725,320),'1. Submit clip source + camera context\nPOST /predict'),
        ((725,380),(1935,380),'2. Verify JWT, create queued event'),
        ((725,450),(1155,450),'3. Enqueue async task'),
        ((1155,520),(1535,520),'4. Deliver task'),
        ((1535,590),(1935,590),'5. Load model, classify clip'),
        ((1535,660),(1935,660),'6. Update event: completed / label / confidence'),
        ((725,760),(1935,760),'7. Poll or retrieve persisted result via GET /events'),
        ((1935,860),(2315,860),'8. Reuse event in notification and analytics workflows'),
        ((2315,940),(725,940),'9. Return event timeline / alert-ready data'),
    ]
    colors = [PURPLE, BLUE, AMBER, GREEN, PURPLE, GREEN, BLUE, TEAL, TEAL]
    for (p1,p2,label), c in zip(steps, colors):
        arrow(d,p1,p2,color=c,width=4,label=label,lf=font(18),label_fill=WHITE)

    # async region box
    d.rounded_rectangle((980,300,2050,720), radius=18, outline=RED, width=3)
    d.text((1000,285),'Asynchronous inference boundary', font=font(22, True), fill=RED)

    # notes
    box(d,(180,1080,880,1235), title='Input', body='Clip/video source enters from an AWS-side caller after permission, membership, and subscription checks have already been performed.', fill=GRAYBOX, outline=BORDER, title_fill=GRAYBOX, title_color=BLACK, body_font=font(20), body_color=BLACK, align='left')
    box(d,(930,1080,1620,1235), title='Persisted Result', body='The AI service does not only return a label; it stores a durable event record with status, confidence, and retrieval metadata.', fill=GRAYBOX, outline=BORDER, title_fill=GRAYBOX, title_color=BLACK, body_font=font(20), body_color=BLACK, align='left')
    box(d,(1670,1080,2360,1235), title='Downstream Reuse', body='Notification and analytics modules consume the stored classification event later, which ties the AI sprint back to the global VigileEye system.', fill=GRAYBOX, outline=BORDER, title_fill=GRAYBOX, title_color=BLACK, body_font=font(20), body_color=BLACK, align='left')

    img.save(OUTDIR/'runtime_inference_sequence_v2.png')


def main():
    static_context()
    global_use_case()
    sprint2_class_grouped()
    ai_overview()
    runtime_sequence()
    print('Generated diagrams in', OUTDIR)

if __name__ == '__main__':
    main()
