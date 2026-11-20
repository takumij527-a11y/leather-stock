import math, json
class S:
    def __init__(s, w, h, pad=None):
        s.w, s.h = w, h; s.k = max(w, h) / 600; s.el = []
        s.pad = pad if pad is not None else 60 * s.k
    def cut(s, d): s.el.append(f'<path d="{d}" fill="#f3e6d6" stroke="#2b211b" stroke-width="{1.6*s.k:.2f}" stroke-linejoin="round"/>')
    def poly(s, pts): s.cut("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z")
    def fold(s, x1, y1, x2, y2): s.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b5552e" stroke-width="{1.1*s.k:.2f}" stroke-dasharray="{8*s.k:.1f} {5*s.k:.1f}"/>')
    def hole(s, x, y, r=5): s.el.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#2b211b" stroke-width="{1*s.k:.2f}"/>')
    def text(s, x, y, t, size=1.0, color="#5b3a29", bold=False, anchor="middle"):
        s.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{15*s.k*size:.1f}" fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" font-weight="{700 if bold else 400}" font-family="sans-serif">{t}</text>')
    def dim(s, x1, y1, x2, y2, label, off):
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
        a1 = (x1 + nx * off, y1 + ny * off); a2 = (x2 + nx * off, y2 + ny * off)
        c = "#2f5d8a"; sw = 0.9 * s.k; e = 4 * s.k if off > 0 else -4 * s.k
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{a1[0]+nx*e:.1f}" y2="{a1[1]+ny*e:.1f}" stroke="{c}" stroke-width="{sw*0.6:.2f}"/>')
        s.el.append(f'<line x1="{x2:.1f}" y1="{y2:.1f}" x2="{a2[0]+nx*e:.1f}" y2="{a2[1]+ny*e:.1f}" stroke="{c}" stroke-width="{sw*0.6:.2f}"/>')
        s.el.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}" stroke="{c}" stroke-width="{sw:.2f}"/>')
        ah = 7 * s.k
        for (px, py), sgn in ((a1, 1), (a2, -1)):
            bx, by = px + ux * ah * sgn, py + uy * ah * sgn
            s.el.append(f'<path d="M{px:.1f},{py:.1f} L{bx+nx*ah*0.35:.1f},{by+ny*ah*0.35:.1f} L{bx-nx*ah*0.35:.1f},{by-ny*ah*0.35:.1f} Z" fill="{c}"/>')
        mx, my = (a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90 or ang <= -90: ang += 180
        t = 9 * s.k * (1 if off > 0 else -1)
        tx, ty = mx + nx * t, my + ny * t
        s.el.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{14*s.k:.1f}" fill="{c}" text-anchor="middle" dominant-baseline="middle" font-family="sans-serif" font-weight="700" transform="rotate({ang:.1f} {tx:.1f} {ty:.1f})" paint-order="stroke" stroke="#fff" stroke-width="{3*s.k:.1f}">{label}</text>')
    def save(s, fn, title):
        p = s.pad; W = s.w + 2 * p; H = s.h + 2 * p + 52 * s.k
        legend = (f'<text x="{-p+10*s.k:.1f}" y="{s.h+p+22*s.k:.1f}" font-size="{12*s.k:.1f}" fill="#8a7a6d" font-family="sans-serif">{title}</text>'
                  f'<text x="{-p+10*s.k:.1f}" y="{s.h+p+40*s.k:.1f}" font-size="{11*s.k:.1f}" fill="#8a7a6d" font-family="sans-serif">単位mm／実線＝裁ち線／赤点線＝折り線／○＝金具位置／寸法は推定</text>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-p:.1f} {-p:.1f} {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}">'
               f'<rect x="{-p}" y="{-p}" width="{W}" height="{H}" fill="#fffdf9"/>' + "".join(s.el) + legend + "</svg>")
        open(fn, "w").write(svg)

# 001 basket bag
s = S(600, 860)
s.cut("M0,0 L360,0 L360,250 L265,250 A60,60 0 0 0 205,310 L205,490 A60,60 0 0 0 265,550 L360,550 L360,800 L0,800 L0,550 L95,550 A60,60 0 0 0 155,490 L155,310 A60,60 0 0 0 95,250 L0,250 Z")
s.text(180, 125, "後ろ", 1.3, bold=True); s.text(180, 675, "前", 1.3, bold=True); s.text(290, 400, "持ち手", 1.0); s.text(290, 430, "フィレットR60", 0.8, "#2f5d8a")
s.text(180, 170, "①本体 ×1", 0.9, "#8a7a6d", bold=True)
s.dim(0, 0, 360, 0, "360", -22); s.dim(360, 0, 360, 250, "250", -22); s.dim(360, 550, 360, 800, "250", -22)
s.dim(155, 310, 155, 490, "180", 30); s.dim(155, 340, 205, 340, "50", -14)
s.dim(0, 800, 95, 800, "95", 22); s.dim(0, 0, 0, 800, "800", 30)
s.cut("M440,0 L570,0 L570,860 L440,860 Z"); s.text(505, 430, "②通しマチ ×1", 0.9, bold=True)
s.dim(440, 0, 570, 0, "130", -22); s.dim(570, 0, 570, 860, "860 (250+360+250)", -22)
s.fold(440, 250, 570, 250); s.fold(440, 610, 570, 610)
s.save("app/pat/001.svg", "仕上がり 幅360×高さ250×奥行130（推定で設定）")

# 002 box A
s = S(220, 180)
s.poly([(50,0),(170,0),(170,50),(220,0),(220,180),(170,130),(170,180),(50,180),(50,130),(0,180),(0,0),(50,50)])
for a in [(50,50,170,50),(50,130,170,130),(50,50,50,130),(170,50,170,130),(0,50,50,50),(170,50,220,50),(0,130,50,130),(170,130,220,130)]: s.fold(*a)
s.text(110, 90, "底", 1.2, bold=True); s.text(110, 25, "前壁", 1.0); s.text(110, 155, "後ろ壁", 1.0); s.text(25, 90, "横", 1.0); s.text(195, 90, "横", 1.0)
s.dim(50, 0, 170, 0, "120", -14); s.dim(220, 50, 220, 130, "80", -14); s.dim(220, 0, 220, 50, "50", -14); s.dim(220, 130, 220, 180, "50", -14)
s.dim(0, 180, 220, 180, "220", 18); s.dim(0, 0, 0, 180, "180", 18)
s.save("app/pat/002.svg", "Aタイプ例：仕上がり 120×80×高さ50")

# 003 trapezoid tote
s = S(900, 430)
s.cut("M90,0 L310,0 Q350,0 357,39.4 L400,280 L0,280 L43,39.4 Q50,0 90,0 Z")
s.text(200, 150, "①前・後ろ ×2", 1.0, bold=True)
s.dim(50, 0, 350, 0, "300", -20); s.dim(0, 280, 400, 280, "400", 20); s.dim(400, 0, 400, 280, "280", -25)
s.text(345, 45, "R40", 0.8, "#2f5d8a")
s.hole(130, 70, 4); s.hole(270, 70, 4); s.text(200, 70, "持ち手位置（中心から±70）", 0.75, "#8a7a6d")
s.poly([(450,274),(600,274),(525,0)]); s.text(525, 200, "②マチ ×2", 0.9, bold=True)
s.dim(450, 274, 600, 274, "150", 20); s.dim(600, 274, 525, 0, "284", 18)
s.cut("M650,0 L800,0 L800,400 L650,400 Z"); s.text(725, 200, "③底 ×1", 0.9, bold=True)
s.dim(650, 0, 800, 0, "150", -20); s.dim(800, 0, 800, 400, "400", -20)
s.cut("M70,337.5 L350,337.5 C380,337.5 385,325 400,325 A25,25 0 0 1 400,375 C385,375 380,362.5 350,362.5 L70,362.5 C40,362.5 35,375 20,375 A25,25 0 0 1 20,325 C35,325 40,337.5 70,337.5 Z")
s.text(525, 355, "④持ち手 ×2", 0.85, bold=True)
s.dim(-5, 375, 425, 375, "430", 14); s.dim(260, 337.5, 260, 362.5, "25", -10); s.dim(425, 325, 425, 375, "50", -14)
s.save("app/pat/003.svg", "仕上がり 下幅400・上幅300×高さ280×マチ150")

# 004 triangle bag
s = S(720, 460)
s.poly([(0,190),(270,190),(135,424)]); s.text(135, 260, "①前 ×1", 1.0, bold=True)
s.dim(0, 190, 270, 190, "270", -18); s.dim(270, 190, 135, 424, "270", -18); s.dim(0, 190, 0, 424, "234", 20)
s.poly([(310,190),(580,190),(445,424)]); s.cut("M310,190 L310,155 L445,0 L580,155 L580,190 Z")
s.fold(310, 190, 580, 190); s.fold(310, 155, 580, 155)
s.text(445, 260, "②後ろ＋フラップ ×1", 1.0, bold=True); s.text(445, 110, "フラップ", 0.9)
s.dim(580, 155, 580, 190, "35", -16); s.dim(580, 0, 580, 155, "155", -16); s.hole(445, 30, 5)
s.cut("M630,0 L665,0 L665,272 L630,272 Z"); s.text(647, 136, "③マチ×2", 0.8, bold=True)
s.dim(630, 0, 665, 0, "35", -16); s.dim(665, 0, 665, 272, "272", -16)
s.cut("M690,0 L710,0 L710,70 L690,70 Z"); s.fold(690, 35, 710, 35); s.text(700, 90, "④タブ×2", 0.7, bold=True)
s.dim(710, 0, 710, 70, "70", -12)
s.save("app/pat/004.svg", "仕上がり 上辺270×高さ234×マチ35")

# 005 box coin case
s = S(150, 190)
s.cut("M15,0 L75,0 A15,15 0 0 1 90,15 L90,190 L0,190 L0,15 A15,15 0 0 1 15,0 Z")
for y in (45, 115, 135): s.fold(0, y, 90, y)
s.text(45, 25, "フラップ", 0.9); s.text(45, 80, "後ろ", 1.0, bold=True); s.text(45, 125, "底", 0.8); s.text(45, 160, "前", 1.0, bold=True)
s.hole(45, 12, 3); s.hole(45, 170, 3)
s.dim(0, 0, 90, 0, "90", -12); s.dim(90, 0, 90, 45, "45", -12); s.dim(90, 45, 90, 115, "70", -12); s.dim(90, 115, 90, 135, "20", -12); s.dim(90, 135, 90, 190, "55", -12)
s.dim(0, 0, 0, 190, "190", 14)
s.poly([(120,190),(140,190),(130,135)]); s.text(130, 120, "②横マチ×2", 0.75, bold=True)
s.dim(120, 190, 140, 190, "20", 12); s.dim(140, 190, 130, 135, "56", -10)
s.save("app/pat/005.svg", "仕上がり 幅90×高さ70×奥行20（外装・内装 各1枚）")

# 006 envelope coin case
s = S(210, 155)
s.poly([(70,0),(140,0),(155,15),(155,60),(210,75),(210,130),(155,130),(155,145),(145,155),(65,155),(55,145),(55,130),(0,130),(0,75),(55,60),(55,15)])
for a in [(55,60,55,130),(155,60,155,130),(55,60,155,60),(55,130,155,130)]: s.fold(*a)
s.text(105, 30, "フラップ", 0.9); s.text(105, 95, "後ろ", 1.0, bold=True); s.text(27, 105, "左羽根", 0.75); s.text(182, 105, "右羽根", 0.75); s.text(105, 142, "底", 0.75)
s.hole(105, 15, 3)
s.dim(55, 0, 155, 0, "100", -12); s.dim(0, 130, 55, 130, "55", 12); s.dim(155, 130, 210, 130, "55", 12)
s.dim(210, 0, 210, 60, "60", -12); s.dim(210, 60, 210, 130, "70", -12); s.dim(155, 130, 155, 155, "25", -62)
s.dim(0, 75, 0, 130, "55", 12); s.dim(0, 155, 210, 155, "210", 18)
s.text(160, 6, "C15", 0.75, "#2f5d8a")
s.save("app/pat/006.svg", "仕上がり 幅100×高さ70（羽根の重なり10）")
print("ok")

# 007 card case with band
s = S(260, 150)
s.cut("M0,76 L0,55 Q0,40 25,32 L25,25 A25,25 0 0 1 75,25 L75,32 Q100,40 100,55 L100,146 L0,146 Z")
s.fold(0, 70, 100, 70); s.fold(0, 76, 100, 76)
s.text(50, 45, "フラップ", 0.9); s.text(50, 110, "後ろ", 1.0, bold=True); s.text(50, 128, "①後ろ＋フラップ ×1", 0.75, "#8a7a6d")
s.dim(0, 146, 100, 146, "100", 14); s.dim(100, 76, 100, 146, "70", -14); s.dim(100, 70, 100, 76, "6", -30); s.dim(100, 0, 100, 70, "70", -14)
s.dim(25, 25, 75, 25, "50", 12); s.text(50, 8, "先端R25", 0.7, "#2f5d8a")
s.cut("M140,76 L240,76 L240,140 L140,140 Z"); s.text(190, 108, "②前 ×1", 1.0, bold=True)
s.dim(140, 140, 240, 140, "100", 14); s.dim(240, 76, 240, 140, "64", -14)
s.cut("M140,20 L240,20 L240,42 L140,42 Z"); s.text(190, 31, "③ベルト ×1", 0.8, bold=True)
s.dim(140, 20, 240, 20, "100", -10); s.dim(240, 20, 240, 42, "22", -14)
s.save("app/pat/007.svg", "仕上がり 幅100×高さ70（カード86×54が入る内寸92×62）")
