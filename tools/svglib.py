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


def rr(x, y, w, h, r):
    """rounded rect path; r = number or (tl,tr,br,bl)"""
    if not isinstance(r, (tuple, list)): r = (r, r, r, r)
    tl, tr, br, bl = r
    d = f"M{x+tl},{y} L{x+w-tr},{y} "
    d += (f"A{tr},{tr} 0 0 1 {x+w},{y+tr} " if tr else "")
    d += f"L{x+w},{y+h-br} " + (f"A{br},{br} 0 0 1 {x+w-br},{y+h} " if br else "")
    d += f"L{x+bl},{y+h} " + (f"A{bl},{bl} 0 0 1 {x},{y+h-bl} " if bl else "")
    d += f"L{x},{y+tl} " + (f"A{tl},{tl} 0 0 1 {x+tl},{y} " if tl else "") + "Z"
    return d

class Ill:
    """finished-item illustration"""
    def __init__(s, w, h):
        s.w, s.h = w, h; s.k = max(w, h) / 300; s.el = []; s.pad = 18 * s.k
    def body(s, d, fill="#c08a5b", stroke="#7a4f30"):
        s.el.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{1.4*s.k:.2f}" stroke-linejoin="round"/>')
    def stitch(s, d, color="#f6efe4"):
        s.el.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{1.1*s.k:.2f}" stroke-dasharray="{3.2*s.k:.1f} {2.4*s.k:.1f}" stroke-linecap="round"/>')
    def line(s, x1, y1, x2, y2, color="#7a4f30", w=1.2):
        s.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w*s.k:.2f}" stroke-linecap="round"/>')
    def metal(s, x, y, r):
        s.el.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d9c27a" stroke="#8a7333" stroke-width="{0.9*s.k:.2f}"/>')
    def ring(s, x, y, r, w=2.2):
        s.el.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#a8a8a8" stroke-width="{w*s.k:.2f}"/>')
    def raw(s, t): s.el.append(t)
    def save(s, fn):
        p = s.pad; W = s.w + 2*p; H = s.h + 2*p
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-p:.1f} {-p:.1f} {W:.1f} {H:.1f}" width="{W*2:.0f}" height="{H*2:.0f}">'
               f'<rect x="{-p}" y="{-p}" width="{W}" height="{H}" fill="#efe6da"/>'
               f'<ellipse cx="{s.w/2}" cy="{s.h+p*0.45}" rx="{s.w*0.45}" ry="{p*0.25}" fill="#00000014"/>' + "".join(s.el) + "</svg>")
        open(fn, "w").write(svg)
