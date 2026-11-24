"""縫い線・注記つきの作図クラス T（svglib.S を拡張）"""
from svglib import S


class T(S):
    def stitch(s, d):
        s.el.append(f'<path d="{d}" fill="none" stroke="#2b211b" stroke-width="{0.7*s.k:.2f}" stroke-dasharray="{2.5*s.k:.1f} {2.5*s.k:.1f}"/>')

    def sline(s, x1, y1, x2, y2): s.stitch(f"M{x1},{y1} L{x2},{y2}")

    def note(s, x, y, lines, size=0.62):
        for i, t in enumerate(lines):
            s.text(x, y + i * 13 * s.k * size * 1.45, t, size, "#5b3a29", anchor="start")

    def save(s, fn, title):
        super().save(fn, title)
        t = open(fn).read().replace("赤点線＝折り線／○＝金具位置", "赤点線＝折り線／黒の細点線＝縫い線／○＝金具位置")
        open(fn, "w").write(t)
