#!/usr/bin/env python3
"""Generate OneWay FX Volume II — Reading the Story Behind Price Action."""

import math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    NextPageTemplate, PageBreak, KeepTogether, Flowable
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon, Circle

# ---------------------------------------------------------------------------
# Brand palette (shared with Volume I)
# ---------------------------------------------------------------------------
NAVY = HexColor('#0B2545')
NAVY_DARK = HexColor('#071A33')
GOLD = HexColor('#C9962B')
GOLD_LIGHT = HexColor('#E7C878')
BULL_GREEN = HexColor('#26A69A')
BEAR_RED = HexColor('#EF5350')
BULL_STROKE = HexColor('#0F7A6B')
BEAR_STROKE = HexColor('#B33330')
BEAR_DARK_RED = HexColor('#8B1E1E')
CONTEXT_GRAY = HexColor('#BAC4D0')
CONTEXT_STROKE = HexColor('#96A2B2')
INK = HexColor('#1B2430')
SUBTLE = HexColor('#5B6B7C')
PANEL_BG = HexColor('#F3F6FA')
PANEL_LINE = HexColor('#D8E0EA')
WARN_BG = HexColor('#FDF1E8')
WARN_LINE = HexColor('#E6A15C')
CHART_BG = HexColor('#FCFDFE')
CHART_BORDER = HexColor('#E1E7EF')
CHART_GRID = HexColor('#EBEFF4')
SHIFT_VIOLET = HexColor('#7C5CBF')
TRAP_ORANGE = HexColor('#C9722F')
GOOD_GREEN = HexColor('#178A5B')
BAD_RED = HexColor('#B3271E')

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

OUT_PATH = "OneWayFX_Reading_the_Story_Behind_Price_Action_Vol2.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='CoverTitle', fontName='Helvetica-Bold', fontSize=27, leading=33,
    textColor=colors.white, alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='CoverSubtitle', fontName='Helvetica', fontSize=14, leading=19,
    textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=4
))
styles.add(ParagraphStyle(
    name='CoverFooter', fontName='Helvetica', fontSize=10.5, leading=14,
    textColor=HexColor('#C7D2E0'), alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    name='ChapterKicker', fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=GOLD, alignment=TA_LEFT, spaceAfter=2, tracking=1
))
styles.add(ParagraphStyle(
    name='ChapterTitle', fontName='Helvetica-Bold', fontSize=22, leading=27,
    textColor=NAVY, alignment=TA_LEFT, spaceAfter=14, spaceBefore=0,
))
styles.add(ParagraphStyle(
    name='SectionHeading', fontName='Helvetica-Bold', fontSize=15, leading=19,
    textColor=NAVY, spaceBefore=16, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name='PatternTitle', fontName='Helvetica-Bold', fontSize=16, leading=20,
    textColor=colors.white, spaceBefore=0, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name='PatternSub', fontName='Helvetica-Oblique', fontSize=9.6, leading=13,
    textColor=HexColor('#DCE6F2'), spaceBefore=1,
))
styles.add(ParagraphStyle(
    name='SubHeading', fontName='Helvetica-Bold', fontSize=11.3, leading=15,
    textColor=NAVY, spaceBefore=10, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name='Body', fontName='Helvetica', fontSize=10.1, leading=14.6,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name='BulletItem', fontName='Helvetica', fontSize=10.1, leading=14.2,
    textColor=INK, alignment=TA_LEFT, spaceAfter=3, leftIndent=14,
))
styles.add(ParagraphStyle(
    name='Caption', fontName='Helvetica-Oblique', fontSize=8.8, leading=11.8,
    textColor=SUBTLE, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name='WarnHead', fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=HexColor('#8A4B14'),
))
styles.add(ParagraphStyle(
    name='WarnBody', fontName='Helvetica', fontSize=9.6, leading=13.8,
    textColor=HexColor('#5C3A16'), alignment=TA_JUSTIFY,
))
styles.add(ParagraphStyle(
    name='TOCEntry', fontName='Helvetica', fontSize=10.6, leading=18,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name='TOCSub', fontName='Helvetica', fontSize=9.4, leading=15,
    textColor=SUBTLE, leftIndent=10,
))
styles.add(ParagraphStyle(
    name='TOCPart', fontName='Helvetica-Bold', fontSize=11.5, leading=24,
    textColor=NAVY, spaceBefore=8,
))
styles.add(ParagraphStyle(
    name='GlanceLabel', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
    textColor=SUBTLE,
))
styles.add(ParagraphStyle(
    name='GlanceValue', fontName='Helvetica-Bold', fontSize=10.1, leading=13,
    textColor=NAVY,
))
styles.add(ParagraphStyle(
    name='GlossaryEntry', fontName='Helvetica', fontSize=9.6, leading=13.6,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name='ModuleNum', fontName='Helvetica-Bold', fontSize=46, leading=46,
    textColor=HexColor('#1B3B66'), alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name='RuleText', fontName='Helvetica-Bold', fontSize=11.2, leading=15,
    textColor=NAVY, alignment=TA_LEFT, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name='RuleWhy', fontName='Helvetica', fontSize=9.6, leading=13.6,
    textColor=SUBTLE, alignment=TA_LEFT, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name='CaseTag', fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=colors.white,
))

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _hex(c):
    return '#%02X%02X%02X' % (round(c.red * 255), round(c.green * 255), round(c.blue * 255))


class HR(Flowable):
    def __init__(self, width, color=PANEL_LINE, thickness=0.75, space_before=4, space_after=4):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after
        self.height = thickness + space_before + space_after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after
        self.canv.line(0, y, self.width, y)


def gold_rule(width=468):
    return HR(width, color=GOLD, thickness=2, space_before=0, space_after=14)


def chapter_block(kicker, title):
    return [Paragraph(kicker.upper(), styles['ChapterKicker']),
            Paragraph(title, styles['ChapterTitle']),
            gold_rule()]


def warn_box(title, body_lines, bg=WARN_BG, line=WARN_LINE, head_style='WarnHead', body_style='WarnBody', bullet=True):
    inner = [Paragraph(title, styles[head_style])]
    for line_text in body_lines:
        prefix = '•  ' if bullet else ''
        inner.append(Paragraph(f'{prefix}{line_text}', styles[body_style]))
    t = Table([[inner]], colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 1, line),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


def module_opener(number, title, blurb):
    """A visually distinct module-opener block: big number + title + one-line blurb."""
    num = Paragraph(f'{number:02d}', styles['ModuleNum'])
    head = [Paragraph(f'MODULE {number}', styles['ChapterKicker']),
            Paragraph(title, styles['ChapterTitle']),
            Paragraph(blurb, styles['Body'])]
    t = Table([[num, head]], colWidths=[64, 404])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    return [t, gold_rule()]


def topic_heading(text):
    return Paragraph(text, styles['SectionHeading'])


# ---------------------------------------------------------------------------
# Drawing primitives shared by every diagram in this book
# ---------------------------------------------------------------------------

def _chart_panel(d, width, height):
    d.add(Rect(1, 4, width - 2, height - 8, fillColor=CHART_BG,
               strokeColor=CHART_BORDER, strokeWidth=0.9))
    for frac in (0.22, 0.42, 0.62, 0.82):
        gy = 4 + frac * (height - 8)
        d.add(Line(9, gy, width - 9, gy, strokeColor=CHART_GRID, strokeWidth=0.6,
                   strokeDashArray=[2, 2.5]))


def _xy(width, height, left=20, right=20, top=26, bottom=26):
    plot_w = width - left - right
    plot_h = height - top - bottom

    def X(frac):
        return left + frac * plot_w

    def Y(v):
        return bottom + (v / 100.0) * plot_h

    return X, Y


def _label(d, x, y, text, size=7.6, color=SUBTLE, bold=False, anchor='middle'):
    d.add(String(x, y, text, fontSize=size, fillColor=color,
                 fontName='Helvetica-Bold' if bold else 'Helvetica',
                 textAnchor=anchor))


def _arrow(d, x0, y0, x1, y1, color, dashed=True, width=1.8):
    d.add(Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=width,
               strokeDashArray=[3, 2.4] if dashed else None))
    ang = math.atan2(y1 - y0, x1 - x0)
    size = 6.5
    a = 0.42
    p2 = (x1 - size * math.cos(ang - a), y1 - size * math.sin(ang - a))
    p3 = (x1 - size * math.cos(ang + a), y1 - size * math.sin(ang + a))
    d.add(Polygon(points=[x1, y1, p2[0], p2[1], p3[0], p3[1]],
                  fillColor=color, strokeColor=color))


def _tri_arrow(d, x, y, direction, color, size=5.5):
    """Small filled triangle pointing up or down, used to flag bounce/reject points."""
    if direction == 'up':
        pts = [x, y + size, x - size * 0.8, y - size * 0.3, x + size * 0.8, y - size * 0.3]
    else:
        pts = [x, y - size, x - size * 0.8, y + size * 0.3, x + size * 0.8, y + size * 0.3]
    d.add(Polygon(points=pts, fillColor=color, strokeColor=color))


# ---------------------------------------------------------------------------
# Structure / level diagram engine (Modules 1, 2, 8, 9, 10, 11)
# ---------------------------------------------------------------------------

def structure_drawing(points, width=468, height=188, ref_line=None, ref_label=None,
                       ref_diag=None, ref_color=None, zone=None, zone_color=None,
                       break_from=None, annotation=None, annotation_color=None,
                       trend_label=None, arrows=None, path_color=None, levels=None):
    """points: list of (frac 0-1, v 0-100, label_or_None, kind 'high'/'low'/None).
    levels: optional list of (v, label, color) solid reference lines, e.g. for
    marking Entry / Stop Loss / Take Profit."""
    d = Drawing(width, height)
    _chart_panel(d, width, height)
    X, Y = _xy(width, height)

    if zone is not None:
        lo, hi = zone
        d.add(Rect(X(0), Y(lo), X(1) - X(0), Y(hi) - Y(lo),
                   fillColor=zone_color or GOLD_LIGHT, fillOpacity=0.20, strokeColor=None))

    if levels:
        for v, lv_label, lv_color in levels:
            ly = Y(v)
            d.add(Line(X(0), ly, X(1), ly, strokeColor=lv_color, strokeWidth=1.1))
            _label(d, X(1) - 4, ly + 3, lv_label, size=7.4, color=lv_color, bold=True, anchor='end')

    if ref_line is not None:
        ry = Y(ref_line)
        d.add(Line(X(0), ry, X(1), ry, strokeColor=ref_color or GOLD, strokeWidth=1.1,
                   strokeDashArray=[3, 2.5]))
        if ref_label:
            _label(d, X(0) + 4, ry + 5, ref_label, size=7.4, color=ref_color or GOLD,
                   bold=True, anchor='start')

    if ref_diag is not None:
        (fx0, v0), (fx1, v1) = ref_diag
        d.add(Line(X(fx0), Y(v0), X(fx1), Y(v1), strokeColor=ref_color or GOLD,
                   strokeWidth=1.1, strokeDashArray=[3, 2.5]))

    pts_xy = [(X(p[0]), Y(p[1])) for p in points]
    for i in range(len(pts_xy) - 1):
        x0, y0 = pts_xy[i]
        x1, y1 = pts_xy[i + 1]
        seg_color = path_color or NAVY
        dash = None
        if break_from is not None and i >= break_from:
            seg_color = annotation_color or GOLD
            dash = [3, 2.5]
        d.add(Line(x0, y0, x1, y1, strokeColor=seg_color, strokeWidth=1.6, strokeDashArray=dash))

    for i, p in enumerate(points):
        frac, v, label, kind = p
        x, y = pts_xy[i]
        if label:
            color = BULL_GREEN if label in ('HH', 'HL') else BEAR_RED if label in ('LH', 'LL') else NAVY
        else:
            color = CONTEXT_STROKE
        d.add(Circle(x, y, 3.0, fillColor=color, strokeColor=color))
        if label:
            ly = y + 11 if kind == 'high' else y - 15
            _label(d, x, ly, label, size=7.4, color=color, bold=True)

    if arrows:
        for idx, direction, acolor in arrows:
            x, y = pts_xy[idx]
            off = 11 if direction == 'up' else -11
            _tri_arrow(d, x, y + off, direction, acolor)

    if annotation:
        text, acolor = annotation
        lastx, lasty = pts_xy[-1]
        anchor = 'start' if lastx < width - 84 else 'end'
        ly = lasty + 12 if lasty < height * 0.62 else lasty - 16
        _label(d, min(lastx + 6, width - 10), ly, text, size=8.6, color=acolor, bold=True, anchor=anchor)

    if trend_label:
        _label(d, 14, height - 12, trend_label, size=7.8, color=SUBTLE, bold=True, anchor='start')

    return d


def split_drawing_row(left_drawing, left_caption, right_drawing, right_caption, gap=14):
    row = Table(
        [[left_drawing, right_drawing],
         [Paragraph(left_caption, styles['Caption']), Paragraph(right_caption, styles['Caption'])]],
        colWidths=[(468 - gap) / 2.0, (468 - gap) / 2.0])
    row.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), gap),
        ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return row


# ---------------------------------------------------------------------------
# Candlestick diagram engine (Modules 4, 5, 10, 11) — ported from Volume I
# ---------------------------------------------------------------------------

def _candle(d, cx, o, c, hi, lo, w, y0, yscale, fill=None, muted=False):
    def Y(v):
        return y0 + v * yscale
    bull = c >= o
    if muted:
        fill_color = CONTEXT_GRAY
        stroke = CONTEXT_STROKE
        sw = 0.6
        wick_w = 0.9
    else:
        if fill:
            fill_color, stroke = fill, HexColor('#1B2430')
        elif bull:
            fill_color, stroke = BULL_GREEN, BULL_STROKE
        else:
            fill_color, stroke = BEAR_RED, BEAR_STROKE
        sw = 0.7
        wick_w = 1.15
    top, bottom = max(o, c), min(o, c)
    d.add(Line(cx, Y(lo), cx, Y(hi), strokeColor=stroke, strokeWidth=wick_w))
    body_h = max(Y(top) - Y(bottom), 1.4)
    body_w = w * 0.62 if not muted else w
    d.add(Rect(cx - body_w / 2.0, Y(bottom), body_w, body_h, fillColor=fill_color,
                strokeColor=stroke, strokeWidth=sw))


def _ghost_candle(d, cx, o, c, hi, lo, w, y0, yscale, color):
    def Y(v):
        return y0 + v * yscale
    top, bottom = max(o, c), min(o, c)
    d.add(Line(cx, Y(lo), cx, Y(hi), strokeColor=color, strokeWidth=1.0, strokeDashArray=[2, 2]))
    body_h = max(Y(top) - Y(bottom), 1.4)
    body_w = w * 0.62
    d.add(Rect(cx - body_w / 2.0, Y(bottom), body_w, body_h, fillColor=color,
               fillOpacity=0.10, strokeColor=color, strokeWidth=1.0, strokeDashArray=[2, 2]))


BIAS_STYLE = {
    'bullish': (BULL_GREEN, 'Bullish Reversal'),
    'bearish': (BEAR_DARK_RED, 'Bearish Reversal'),
    'neutral': (HexColor('#8A93A3'), 'Indecision'),
}


def downtrend_context(end_level=68, n=7):
    top = min(97, end_level + 3 + (n - 1) * 6)
    bottom = end_level + 3
    step = (top - bottom) / (n - 1) if n > 1 else 6
    out = []
    lvl = top
    for i in range(n):
        o = lvl
        c = lvl - step * 0.72
        hi = o + step * 0.22
        lo = c - step * 0.28
        out.append((o, c, hi, lo))
        lvl = c - step * 0.1
    return out


def uptrend_context(end_level=32, n=7):
    bottom = max(3, end_level - 3 - (n - 1) * 6)
    top = end_level - 3
    step = (top - bottom) / (n - 1) if n > 1 else 6
    out = []
    lvl = bottom
    for i in range(n):
        o = lvl
        c = lvl + step * 0.72
        hi = c + step * 0.22
        lo = o - step * 0.28
        out.append((o, c, hi, lo))
        lvl = c + step * 0.1
    return out


def pattern_drawing(context, pattern, bias, trend_label, bias_label=None,
                     width=468, height=192):
    d = Drawing(width, height)
    y0 = 34
    yscale = 1.1

    def Y(v):
        return y0 + v * yscale

    d.add(Rect(1, 4, width - 2, height - 8, fillColor=CHART_BG,
               strokeColor=CHART_BORDER, strokeWidth=0.9))
    for lvl in (20, 40, 60, 80):
        gy = Y(lvl)
        d.add(Line(9, gy, width - 9, gy, strokeColor=CHART_GRID, strokeWidth=0.6,
                   strokeDashArray=[2, 2.5]))
    d.add(Line(8, 22, width - 8, 22, strokeColor=PANEL_LINE, strokeWidth=0.75))

    label_row = height - 12
    cctx_w = 7
    step = 13.5
    x = 20
    for (o, c, hi, lo) in context:
        _candle(d, x, o, c, hi, lo, cctx_w, y0, yscale, muted=True)
        x += step
    ctx_last_x = x - step
    ctx_first_x = 20
    _label(d, (ctx_first_x + ctx_last_x) / 2.0, label_row, trend_label,
           size=8, color=SUBTLE, bold=True)

    divider_x = ctx_last_x + cctx_w / 2.0 + 9
    d.add(Line(divider_x, 12, divider_x, height - 18, strokeColor=GOLD_LIGHT,
               strokeWidth=0.8, strokeDashArray=[2, 2.5]))

    x = divider_x + 17
    n = len(pattern)
    if n == 1:
        cw, gap = 28, 0
    elif n == 2:
        cw, gap = 22, 28
    elif n == 3:
        cw, gap = 18, 22
    else:
        cw, gap = 13, 15
    positions = []
    for (o, c, hi, lo) in pattern:
        _candle(d, x, o, c, hi, lo, cw, y0, yscale)
        positions.append((x, o, c, hi, lo))
        x += cw + gap
    xs = [p[0] for p in positions]
    his = [p[3] for p in positions]
    los = [p[4] for p in positions]
    box_x0 = xs[0] - cw / 2.0 - 8
    box_x1 = xs[-1] + cw / 2.0 + 8
    box_y0 = Y(min(los)) - 8
    box_y1 = Y(max(his)) + 9
    d.add(Rect(box_x0, box_y0, box_x1 - box_x0, box_y1 - box_y0, rx=6, ry=6,
               fillColor=None, strokeColor=GOLD, strokeWidth=1.4))
    _label(d, (box_x0 + box_x1) / 2.0, label_row, 'PATTERN', size=8, color=GOLD, bold=True)

    color, default_bias_label = BIAS_STYLE[bias]
    last_close = positions[-1][2]
    gw = 13
    ggap = 17
    if bias == 'bullish':
        c1 = min(94, last_close + 12)
        c2 = min(97, c1 + 12)
        g1 = (last_close, c1, c1 + 4, last_close - 3)
        g2 = (c1, c2, c2 + 4, c1 - 3)
    elif bias == 'bearish':
        c1 = max(6, last_close - 12)
        c2 = max(3, c1 - 12)
        g1 = (last_close, c1, last_close + 3, c1 - 4)
        g2 = (c1, c2, c1 + 3, c2 - 4)
    else:
        c1 = last_close + 5
        c2 = last_close - 3
        g1 = (last_close, c1, c1 + 4, last_close - 4)
        g2 = (c1, c2, c1 + 4, c2 - 4)

    gx1 = box_x1 + 16 + gw / 2.0
    gx2 = gx1 + gw + ggap
    _ghost_candle(d, gx1, *g1, gw, y0, yscale, color)
    _ghost_candle(d, gx2, *g2, gw, y0, yscale, color)

    ax0 = box_x1 + 6
    ay0 = Y(last_close)
    ax1 = gx2 + gw / 2.0 + 30
    ay1 = Y(g2[1]) + (8 if bias == 'bullish' else (-8 if bias == 'bearish' else 0))
    if ax1 > width - 12:
        shift = ax1 - (width - 12)
        ax0 -= shift
        ax1 -= shift
        gx1 -= shift
        gx2 -= shift
    _arrow(d, ax0, ay0, ax1, ay1, color)
    label = bias_label or default_bias_label
    ly = ay1 + (11 if bias != 'bearish' else -15)
    _label(d, ax1, ly, label, size=8.4, color=color, bold=True,
           anchor='end' if ax1 > width - 78 else 'start')
    _label(d, (gx1 + gx2) / 2.0, label_row, 'EXPECTED', size=7.4, color=color, bold=True)

    return d


def glance_table(bias, reliability, best_seen, bias_label=None):
    color, default_word = BIAS_STYLE[bias]
    bias_word = bias_label or default_word
    data = [
        [Paragraph('BIAS', styles['GlanceLabel']),
         Paragraph('RELIABILITY', styles['GlanceLabel']),
         Paragraph('BEST SEEN', styles['GlanceLabel'])],
        [Paragraph(f'<font color="{_hex(color)}">{bias_word}</font>', styles['GlanceValue']),
         Paragraph(reliability, styles['GlanceValue']),
         Paragraph(best_seen, styles['GlanceValue'])],
    ]
    t = Table(data, colWidths=[110, 150, 208])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, PANEL_LINE),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, PANEL_LINE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def pattern_header_table(name, tagline):
    data = [[Paragraph(name, styles['PatternTitle'])],
            [Paragraph(tagline, styles['PatternSub'])]]
    t = Table(data, colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ('TOPPADDING', (0, 1), (-1, 1), 1),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('LINEABOVE', (0, 0), (-1, 0), 3, GOLD),
    ]))
    return t


def render_topic(title, paragraphs, drawing=None, caption=None, bullets=None):
    block = [topic_heading(title)]
    for para in paragraphs:
        block.append(Paragraph(para, styles['Body']))
    if bullets:
        for b in bullets:
            block.append(Paragraph(f'•  {b}', styles['BulletItem']))
    if drawing is not None:
        block.append(Spacer(1, 6))
        block.append(drawing)
        if caption:
            block.append(Paragraph(caption, styles['Caption']))
    return KeepTogether(block)


# ---------------------------------------------------------------------------
# MODULE 1 — Understanding Market Structure
# ---------------------------------------------------------------------------

MODULE1_INTRO = (
    "Before you ever look for a candlestick pattern, you need to know one thing: "
    "which direction is the market already leaning? A perfect Bullish Engulfing Bar "
    "means very different things in an uptrend, a downtrend, and a dead-flat range. "
    "Market structure is the skeleton underneath every chart — it's what tells you "
    "whether you're looking for reasons to buy, reasons to sell, or reasons to stay "
    "out entirely."
)

MODULE1_TOPICS = [
    dict(
        title='What Is Market Structure?',
        paragraphs=[
            "Market structure is simply the shape price leaves behind as it moves — "
            "the sequence of swing highs (points where price turned down) and swing "
            "lows (points where price turned up). Connect those turning points and "
            "you get a zigzag that tells you, at a glance, whether buyers or sellers "
            "have been winning.",
            "Everything in this module — trends, ranges, reversals, BOS, CHoCH — is "
            "just a different way of describing the relationship between one swing "
            "point and the next.",
        ],
        drawing=structure_drawing(
            [(0.04, 28, None, 'low'), (0.20, 66, 'Swing High', 'high'),
             (0.38, 40, 'Swing Low', 'low'), (0.56, 76, 'Swing High', 'high'),
             (0.74, 48, 'Swing Low', 'low'), (0.92, 84, 'Swing High', 'high')],
            trend_label='Price Path'),
        caption='Figure — Every chart is just a sequence of swing highs and swing lows.',
    ),
    dict(
        title='Higher Highs (HH)',
        paragraphs=[
            "A Higher High forms when a new swing high prints above the previous "
            "swing high. It's the clearest sign that buyers are extending their "
            "control — each rally is making more ground than the last one.",
        ],
        drawing=structure_drawing(
            [(0.08, 30, None, 'low'), (0.32, 58, 'Prior High', 'high'),
             (0.58, 38, None, 'low'), (0.85, 78, 'Higher High', 'high')],
        ),
        caption='Figure — The second peak prints above the first: a Higher High.',
    ),
    dict(
        title='Higher Lows (HL)',
        paragraphs=[
            "A Higher Low forms when a new swing low prints above the previous swing "
            "low — sellers can no longer push price back down as far as they did "
            "last time. Higher Highs and Higher Lows together are what define an "
            "uptrend; you need both, not just one.",
        ],
        drawing=structure_drawing(
            [(0.08, 82, None, 'high'), (0.32, 42, 'Prior Low', 'low'),
             (0.58, 70, None, 'high'), (0.85, 55, 'Higher Low', 'low')],
        ),
        caption='Figure — The second dip holds above the first: a Higher Low.',
    ),
    dict(
        title='Lower Highs (LH)',
        paragraphs=[
            "A Lower High forms when a new swing high fails to reach the previous "
            "swing high. It's usually the first visible crack in an uptrend — "
            "buyers pushed, but with noticeably less force than before.",
        ],
        drawing=structure_drawing(
            [(0.08, 28, None, 'low'), (0.32, 74, 'Prior High', 'high'),
             (0.58, 44, None, 'low'), (0.85, 58, 'Lower High', 'high')],
        ),
        caption='Figure — The second peak fails below the first: a Lower High.',
    ),
    dict(
        title='Lower Lows (LL)',
        paragraphs=[
            "A Lower Low forms when a new swing low prints below the previous swing "
            "low — sellers are extending their control. Lower Highs and Lower Lows "
            "together are what define a downtrend.",
        ],
        drawing=structure_drawing(
            [(0.08, 86, None, 'high'), (0.32, 54, 'Prior Low', 'low'),
             (0.58, 70, None, 'high'), (0.85, 34, 'Lower Low', 'low')],
        ),
        caption='Figure — The second dip breaks below the first: a Lower Low.',
    ),
    dict(
        title='Uptrends',
        paragraphs=[
            "An uptrend is nothing more than a repeating pattern of Higher Highs "
            "and Higher Lows. As long as that pattern keeps repeating, the trend is "
            "intact — your job as a trader is to look for bullish candlestick "
            "signals at the Higher Low, not to guess when the next high will form.",
        ],
        drawing=structure_drawing(
            [(0.05, 22, None, 'low'), (0.19, 42, 'HH', 'high'), (0.33, 32, 'HL', 'low'),
             (0.47, 58, 'HH', 'high'), (0.61, 46, 'HL', 'low'), (0.75, 72, 'HH', 'high'),
             (0.90, 60, 'HL', 'low')],
            ref_diag=((0.05, 18), (0.90, 56)), ref_color=GOLD,
            trend_label='Uptrend = HH + HL'),
        caption='Figure — A rising sequence of Higher Highs and Higher Lows.',
    ),
    dict(
        title='Downtrends',
        paragraphs=[
            "A downtrend is a repeating pattern of Lower Highs and Lower Lows — the "
            "mirror image of an uptrend. Here, your job is to look for bearish "
            "candlestick signals at the Lower High, not at the bottom of the move.",
        ],
        drawing=structure_drawing(
            [(0.05, 80, None, 'high'), (0.19, 58, 'LL', 'low'), (0.33, 68, 'LH', 'high'),
             (0.47, 42, 'LL', 'low'), (0.61, 54, 'LH', 'high'), (0.75, 28, 'LL', 'low'),
             (0.90, 40, 'LH', 'high')],
            ref_diag=((0.05, 78), (0.90, 40)), ref_color=GOLD,
            trend_label='Downtrend = LH + LL'),
        caption='Figure — A falling sequence of Lower Highs and Lower Lows.',
    ),
    dict(
        title='Ranging Markets',
        paragraphs=[
            "A range (or consolidation) is what happens when neither buyers nor "
            "sellers can extend structure in either direction — price oscillates "
            "between a ceiling and a floor without printing a new Higher High or a "
            "new Lower Low. Ranges are where candlestick patterns are least "
            "reliable on their own, because there's no prevailing direction for a "
            "pattern to confirm.",
        ],
        drawing=structure_drawing(
            [(0.05, 50, None, 'low'), (0.20, 63, None, 'high'), (0.35, 38, None, 'low'),
             (0.50, 64, None, 'high'), (0.65, 37, None, 'low'), (0.80, 62, None, 'high'),
             (0.95, 40, None, 'low')],
            zone=(35, 65), zone_color=GOLD_LIGHT,
            trend_label='Range-Bound / Consolidation'),
        caption='Figure — Price oscillates inside a ceiling and floor, going nowhere.',
    ),
    dict(
        title='Trend Reversals',
        paragraphs=[
            "A reversal happens when the market fails to extend the existing "
            "structure and starts printing the opposite structure instead. In an "
            "uptrend, that means a swing high fails to beat the prior high (a Lower "
            "High), and price then breaks below the last Higher Low — the sequence "
            "of HH/HL has quietly become a sequence of LH/LL.",
        ],
        drawing=structure_drawing(
            [(0.05, 25, None, 'low'), (0.18, 45, 'HH', 'high'), (0.31, 35, 'HL', 'low'),
             (0.44, 62, 'HH', 'high'), (0.57, 50, 'HL', 'low'), (0.70, 58, 'LH', 'high'),
             (0.83, 32, 'LL', 'low')],
            break_from=5, annotation=('Reversal', SHIFT_VIOLET), annotation_color=SHIFT_VIOLET,
            trend_label='Uptrend → Downtrend'),
        caption='Figure — The uptrend fails to make a new high, then breaks its last Higher Low.',
    ),
    dict(
        title='Trend Continuations',
        paragraphs=[
            "Most of the time, a trend does exactly what it's been doing. A "
            "continuation is what happens when a pullback holds above the prior "
            "Higher Low and price simply resumes making new Higher Highs — the far "
            "more common (and far less exciting) outcome than a reversal.",
        ],
        drawing=structure_drawing(
            [(0.06, 28, None, 'low'), (0.28, 55, 'HH', 'high'), (0.50, 42, 'HL', 'low'),
             (0.72, 78, 'HH', 'high'), (0.94, 66, 'HL', 'low')],
            annotation=('Trend Resumes', BULL_GREEN), annotation_color=BULL_GREEN,
            trend_label='Pullback Holds → New High'),
        caption='Figure — The pullback holds the Higher Low, and the uptrend continues.',
    ),
    dict(
        title='Break of Structure (BOS)',
        paragraphs=[
            "A Break of Structure is what it sounds like: price breaks through the "
            "most recent significant swing high (in an uptrend) or swing low (in a "
            "downtrend), confirming that the existing trend is still in control. "
            "A BOS is a continuation signal — it tells you the trend just proved "
            "itself again.",
        ],
        drawing=structure_drawing(
            [(0.06, 30, None, 'low'), (0.28, 58, 'HH', 'high'), (0.50, 44, 'HL', 'low'),
             (0.90, 82, None, 'high')],
            ref_line=58, ref_label='Prior High', ref_color=GOLD, break_from=2,
            annotation=('BOS', GOLD), annotation_color=GOLD,
            trend_label='Break of Structure'),
        caption='Figure — Price pushes back through the prior swing high: structure holds.',
    ),
    dict(
        title='Change of Character (CHoCH)',
        paragraphs=[
            "A Change of Character is the opposite signal: price breaks the most "
            "recent Higher Low (in an uptrend) or Lower High (in a downtrend) — "
            "structure breaking against the prevailing trend for the first time. "
            "A CHoCH is your earliest warning that a reversal may be starting; it's "
            "often the very first leg of what later becomes a full trend reversal.",
        ],
        drawing=structure_drawing(
            [(0.06, 30, None, 'low'), (0.24, 52, 'HH', 'high'), (0.42, 38, 'HL', 'low'),
             (0.60, 68, 'HH', 'high'), (0.78, 50, 'HL', 'low'), (0.94, 25, None, 'low')],
            ref_line=50, ref_label='Last Higher Low', ref_color=SHIFT_VIOLET, break_from=4,
            annotation=('CHoCH', SHIFT_VIOLET), annotation_color=SHIFT_VIOLET,
            trend_label='Possible Trend Shift'),
        caption='Figure — Price breaks the last Higher Low: the first sign of a possible shift.',
    ),
]

# ---------------------------------------------------------------------------
# MODULE 2 — Support & Resistance
# ---------------------------------------------------------------------------

MODULE2_INTRO = (
    "Structure tells you the direction. Support and resistance tell you where to "
    "actually look for a trade. A Bullish Engulfing Bar floating in open air is a "
    "coin flip; the same candle forming exactly at a level price has respected "
    "before is a completely different proposition. This module is about finding "
    "those levels and learning to tell the strong ones from the weak ones."
)

MODULE2_TOPICS = [
    dict(
        title='Horizontal Support',
        paragraphs=[
            "Horizontal support is a flat price level where buying has repeatedly "
            "stepped in to stop a decline. The more times a level holds, the more "
            "traders notice it — and the more orders tend to cluster there, which "
            "can (up to a point) make the level even more likely to hold again.",
        ],
        drawing=structure_drawing(
            [(0.05, 55, None, 'high'), (0.20, 26, None, 'low'), (0.35, 58, None, 'high'),
             (0.50, 27, None, 'low'), (0.65, 60, None, 'high'), (0.80, 25, None, 'low'),
             (0.95, 62, None, 'high')],
            ref_line=25, ref_label='Support', ref_color=GOLD,
            arrows=[(1, 'up', BULL_GREEN), (3, 'up', BULL_GREEN), (5, 'up', BULL_GREEN)]),
        caption='Figure — Price bounces off the same floor three times in a row.',
    ),
    dict(
        title='Horizontal Resistance',
        paragraphs=[
            "Horizontal resistance is the mirror image — a flat level where selling "
            "has repeatedly stopped an advance. Watch for candlestick reversal "
            "signals (Shooting Stars, Bearish Engulfing Bars, Evening Stars) "
            "forming right at a resistance level; that's the highest-value spot on "
            "the whole chart to look for one.",
        ],
        drawing=structure_drawing(
            [(0.05, 45, None, 'low'), (0.20, 74, None, 'high'), (0.35, 42, None, 'low'),
             (0.50, 73, None, 'high'), (0.65, 40, None, 'low'), (0.80, 75, None, 'high'),
             (0.95, 38, None, 'low')],
            ref_line=75, ref_label='Resistance', ref_color=GOLD,
            arrows=[(1, 'down', BEAR_RED), (3, 'down', BEAR_RED), (5, 'down', BEAR_RED)]),
        caption='Figure — Price is turned away from the same ceiling three times in a row.',
    ),
    dict(
        title='Dynamic Support',
        paragraphs=[
            "Not every level is flat. Dynamic support is a rising line — often a "
            "trendline or moving average — that price keeps bouncing off as it "
            "climbs. It moves with the trend, which makes it useful for spotting "
            "pullback entries inside a strong uptrend rather than waiting for price "
            "to fall all the way back to a fixed horizontal level.",
        ],
        drawing=structure_drawing(
            [(0.05, 20, None, 'low'), (0.20, 45, None, 'high'), (0.35, 28, None, 'low'),
             (0.50, 55, None, 'high'), (0.65, 38, None, 'low'), (0.80, 65, None, 'high'),
             (0.95, 48, None, 'low')],
            ref_diag=((0.05, 18), (0.95, 46)), ref_color=GOLD,
            arrows=[(2, 'up', BULL_GREEN), (4, 'up', BULL_GREEN), (6, 'up', BULL_GREEN)],
            trend_label='Rising Trendline = Dynamic Support'),
        caption='Figure — Price rides a rising trendline higher, bouncing off it each time.',
    ),
    dict(
        title='Dynamic Resistance',
        paragraphs=[
            "The falling counterpart: a descending trendline that price keeps "
            "getting rejected from on the way down. As long as each rally is capped "
            "by that falling line, sellers remain in control — a clean break above "
            "it is often one of the first hints a downtrend is losing its grip.",
        ],
        drawing=structure_drawing(
            [(0.05, 80, None, 'high'), (0.20, 55, None, 'low'), (0.35, 72, None, 'high'),
             (0.50, 45, None, 'low'), (0.65, 62, None, 'high'), (0.80, 35, None, 'low'),
             (0.95, 52, None, 'high')],
            ref_diag=((0.05, 82), (0.95, 54)), ref_color=GOLD,
            arrows=[(2, 'down', BEAR_RED), (4, 'down', BEAR_RED), (6, 'down', BEAR_RED)],
            trend_label='Falling Trendline = Dynamic Resistance'),
        caption='Figure — Price is capped by a falling trendline, rejected each time it approaches.',
    ),
    dict(
        title='Role Reversal',
        paragraphs=[
            "One of the most useful ideas in trading: once a resistance level "
            "finally breaks, it frequently flips and starts acting as support — and "
            "once a support level breaks, it frequently flips and starts acting as "
            "resistance. The market's memory of a level doesn't disappear just "
            "because price broke through it once.",
            "A retest of a broken level, holding on the new side, is one of the "
            "higher-probability entries in this entire book — especially when a "
            "bullish or bearish candlestick pattern confirms it.",
        ],
        drawing=structure_drawing(
            [(0.05, 40, None, 'low'), (0.18, 58, None, 'high'), (0.31, 42, None, 'low'),
             (0.44, 59, None, 'high'), (0.57, 45, None, 'low'), (0.70, 82, None, 'high'),
             (0.83, 60, None, 'low'), (0.96, 85, None, 'high')],
            ref_line=60, ref_label='Key Level', ref_color=GOLD,
            arrows=[(1, 'down', BEAR_RED), (3, 'down', BEAR_RED), (6, 'up', BULL_GREEN)],
            annotation=('Now Support', BULL_GREEN), annotation_color=BULL_GREEN),
        caption='Figure — Resistance is broken, then retested and defended as new support.',
    ),
    dict(
        title='Psychological Price Levels',
        paragraphs=[
            "Round numbers act like magnets — a level like 1.2000 on EUR/USD or a "
            "clean 100.00 on an index attracts orders simply because so many "
            "traders and institutions use round numbers to place them. These "
            "levels can act as support or resistance even with no prior chart "
            "history at all, purely because of where the number sits.",
        ],
        drawing=structure_drawing(
            [(0.05, 40, None, 'low'), (0.20, 60, None, 'high'), (0.35, 48, None, 'low'),
             (0.50, 62, None, 'high'), (0.65, 46, None, 'low'), (0.80, 58, None, 'high'),
             (0.95, 50, None, 'low')],
            ref_line=55, ref_label='Round Number Level', ref_color=GOLD,
            arrows=[(1, 'down', GOLD), (2, 'up', GOLD), (3, 'down', GOLD), (4, 'up', GOLD)]),
        caption='Figure — Price reacts around a round number from both directions.',
    ),
    dict(
        title='Fresh vs Tested Levels',
        paragraphs=[
            "A fresh level — one that hasn't been touched yet — tends to produce a "
            "strong, clean reaction the first time price arrives, because the full "
            "weight of unfilled orders is still sitting there untouched. A level "
            "that's already been tested several times has fewer of those orders "
            "left; each additional touch tends to produce a weaker reaction until "
            "the level eventually gives way.",
        ],
        drawing=split_drawing_row(
            structure_drawing(
                [(0.10, 55, None, 'high'), (0.50, 22, None, 'low'), (0.90, 68, None, 'high')],
                width=227, ref_line=20, ref_label='Fresh', ref_color=GOLD,
                arrows=[(1, 'up', BULL_GREEN)]),
            'Fresh level — first touch, strong reaction.',
            structure_drawing(
                [(0.06, 60, None, 'high'), (0.22, 22, None, 'low'), (0.38, 50, None, 'high'),
                 (0.52, 24, None, 'low'), (0.66, 42, None, 'high'), (0.80, 26, None, 'low'),
                 (0.94, 34, None, 'high')],
                width=227, ref_line=20, ref_label='Tested', ref_color=GOLD,
                arrows=[(1, 'up', BULL_GREEN), (3, 'up', GOLD), (5, 'up', TRAP_ORANGE)]),
            'Tested level — each touch reacts a little weaker.',
        ),
    ),
    dict(
        title='Strong vs Weak Zones',
        paragraphs=[
            "A strong zone produces a sharp, decisive reaction — price arrives, "
            "reverses hard, and leaves quickly, which shows real conviction behind "
            "the level. A weak zone produces a choppy, grinding reaction — price "
            "lingers, wobbles, and often eventually slices straight through. The "
            "sharper the reaction, the more you can trust the zone next time.",
        ],
        drawing=split_drawing_row(
            structure_drawing(
                [(0.15, 70, None, 'high'), (0.50, 20, None, 'low'), (0.85, 72, None, 'high')],
                width=227, zone=(15, 25), zone_color=BULL_GREEN,
                arrows=[(1, 'up', BULL_GREEN)]),
            'Strong zone — sharp, decisive rejection.',
            structure_drawing(
                [(0.06, 45, None, 'high'), (0.20, 30, None, 'low'), (0.34, 42, None, 'high'),
                 (0.48, 28, None, 'low'), (0.62, 38, None, 'high'), (0.76, 24, None, 'low'),
                 (0.90, 18, None, 'low')],
                width=227, zone=(18, 32), zone_color=TRAP_ORANGE),
            'Weak zone — choppy, grinds through easily.',
        ),
    ),
]

# ---------------------------------------------------------------------------
# MODULE 3 — Candlestick Psychology
# ---------------------------------------------------------------------------

MODULE3_INTRO = (
    "Volume I taught you to recognize fourteen candlestick patterns by shape. This "
    "module asks a different question: why does each one form in the first place? "
    "Every pattern is really just a short story about a fight between buyers and "
    "sellers — and once you can read that story, you stop memorizing shapes and "
    "start thinking about what large, well-funded traders were probably doing "
    "during that candle. That shift in thinking is what separates a trader who "
    "reacts to patterns from one who anticipates them."
)


def psychology_card(name, setup, reaction, outcome, read):
    inner = [
        Paragraph(name, ParagraphStyle('cardname_' + name.replace(' ', '_'),
                  fontName='Helvetica-Bold', fontSize=12.5, textColor=NAVY, spaceAfter=5)),
        Paragraph(f'<b>Setup —</b> {setup}', styles['Body']),
        Paragraph(f'<b>Reaction —</b> {reaction}', styles['Body']),
        Paragraph(f'<b>Outcome —</b> {outcome}', styles['Body']),
        Paragraph(f'<b><font color="{_hex(GOLD)}">Institutional Read —</font></b> '
                  f'<i>{read}</i>', styles['Body']),
    ]
    t = Table([[inner]], colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, PANEL_LINE),
        ('LINEBEFORE', (0, 0), (0, -1), 3, GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


MODULE3_PATTERNS = [
    dict(name='Hammer', setup="Price sells off hard within the period.",
         reaction="Sellers push to a new low, but buyers absorb every bit of that "
                  "supply and drive price back up.",
         outcome="Buyers win the session decisively.",
         read="A large buyer likely used the sell-off as a chance to accumulate at "
              "a discount — smart money often buys into panic, not into strength."),
    dict(name='Hanging Man', setup="Price has been rallying.",
         reaction="Sellers push price sharply lower intraday even though the trend "
                  "is up; buyers only partially recover it.",
         outcome="Buyers technically \"win\" the candle, but only after real "
                 "selling pressure showed up for the first time.",
         read="Large sellers are starting to test the market's ability to absorb "
              "supply — the first crack in an uptrend often looks exactly like this."),
    dict(name='Shooting Star', setup="Price has been rallying.",
         reaction="Buyers push to a new high, but sellers overwhelm them and slam "
                  "price back down near the open.",
         outcome="Sellers win the session after buyers briefly looked in control.",
         read="This is often where large sellers unload into retail buying "
              "enthusiasm at the top of a move — distribution disguised as a "
              "breakout."),
    dict(name='Doji', setup="Often appears after an extended move in either direction.",
         reaction="Buyers and sellers both push price around but neither can hold "
                  "the advantage into the close.",
         outcome="A dead-even standoff.",
         read="Big players are pausing, not stepping away — a Doji after a strong "
              "trend often means smart money is quietly repositioning."),
    dict(name='Bullish Engulfing Bar', setup="Price has been falling.",
         reaction="Sellers control the first candle, but on the second, buyers "
                  "don't just stop the decline — they erase it entirely and then some.",
         outcome="A total, forceful handover of control to buyers.",
         read="This is what it looks like when a large buyer steps in aggressively "
              "enough to absorb an entire session's worth of selling in one move."),
    dict(name='Bearish Engulfing Bar', setup="Price has been rising.",
         reaction="Buyers control the first candle, but sellers erase the entire "
                  "gain on the second and push further.",
         outcome="A forceful handover of control to sellers.",
         read="Large sellers are using rally strength as their exit — and taking "
              "price with them on the way out."),
    dict(name='Bullish Harami', setup="Price has been falling hard.",
         reaction="After one more strong seller push, the very next candle "
                  "contracts sharply into a small, indecisive range.",
         outcome="Sellers haven't lost yet, but they've clearly stopped gaining ground.",
         read="Aggressive selling has met a wall of hidden demand — often the "
              "first sign that a large buyer has started quietly absorbing supply."),
    dict(name='Bearish Harami', setup="Price has been rising strongly.",
         reaction="After one more strong buyer push, the next candle contracts sharply.",
         outcome="Buyers haven't lost control yet, but their momentum has stalled hard.",
         read="A large seller has likely started absorbing the rally without yet "
              "forcing price down — distribution often begins exactly like this."),
    dict(name='Morning Star', setup="Price is in a clear downtrend.",
         reaction="One more strong seller candle, followed by a session of pure "
                  "indecision, followed by buyers taking full control.",
         outcome="A three-act story of sellers exhausting themselves and buyers "
                 "seizing the moment.",
         read="The \"star\" candle in the middle is often where smart money "
              "quietly finishes accumulating before letting price run."),
    dict(name='Evening Star', setup="Price is in a clear uptrend.",
         reaction="One more strong buyer candle, a session of indecision, then "
                  "sellers take full control.",
         outcome="A three-act top forming in real time.",
         read="The indecision candle is often the exact moment large holders "
              "begin distributing into the last wave of buyers."),
    dict(name='Tweezer Tops', setup="Price is rallying toward a level.",
         reaction="Price tests the same high twice and is turned back both times.",
         outcome="A clearly defined ceiling.",
         read="A large seller is defending that price with real size — two "
              "rejections at almost the same print rarely happens by accident."),
    dict(name='Tweezer Bottoms', setup="Price is falling toward a level.",
         reaction="Price tests the same low twice and is defended both times.",
         outcome="A clearly defined floor.",
         read="A large buyer is defending that price — the market is telling you "
              "exactly where the order book gets heavy."),
    dict(name='Dragonfly Doji', setup="Price has been falling.",
         reaction="Sellers drive price sharply lower during the session, but "
                  "buyers reclaim essentially all of the ground by the close.",
         outcome="A decisive rejection of lower prices.",
         read="Often a stop-hunt — price is pushed low enough to trigger panic "
              "selling and stop-losses, which large buyers then absorb."),
    dict(name='Gravestone Doji', setup="Price has been rising.",
         reaction="Buyers drive price sharply higher, but sellers reclaim "
                  "essentially all of the ground by the close.",
         outcome="A decisive rejection of higher prices.",
         read="Often a liquidity grab above a well-known high, sweeping in "
              "breakout buyers right before smart money sells into them."),
]

# ---------------------------------------------------------------------------
# MODULE 4 — Candlestick Confirmation
# ---------------------------------------------------------------------------

MODULE4_INTRO = (
    "Here is the single most important habit in this entire book: never trade the "
    "candle alone. A candlestick pattern is a hypothesis about what buyers and "
    "sellers just did — not proof of what they're about to do next. Professional "
    "traders treat every pattern as the first piece of evidence in a case, and "
    "they wait for more evidence to stack up before they ever risk money on it."
)

_confirm_context = downtrend_context(end_level=55, n=6)
_confirm_pattern = [(55, 45, 57, 43), (42, 62, 64, 40)]

MODULE4_CONFIRM_DRAWING = [
    pattern_drawing(_confirm_context, _confirm_pattern, bias='neutral',
                     trend_label='Downtrend', bias_label='Unclear — no confirmation yet'),
    Paragraph('Without confirmation: the pattern appeared, but nothing has proven it yet.',
              styles['Caption']),
    Spacer(1, 8),
    pattern_drawing(_confirm_context, _confirm_pattern, bias='bullish',
                     trend_label='Downtrend'),
    Paragraph('With confirmation: the next candle closes higher, proving buyers are in control.',
              styles['Caption']),
]

MODULE4_TOPICS = [
    dict(
        title='Next Candle Confirmation',
        paragraphs=[
            "The single most reliable confirmation is also the simplest: wait for "
            "the candle after the pattern to close in the direction the pattern "
            "implied. A Bullish Engulfing Bar followed by another strong bullish "
            "candle is a very different trade than one followed by a candle that "
            "immediately gives the gain back.",
            "Yes, waiting costs you a little bit of entry price. It also filters "
            "out a large share of the patterns that were never going to work.",
        ],
    ),
    dict(
        title='Momentum',
        paragraphs=[
            "Momentum is the speed and force behind a move. A confirming candle "
            "with a large body and real follow-through carries far more weight "
            "than a small, hesitant one that barely edges in the right direction. "
            "If you use an indicator like RSI or a moving average, a decisive move "
            "away from neutral adds another layer of confidence on top of the "
            "candle itself.",
        ],
    ),
    dict(
        title='Volume (Where Available)',
        paragraphs=[
            "On instruments where real volume data exists — stocks, futures, most "
            "crypto pairs — a pattern that forms on above-average volume is far "
            "more trustworthy than the same pattern on a quiet, thin session. "
            "Volume shows you how many participants actually agreed with the move.",
            "Many FX, HFX, and binary options platforms don't provide true "
            "exchange volume, only tick activity — so treat this confirmation as a "
            "bonus where it's available, not a requirement everywhere.",
        ],
    ),
    dict(
        title='Trend Direction',
        paragraphs=[
            "Go back to Module 1. A reversal pattern only means something at the "
            "end of a real trend; a continuation pattern only means something in "
            "the direction of a trend that's already in motion. The exact same "
            "candle shape appearing in the middle of a range, with no structure "
            "behind it, is far weaker evidence.",
        ],
    ),
    dict(
        title='Support & Resistance',
        paragraphs=[
            "Go back to Module 2. A pattern forming at a well-tested horizontal "
            "level, a dynamic trendline, or a round psychological number carries "
            "meaningfully more weight than the same pattern forming in open air "
            "with no level nearby.",
        ],
    ),
    dict(
        title='Multiple Confirmations',
        paragraphs=[
            "No single confirmation guarantees a winning trade — but each one you "
            "stack on top of the pattern meaningfully improves your odds. A "
            "Hammer, at support, with the next candle closing higher, and RSI "
            "turning up from oversold, is a completely different quality of setup "
            "than a Hammer sitting alone in the middle of a chart.",
            "This is the exact idea Module 7 builds on: professional setups are "
            "rarely a single pattern in isolation — they're several signals "
            "agreeing with each other at the same time and the same price.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MODULE 5 — 12 Advanced Candlestick Patterns
# ---------------------------------------------------------------------------

MODULE5_INTRO = (
    "The fourteen patterns in Volume I cover most of what you'll see day to day. "
    "This module adds twelve more — patterns built from three, four, or five "
    "candles instead of one or two, which means they tell a longer, more detailed "
    "story about the fight between buyers and sellers. They tend to be rarer than "
    "the basics, but when they do appear, they're often some of the highest-"
    "conviction signals on the whole chart."
)

MODULE5_PATTERNS = [
    dict(
        key='piercing_line', name='Piercing Line',
        tagline='A bullish candle drives deep into the bear’s territory',
        bias='bullish', reliability='Medium-High', best_seen='After a downtrend',
        context=downtrend_context(end_level=70), trend_label='Downtrend',
        pattern=[(70, 40, 72, 38), (32, 58, 60, 30)],
        looks_like="A two-candle pattern: a large bearish candle, followed by a "
                   "bullish candle that opens below the first candle's low but "
                   "closes more than halfway back up into the first candle's body "
                   "— without fully engulfing it.",
        psychology="Sellers open the second session with a fresh push lower, but "
                   "buyers take that low print and drive price back up through more "
                   "than half of the previous session's decline. It's forceful, but "
                   "not quite the total takeover an engulfing bar represents.",
        usage="Traders treat a Piercing Line after a downtrend similarly to a "
              "Bullish Engulfing Bar, though slightly less decisively — many wait "
              "for one more bullish candle before committing to a full position.",
        caution="The deeper the second candle closes into the first candle's body, "
                "the stronger the signal. A close barely above the halfway point is "
                "a much weaker version of this pattern.",
    ),
    dict(
        key='dark_cloud_cover', name='Dark Cloud Cover',
        tagline='A bearish candle drags price back down through the rally',
        bias='bearish', reliability='Medium-High', best_seen='After an uptrend',
        context=uptrend_context(end_level=30), trend_label='Uptrend',
        pattern=[(30, 60, 62, 28), (68, 42, 70, 40)],
        looks_like="The mirror of the Piercing Line: a large bullish candle, "
                   "followed by a bearish candle that opens above the first "
                   "candle's high but closes more than halfway back down into the "
                   "first candle's body.",
        psychology="Buyers open the second session pushing to a fresh high, but "
                   "sellers seize control and drag price back down through more "
                   "than half of the prior rally. A clear signal that momentum has "
                   "swung, even without a full engulfing close.",
        usage="Traders treat a confirmed Dark Cloud Cover after an uptrend as a "
              "solid warning sign to reduce exposure or look for a bearish entry, "
              "particularly when it forms at resistance.",
        caution="As with the Piercing Line, depth matters — the further the second "
                "candle closes into the first candle's body, the more conviction "
                "the pattern carries.",
    ),
    dict(
        key='three_white_soldiers', name='Three White Soldiers',
        tagline='Three straight candles march to new highs',
        bias='bullish', reliability='High', best_seen='After a downtrend',
        context=downtrend_context(end_level=25), trend_label='Downtrend',
        pattern=[(25, 45, 47, 23), (35, 58, 60, 33), (48, 70, 72, 46)],
        looks_like="Three consecutive, similarly sized bullish candles, each "
                   "opening inside the previous candle's body and closing at a new "
                   "high, with small wicks throughout.",
        psychology="Buyers take control and simply keep taking control, session "
                   "after session, without giving sellers any real opportunity to "
                   "push back. Three clean, steady wins in a row is a strong show "
                   "of sustained conviction rather than a single burst of buying.",
        usage="This is one of the more trusted multi-candle reversal or momentum "
              "signals — traders often use it to confirm a new uptrend is underway "
              "and look to join on the next shallow pullback rather than chase the "
              "third candle directly.",
        caution="Watch for unusually long bodies with almost no wicks across all "
                "three candles — that can signal an overextended, exhausted move "
                "that's due for a pause rather than a healthy new trend.",
    ),
    dict(
        key='three_black_crows', name='Three Black Crows',
        tagline='Three straight candles march to new lows',
        bias='bearish', reliability='High', best_seen='After an uptrend',
        context=uptrend_context(end_level=75), trend_label='Uptrend',
        pattern=[(75, 55, 77, 53), (65, 42, 67, 40), (52, 30, 54, 28)],
        looks_like="Three consecutive, similarly sized bearish candles, each "
                   "opening inside the previous candle's body and closing at a new "
                   "low, with small wicks throughout.",
        psychology="Sellers take control and keep it, session after session, with "
                   "no real pushback from buyers. Three consistent, orderly losses "
                   "in a row show sustained selling pressure rather than a single "
                   "panic spike.",
        usage="Traders treat this as strong confirmation that a top is forming and "
              "a new downtrend is underway, often looking to join on the next "
              "shallow bounce rather than chase the third candle directly.",
        caution="As with Three White Soldiers, watch for exhaustion — three "
                "unusually long, wick-free candles in a row can mean the move is "
                "overextended and due for at least a temporary bounce.",
    ),
    dict(
        key='bullish_marubozu', name='Bullish Marubozu',
        tagline='A candle with no wicks at all — pure conviction',
        bias='bullish', reliability='Medium', best_seen='After a downtrend or breakout',
        context=downtrend_context(end_level=30), trend_label='Downtrend',
        pattern=[(30, 75, 76, 29)],
        looks_like="A single candle with a large bullish body and virtually no "
                   "upper or lower wick — the open is (almost) the low, and the "
                   "close is (almost) the high.",
        psychology="Buyers control the entire session from the opening bell to the "
                   "close, without sellers ever meaningfully pushing back. No wick "
                   "means no rejection at either end — pure, uncontested buying "
                   "pressure for the whole period.",
        usage="A Marubozu is often used as a momentum confirmation candle — "
              "traders treat it as a strong signal that whichever side is in "
              "control intends to keep pushing, and it works both as a reversal "
              "candle after a decline and as a continuation candle mid-trend.",
        caution="A Marubozu appearing after an already extended move can mark "
                "exhaustion (a climax candle) rather than the start of a fresh "
                "trend — location still matters as much as shape.",
    ),
    dict(
        key='bearish_marubozu', name='Bearish Marubozu',
        tagline='A candle with no wicks at all — pure conviction, downward',
        bias='bearish', reliability='Medium', best_seen='After an uptrend or breakdown',
        context=uptrend_context(end_level=75), trend_label='Uptrend',
        pattern=[(75, 30, 76, 29)],
        looks_like="A single candle with a large bearish body and virtually no "
                   "upper or lower wick — the open is (almost) the high, and the "
                   "close is (almost) the low.",
        psychology="Sellers control the entire session with no meaningful pushback "
                   "from buyers at either end. Uncontested selling pressure for the "
                   "full period.",
        usage="Traders read a Bearish Marubozu as a strong momentum confirmation, "
              "useful both as a reversal signal after an uptrend and as a "
              "continuation signal mid-downtrend.",
        caution="A Bearish Marubozu after an already extended decline can mark a "
                "selling climax rather than a fresh breakdown — check for "
                "exhaustion before assuming the move continues.",
    ),
    dict(
        key='rising_three_methods', name='Rising Three Methods',
        tagline='A pause inside the trend, then the rally resumes',
        bias='bullish', bias_label='Bullish Continuation',
        reliability='Medium-High', best_seen='Mid-uptrend (continuation)',
        context=uptrend_context(end_level=30), trend_label='Uptrend',
        pattern=[(30, 65, 67, 28), (62, 52, 64, 50), (55, 45, 57, 43),
                 (48, 40, 50, 38), (42, 80, 82, 40)],
        looks_like="A large bullish candle, followed by three small candles that "
                   "drift lower but stay contained within the first candle's "
                   "range, followed by a final large bullish candle that closes "
                   "above the first candle's high.",
        psychology="After a strong push higher, the market takes a breather — "
                   "sellers nudge price down a little, but never with enough force "
                   "to erase the initial gain or break the range. Once that pause "
                   "is over, buyers resume control and push to a new high.",
        usage="This is a continuation pattern, not a reversal — traders use it to "
              "confirm that a pullback inside an uptrend was just a pause, not a "
              "top, and look to join the trend once the fifth candle confirms.",
        caution="If any of the three middle candles closes outside the first "
                "candle's range, the pattern is invalidated — that would suggest "
                "real selling pressure, not just a pause.",
    ),
    dict(
        key='falling_three_methods', name='Falling Three Methods',
        tagline='A pause inside the trend, then the decline resumes',
        bias='bearish', bias_label='Bearish Continuation',
        reliability='Medium-High', best_seen='Mid-downtrend (continuation)',
        context=downtrend_context(end_level=70), trend_label='Downtrend',
        pattern=[(70, 35, 72, 33), (38, 48, 50, 36), (45, 55, 57, 43),
                 (52, 60, 62, 50), (58, 20, 60, 18)],
        looks_like="A large bearish candle, followed by three small candles that "
                   "drift higher but stay contained within the first candle's "
                   "range, followed by a final large bearish candle that closes "
                   "below the first candle's low.",
        psychology="After a strong push lower, the market pauses — buyers nudge "
                   "price up a little, but never with enough force to erase the "
                   "decline or break the range. Once the pause ends, sellers "
                   "resume control and push to a new low.",
        usage="A continuation pattern traders use to confirm that a bounce inside "
              "a downtrend was just a pause, not a bottom, joining the trend once "
              "the fifth candle confirms.",
        caution="If any of the three middle candles closes outside the first "
                "candle's range, the pattern is invalidated.",
    ),
    dict(
        key='bullish_kicker', name='Bullish Kicker',
        tagline='A total, gap-driven reversal in sentiment',
        bias='bullish', reliability='High', best_seen='At the end of a downtrend',
        context=downtrend_context(end_level=60), trend_label='Downtrend',
        pattern=[(60, 40, 62, 38), (65, 85, 87, 63)],
        looks_like="A bearish candle, followed by a bullish candle that gaps up "
                   "and opens above the first candle's open — the two candles' "
                   "ranges don't overlap at all.",
        psychology="Sentiment doesn't just shift, it snaps. Whatever news or order "
                   "flow caused the gap overwhelmed the prior trend so completely "
                   "that price never even traded back into the previous candle's "
                   "range — a clean, total handover from sellers to buyers.",
        usage="Traders treat a Bullish Kicker as one of the strongest single "
              "reversal signals available, often entering as soon as the second "
              "candle confirms, with the gap itself used as a key risk level.",
        caution="Kickers are often driven by news or a major level giving way — "
                "confirm there's a real catalyst rather than a data glitch or a "
                "thin-liquidity gap before trusting it fully.",
    ),
    dict(
        key='bearish_kicker', name='Bearish Kicker',
        tagline='A total, gap-driven reversal in sentiment, downward',
        bias='bearish', reliability='High', best_seen='At the end of an uptrend',
        context=uptrend_context(end_level=40), trend_label='Uptrend',
        pattern=[(40, 60, 62, 38), (35, 15, 37, 13)],
        looks_like="A bullish candle, followed by a bearish candle that gaps down "
                   "and opens below the first candle's open — the two candles' "
                   "ranges don't overlap at all.",
        psychology="Sentiment snaps from bullish to bearish in an instant. Whatever "
                   "drove the gap down overwhelmed the prior uptrend so completely "
                   "that price never traded back into the previous candle's range.",
        usage="Traders treat a Bearish Kicker as one of the strongest single "
              "reversal signals available, often entering as soon as the second "
              "candle confirms, using the gap as a key risk level.",
        caution="Confirm there's a genuine catalyst behind the gap — news, an "
                "earnings surprise, a key level failing — rather than a thin-"
                "liquidity anomaly before trusting it fully.",
    ),
    dict(
        key='three_inside_up', name='Three Inside Up',
        tagline='A harami, then proof that buyers really meant it',
        bias='bullish', reliability='Medium-High', best_seen='After a downtrend',
        context=downtrend_context(end_level=65), trend_label='Downtrend',
        pattern=[(65, 35, 67, 33), (45, 55, 57, 43), (54, 72, 74, 52)],
        looks_like="A large bearish candle, a small bullish candle contained "
                   "inside it (a Bullish Harami), and then a third candle that "
                   "closes above the first candle's open — confirming what the "
                   "harami only hinted at.",
        psychology="The first two candles show selling pressure stalling out. The "
                   "third candle is buyers proving it wasn't a fluke — they push "
                   "price convincingly back above where the whole pattern started.",
        usage="This is essentially a Bullish Harami with its own built-in "
              "confirmation candle, which is why it's rated more reliable than a "
              "harami alone — traders can act on the third candle's close with "
              "more confidence than they could on the harami by itself.",
        caution="A weak, small third candle that barely closes above the first "
                "candle's open is a far less convincing version of this pattern.",
    ),
    dict(
        key='three_inside_down', name='Three Inside Down',
        tagline='A harami, then proof that sellers really meant it',
        bias='bearish', reliability='Medium-High', best_seen='After an uptrend',
        context=uptrend_context(end_level=35), trend_label='Uptrend',
        pattern=[(35, 65, 67, 33), (55, 45, 57, 43), (46, 28, 48, 26)],
        looks_like="A large bullish candle, a small bearish candle contained "
                   "inside it (a Bearish Harami), and then a third candle that "
                   "closes below the first candle's open — confirming the harami.",
        psychology="The first two candles show buying pressure stalling out. The "
                   "third candle is sellers proving it wasn't a fluke — they push "
                   "price convincingly back below where the whole pattern started.",
        usage="A Bearish Harami with its own built-in confirmation candle, rated "
              "more reliable than a harami alone for the same reason: the third "
              "candle removes the guesswork.",
        caution="A weak, small third candle that barely closes below the first "
                "candle's open is a far less convincing version of this pattern.",
    ),
]

# ---------------------------------------------------------------------------
# MODULE 6 — Candlestick Pattern Reliability
# ---------------------------------------------------------------------------

MODULE6_INTRO = (
    "Not every candlestick pattern deserves the same amount of trust. Some "
    "patterns represent a total, forceful handover of control that's hard to fake; "
    "others represent a much softer signal that needs real supporting evidence "
    "before it means anything. This module sorts every pattern from both volumes "
    "into three tiers, and explains what separates one tier from the next."
)


def _star_points(cx, cy, outer_r, inner_r):
    pts = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        radius = outer_r if i % 2 == 0 else inner_r
        pts.append(cx + radius * math.cos(angle))
        pts.append(cy + radius * math.sin(angle))
    return pts


def star_rating_drawing(filled, total=5, width=112, height=16):
    d = Drawing(width, height)
    outer_r, inner_r = 7.2, 3.0
    spacing = width / total
    for i in range(total):
        cx = spacing * i + spacing / 2
        cy = height / 2
        pts = _star_points(cx, cy, outer_r, inner_r)
        color = GOLD if i < filled else HexColor('#DCE1E8')
        d.add(Polygon(points=pts, fillColor=color, strokeColor=color))
    return d


def reliability_tier(stars, title, why, pattern_names):
    row = Table([[star_rating_drawing(stars), Paragraph(title, ParagraphStyle(
        'tiertitle', fontName='Helvetica-Bold', fontSize=13.5, textColor=NAVY))]],
        colWidths=[120, 340])
    row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    names = Paragraph('<b>' + ' &nbsp;•&nbsp; '.join(pattern_names) + '</b>',
                       ParagraphStyle('tiernames', fontName='Helvetica', fontSize=9.6,
                                      leading=15, textColor=NAVY, spaceBefore=6, spaceAfter=4))
    block = [row, Paragraph(why, styles['Body']), names]
    t = Table([[block]], colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, PANEL_LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 12), ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


MODULE6_TIERS = [
    dict(stars=5, title='Highest Conviction',
         why="These patterns show a total, forceful handover of control — one "
             "side didn't just win, they overwhelmed the other side completely, "
             "often across multiple candles. They're the hardest patterns to fake "
             "by accident.",
         names=['Bullish Engulfing Bar', 'Bearish Engulfing Bar', 'Morning Star',
                'Evening Star', 'Hammer', 'Shooting Star', 'Three White Soldiers',
                'Three Black Crows', 'Bullish Kicker', 'Bearish Kicker']),
    dict(stars=4, title='Strong, Lean on Confirmation',
         why="These patterns show real, meaningful pressure shifting — but "
             "slightly less decisively than a five-star pattern. They're "
             "trustworthy once confirmed by the next candle or a nearby level, "
             "but weaker as a standalone signal.",
         names=['Bullish Harami', 'Bearish Harami', 'Tweezer Tops', 'Tweezer Bottoms',
                'Doji', 'Dragonfly Doji', 'Gravestone Doji', 'Hanging Man',
                'Piercing Line', 'Dark Cloud Cover', 'Three Inside Up',
                'Three Inside Down', 'Rising Three Methods', 'Falling Three Methods']),
    dict(stars=3, title='Common, Highly Context-Dependent',
         why="These patterns show up constantly and mean very little on their "
             "own — a Marubozu is just a strong-momentum candle, and a Spinning "
             "Top (a small body with wicks on both sides, similar to a Doji but "
             "with a bit more real range) just shows a mild standoff. Both need "
             "heavy context — trend, level, and confirmation — before they're "
             "worth acting on.",
         names=['Bullish Marubozu', 'Bearish Marubozu', 'Spinning Top']),
]

# ---------------------------------------------------------------------------
# MODULE 7 — Candlestick Pattern Combinations
# ---------------------------------------------------------------------------

MODULE7_INTRO = (
    "Every module so far has taught you one ingredient at a time: structure, "
    "levels, a pattern, confirmation. Real, high-conviction setups come from "
    "stacking several of those ingredients on top of each other at the same price, "
    "at the same time. This module shows what that stacking actually looks like "
    "in practice."
)


def combo_card(parts, result, result_color, explanation):
    eq_parts = []
    for i, part in enumerate(parts):
        if i > 0:
            eq_parts.append(f'<font color="{_hex(GOLD)}"><b> + </b></font>')
        eq_parts.append(f'<b>{part}</b>')
    eq_parts.append(f'<font color="{_hex(SUBTLE)}"><b>  =  </b></font>')
    eq_line = Paragraph(''.join(eq_parts) +
                         f'<font color="{_hex(result_color)}"><b>{result}</b></font>',
                         ParagraphStyle('combo', fontName='Helvetica', fontSize=11.6,
                                        leading=18, textColor=NAVY))
    body = Paragraph(explanation, styles['Body'])
    t = Table([[[eq_line, Spacer(1, 6), body]]], colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, PANEL_LINE),
        ('LINEBEFORE', (0, 0), (0, -1), 3, result_color),
        ('TOPPADDING', (0, 0), (-1, -1), 12), ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


MODULE7_COMBOS = [
    dict(parts=['Hammer', 'Bullish Engulfing', 'Support'], result='Very Strong Setup',
         result_color=GOOD_GREEN,
         explanation="A Hammer alone is a hint. A Hammer that gets confirmed by a "
                     "Bullish Engulfing Bar, both forming right at a tested support "
                     "level, is three independent signals agreeing at the same "
                     "price — exactly the kind of confluence Module 4 is about."),
    dict(parts=['Morning Star', 'Demand Zone'], result='High Probability',
         result_color=GOOD_GREEN,
         explanation="A Morning Star is already a high-conviction, three-candle "
                     "reversal story. When that same reversal completes right "
                     "inside a demand zone — a level where large buyers have "
                     "stepped in before — the pattern and the location are "
                     "telling you the same thing at once."),
    dict(parts=['Three White Soldiers', 'Break of Structure'], result='Momentum Entry',
         result_color=GOOD_GREEN,
         explanation="Three White Soldiers already shows sustained buying "
                     "pressure. When that same move also breaks above the prior "
                     "swing high (a BOS), you have both a pattern and a structure "
                     "signal confirming the same continuation."),
    dict(parts=['Bearish Engulfing', 'Resistance', 'CHoCH'], result='High-Probability Reversal',
         result_color=BAD_RED,
         explanation="A Bearish Engulfing Bar at a resistance level is already "
                     "strong. Add a Change of Character — price breaking the last "
                     "Higher Low right as this happens — and you have pattern, "
                     "level, and structure all pointing to the same reversal."),
    dict(parts=['Doji', 'Support', 'Confirmation Candle'], result='Cautious Long Entry',
         result_color=GOLD,
         explanation="A Doji by itself is only a three-star signal (Module 6). But "
                     "a Doji at support, followed by a strong bullish confirmation "
                     "candle, has climbed the confidence ladder rung by rung — "
                     "this is how a weak pattern becomes a tradeable setup."),
]

# ---------------------------------------------------------------------------
# MODULE 8 — Fake Candlestick Signals
# ---------------------------------------------------------------------------

MODULE8_INTRO = (
    "Most beginner losses don't come from not knowing any patterns — they come "
    "from trusting a signal that was never real in the first place. This module "
    "covers the most common ways candlesticks lie, and how to protect yourself "
    "from each one."
)

MODULE8_TOPICS = [
    dict(
        title='Fake Engulfings',
        paragraphs=[
            "Not every candle that technically engulfs the last one carries real "
            "weight. A tiny prior candle is trivial to engulf — the resulting "
            "\"engulfing bar\" can look textbook-perfect while representing very "
            "little actual buying or selling pressure. Compare the size of the "
            "engulfing candle to several candles before it, not just the one "
            "immediately prior.",
        ],
    ),
    dict(
        title='False Hammers',
        paragraphs=[
            "A small body with a long lower wick means nothing if it isn't sitting "
            "after a real downtrend or at a real support level. Context is what "
            "turns the shape into a signal — a hammer-shaped candle in the middle "
            "of a range is just noise wearing a costume.",
        ],
    ),
    dict(
        title='News Candles',
        paragraphs=[
            "A candle formed during a major news release (interest rate decisions, "
            "employment data, central bank speeches) can spike, wick, and reverse "
            "violently for reasons that have nothing to do with normal technical "
            "structure. Treat patterns that form during these windows with extra "
            "suspicion, or simply sit out until the volatility settles.",
        ],
    ),
    dict(
        title='Low Liquidity',
        paragraphs=[
            "When very few participants are trading — late in the session, during "
            "holidays, in thinly traded instruments — it takes very little order "
            "flow to create a dramatic-looking candle. A pattern formed on thin "
            "liquidity is far more prone to snapping back the moment normal "
            "trading volume returns.",
        ],
    ),
    dict(
        title='Weekend Gaps',
        paragraphs=[
            "Markets that close over the weekend can reopen at a noticeably "
            "different price than where they closed, creating a gap on the chart "
            "that has nothing to do with a candlestick pattern — it's simply the "
            "market repricing for news that happened while it was shut. Don't "
            "read a weekend gap as an engulfing or kicker pattern; check the "
            "calendar before you interpret it.",
        ],
    ),
    dict(
        title='Fake Breakouts',
        paragraphs=[
            "Price pushes through a support or resistance level, triggers a wave "
            "of breakout entries — and then reverses right back inside the prior "
            "range, leaving all of those entries underwater. This is exactly the "
            "Fakeout concept from Volume I's glossary; the safest way to avoid it "
            "is to wait for a retest of the broken level before entering, rather "
            "than chasing the breakout candle itself.",
        ],
    ),
    dict(
        title='Bull Traps',
        paragraphs=[
            "A bull trap is a fake breakout above resistance that lures buyers in "
            "right before price reverses hard and falls back below the level. "
            "The breakout candle looks convincing precisely because it's designed "
            "to — whether by genuine short-term momentum or by larger players "
            "using retail breakout buying as an exit.",
        ],
        drawing=structure_drawing(
            [(0.06, 45, None, 'low'), (0.24, 62, None, 'high'), (0.42, 52, None, 'low'),
             (0.60, 78, None, 'high'), (0.94, 32, None, 'low')],
            ref_line=62, ref_label='Resistance', ref_color=GOLD, break_from=2,
            annotation=('Bull Trap', TRAP_ORANGE), annotation_color=TRAP_ORANGE,
            trend_label='Fake Breakout'),
        caption='Figure — Price fakes a break above resistance, then reverses hard back below it.',
    ),
    dict(
        title='Bear Traps',
        paragraphs=[
            "A bear trap is the mirror image: a fake breakdown below support that "
            "lures short-sellers in right before price reverses hard and rallies "
            "back above the level, forcing those shorts to buy back at a loss and "
            "fueling the reversal even further.",
        ],
        drawing=structure_drawing(
            [(0.06, 55, None, 'high'), (0.24, 38, None, 'low'), (0.42, 48, None, 'high'),
             (0.60, 22, None, 'low'), (0.94, 68, None, 'high')],
            ref_line=38, ref_label='Support', ref_color=GOLD, break_from=2,
            annotation=('Bear Trap', TRAP_ORANGE), annotation_color=TRAP_ORANGE,
            trend_label='Fake Breakdown'),
        caption='Figure — Price fakes a break below support, then reverses hard back above it.',
    ),
]

# ---------------------------------------------------------------------------
# MODULE 9 — Candlesticks on Different Timeframes
# ---------------------------------------------------------------------------

MODULE9_INTRO = (
    "Every candle you've studied so far has an unspoken assumption baked into it: "
    "a time period. A candle can represent one minute or one month — the shape "
    "rules are identical, but what the shape means to a trader changes enormously "
    "depending on which timeframe you're looking at."
)

MODULE9_TIMEFRAMES = [
    ('1 Minute', "Pure execution speed. Extremely noisy — most \"patterns\" here "
                 "are just randomness. Useful only for fine-tuning the exact "
                 "second of an entry you already decided on elsewhere."),
    ('3 Minute', "Slightly smoother than the 1-minute, still dominated by noise. "
                 "Common on fast HFX execution platforms, rarely useful alone."),
    ('5 Minute', "One of the most common HFX / binary options execution "
                 "timeframes — enough candles to see short-term structure, still "
                 "fast enough for short-expiry trading."),
    ('15 Minute', "A short-term momentum view. Enough data to see a real trend "
                  "and real support/resistance, while still updating quickly."),
    ('30 Minute', "A session-level view — useful for seeing how price has behaved "
                  "across a single trading session (e.g. the London or New York "
                  "session)."),
    ('1 Hour', "A solid intraday trend reference. Many day traders use the "
               "1-Hour chart as their primary \"what's the trend right now\" "
               "check before dropping to a lower timeframe to execute."),
    ('4 Hour', "A swing-level structure view. Higher Highs and Higher Lows here "
               "represent moves that can last days, not minutes."),
    ('Daily', "The primary trend reference for most retail traders. Support, "
              "resistance, and structure on the Daily chart tend to matter more "
              "than the same levels on any lower timeframe."),
    ('Weekly', "Major structural trend. Levels here can hold for months and are "
               "watched closely by larger, longer-term participants."),
    ('Monthly', "Multi-year structural context — mainly relevant to macro and "
                "position traders. Rarely needed for HFX or binary options "
                "execution, but useful for understanding \"the big picture.\""),
]

MODULE9_HTF_DRAWING = [
    Paragraph('Higher Timeframe Controls Lower Timeframe', styles['SectionHeading']),
    Paragraph(
        "Here is the single most important idea in this module: whatever the "
        "higher timeframe is doing outranks whatever the lower timeframe is "
        "doing. A lower-timeframe chart can show a convincing-looking CHoCH or "
        "even a full reversal — and it can still just be a pullback once you "
        "zoom out. When your timeframes disagree, the higher timeframe wins.",
        styles['Body']),
    Spacer(1, 6),
    structure_drawing(
        [(0.05, 20, None, 'low'), (0.25, 45, 'HH', 'high'), (0.45, 32, 'HL', 'low'),
         (0.65, 62, 'HH', 'high'), (0.85, 48, 'HL', 'low'), (0.97, 58, None, None)],
        trend_label='Daily — Higher Timeframe'),
    Paragraph('The Daily chart shows a clean, healthy uptrend.', styles['Caption']),
    Spacer(1, 8),
    structure_drawing(
        [(0.05, 82, None, 'high'), (0.30, 55, 'LH', 'high'), (0.55, 68, None, 'high'),
         (0.80, 40, 'LL', 'low'), (0.97, 50, None, None)],
        annotation=('Looks bearish here...', TRAP_ORANGE), annotation_color=TRAP_ORANGE,
        trend_label='15-Minute — Lower Timeframe'),
    Paragraph('...but this entire panel is just the pullback leg between the Daily HH and HL above — '
              'zoom out before you trust it.', styles['Caption']),
]

# ---------------------------------------------------------------------------
# MODULE 10 — The OneWay FX Candlestick Strategy
# ---------------------------------------------------------------------------

MODULE10_INTRO = (
    "Everything in this book compresses into one repeatable checklist. It won't "
    "make every trade a winner — nothing does — but it will keep you from taking "
    "the low-quality setups that cause most beginner losses. Run every trade "
    "idea through these eight questions, in order, before you risk a single "
    "dollar."
)

MODULE10_CHECKLIST = [
    ("1. What's the trend?", "Check Module 1's structure first: Higher Highs and "
     "Higher Lows, Lower Highs and Lower Lows, or a range? Only take reversal "
     "patterns at the end of a trend, and continuation patterns with the trend."),
    ("2. Is there a support or resistance level here?", "Check Module 2: is "
     "price at a horizontal level, a dynamic trendline, or a psychological round "
     "number? No level nearby is a reason to keep waiting."),
    ("3. Is there an actual candlestick pattern?", "From Volume I or Module 5: "
     "has price formed a recognizable pattern at this level, or are you just "
     "hoping one is about to appear?"),
    ("4. Has it been confirmed?", "Per Module 4: has the next candle closed in "
     "the expected direction? Don't front-run the confirmation."),
    ("5. Is the risk/reward worth it?", "Compare the distance from your entry to "
     "your stop loss against the distance from your entry to your target. A "
     "poor risk/reward isn't worth taking even when everything else lines up."),
    ("6. Define your entry.", "Decide the exact price or condition you'll enter "
     "at — before you're in the trade, not after."),
    ("7. Define your stop loss.", "Set the price that proves the setup was "
     "wrong, based on the structure itself (just beyond the pattern's high or "
     "low) — not on how much you feel like risking."),
    ("8. Define your take profit.", "Set a realistic target — often the next "
     "meaningful support or resistance level — before you enter, so it isn't an "
     "emotional decision made mid-trade."),
]

MODULE10_EXAMPLE_DRAWING = structure_drawing(
    [(0.05, 55, None, 'high'), (0.28, 24, None, 'low'), (0.50, 45, None, None),
     (0.72, 66, None, None), (0.95, 80, None, None)],
    zone=(16, 26), zone_color=BULL_GREEN,
    levels=[(70, 'Take Profit', BULL_GREEN), (30, 'Entry', GOLD), (18, 'Stop Loss', BEAR_RED)],
    trend_label='Worked Example')

# ---------------------------------------------------------------------------
# MODULE 11 — Trade Case Studies (illustrative examples)
# ---------------------------------------------------------------------------

MODULE11_INTRO = (
    "The examples in this module are illustrative teaching diagrams, not real "
    "historical charts or actual trades. Each one pairs a common mistake with the "
    "disciplined version of the same decision, using the ideas from every module "
    "before this one. Read each pair and try to spot which rule from Module 12 it "
    "connects to before you turn the page."
)


def case_study(number, title, bad, good, lesson, drawing=None):
    head = Paragraph(f'Case {number} — {title}', styles['SubHeading'])
    tag_style = ParagraphStyle('casetag', fontName='Helvetica-Bold', fontSize=8.8,
                                textColor=colors.white, alignment=TA_CENTER)
    bad_tag = Table([[Paragraph('BAD TRADE', tag_style)]], colWidths=[80])
    bad_tag.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BAD_RED),
                                  ('TOPPADDING', (0, 0), (-1, -1), 4),
                                  ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    good_tag = Table([[Paragraph('GOOD TRADE', tag_style)]], colWidths=[80])
    good_tag.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), GOOD_GREEN),
                                   ('TOPPADDING', (0, 0), (-1, -1), 4),
                                   ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    rows = [[bad_tag, Paragraph(bad, styles['Body'])],
            [good_tag, Paragraph(good, styles['Body'])]]
    t = Table(rows, colWidths=[88, 380])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('TOPPADDING', (0, 0), (-1, -1), 6),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    block = [head, t, Paragraph(
        f'<font color="{_hex(GOLD)}"><b>Lesson —</b></font> <i>{lesson}</i>', styles['Body'])]
    if drawing is not None:
        block.append(Spacer(1, 4))
        block.append(drawing)
    return KeepTogether(block)


MODULE11_CASES = [
    dict(number=1, title='Chasing the Candle',
         bad="A trader sees a big bullish candle already three-quarters formed "
             "and jumps in mid-candle out of fear of missing out — no confirmation, no plan.",
         good="A trader sees the same candle, waits for it to close, waits for "
              "the next candle to confirm, and enters with a clear stop below the recent low.",
         lesson="Chasing a candle mid-formation means you have no idea yet "
                "whether it will hold — you're buying a story that hasn't finished being written."),
    dict(number=2, title='Buying Into Resistance',
         bad="Price rallies into a well-tested resistance level and a trader "
             "buys anyway because \"it looks strong,\" ignoring Module 2 entirely.",
         good="A trader recognizes the same resistance level, waits to see "
              "whether price breaks and holds above it or gets rejected, and only "
              "acts on whichever outcome actually happens.",
         lesson="Never buy into resistance or sell into support — Module 12's "
                "first rule exists because of exactly this mistake."),
    dict(number=3, title='No Stop Loss',
         bad="A trader enters with no predefined stop loss \"because this one "
             "will definitely work,\" and the trade moves steadily against them "
             "with no exit plan.",
         good="A trader defines a stop loss before entering, sized to a specific "
              "invalidation point in the structure, and exits immediately and "
              "unemotionally when it's hit.",
         lesson="A stop loss isn't pessimism — it's simply the price at which "
                "your original idea is proven wrong."),
    dict(number=4, title='Oversized Risk',
         bad="A trader risks 20% of their account on a single \"can't miss\" setup.",
         good="A trader risks 1–2% of their account on the same setup, sized so "
              "that even a string of losses can't meaningfully damage the account.",
         lesson="Position size determines how many mistakes you're allowed to "
                "make before you're out of the game — keep that number high."),
    dict(number=5, title='Trading a Fake Breakout',
         bad="Price breaks above resistance and a trader buys the breakout "
             "candle immediately, only to watch price reverse back below the "
             "level minutes later — a textbook bull trap.",
         good="A trader waits for price to retest the broken level from above "
              "and hold before entering — missing the very top of the move but "
              "avoiding the trap entirely.",
         lesson="The retest costs you some of the move, but it's the difference "
                "between trading the breakout and being trapped by it.",
         drawing=split_drawing_row(
             structure_drawing(
                 [(0.1, 50, None, 'low'), (0.4, 65, None, 'high'), (0.7, 85, None, 'high'),
                  (1.0, 35, None, 'low')],
                 width=227, ref_line=65, ref_label='Resistance', ref_color=GOLD,
                 break_from=1, arrows=[(2, 'down', BAD_RED)]),
             'Bad — bought the breakout candle directly.',
             structure_drawing(
                 [(0.1, 50, None, 'low'), (0.35, 65, None, 'high'), (0.55, 85, None, 'high'),
                  (0.75, 66, None, 'low'), (1.0, 80, None, 'high')],
                 width=227, ref_line=65, ref_label='Resistance', ref_color=GOLD,
                 break_from=1, arrows=[(3, 'up', GOOD_GREEN)]),
             'Good — waited for the retest to hold.',
         )),
    dict(number=6, title='Ignoring the News Calendar',
         bad="A trader takes a textbook Hammer signal two minutes before a "
             "major interest rate announcement, and the resulting volatility "
             "spike stops them out for reasons that had nothing to do with the pattern.",
         good="A trader checks the calendar first, sees the announcement is "
              "imminent, and either waits until the volatility settles or sits the session out.",
         lesson="The best-looking pattern in the world can't survive being run "
                "over by a scheduled news event."),
    dict(number=7, title='Averaging Down Into a Downtrend',
         bad="A trader buys a falling instrument, watches it fall further, and "
             "adds size at each new low to \"improve their average price,\" with "
             "no structural reason to believe the decline is over.",
         good="A trader waits for actual structure to shift — a Change of "
              "Character, then a Break of Structure — before considering a long "
              "position at all.",
         lesson="Adding to a losing position because it's cheaper isn't a "
                "strategy — it's hoping, and hope isn't confirmation."),
    dict(number=8, title='Trading Against a Strong Higher-Timeframe Trend',
         bad="A trader spots a bearish pattern on a 5-minute chart and shorts "
             "it, without checking that the Daily chart is in a powerful, "
             "well-established uptrend.",
         good="A trader checks the Daily trend first (Module 9), sees the "
              "strong uptrend, and either skips the short entirely or only takes "
              "bullish setups on the lower timeframe.",
         lesson="The higher timeframe controls the lower timeframe — fighting "
                "it is fighting the larger trend for a small, risky reward."),
    dict(number=9, title='Ignoring a Confirmed CHoCH',
         bad="A trader stays long through a clear Change of Character, telling "
             "themselves the uptrend \"always comes back,\" and rides the "
             "position deep into what becomes a full reversal.",
         good="A trader treats the CHoCH as the early warning it is, exits or "
              "tightens the stop immediately, and waits for new structure to "
              "form before considering a new position.",
         lesson="A CHoCH doesn't guarantee a reversal, but it removes your "
                "right to assume the old trend is still safe.",
         drawing=split_drawing_row(
             structure_drawing(
                 [(0.06, 30, None, 'low'), (0.28, 55, 'HH', 'high'), (0.50, 42, 'HL', 'low'),
                  (0.72, 60, None, 'high'), (0.94, 25, None, 'low')],
                 width=227, ref_line=42, ref_color=SHIFT_VIOLET, break_from=2,
                 arrows=[(2, 'down', BAD_RED)], annotation=('Stayed long', BAD_RED),
                 annotation_color=BAD_RED),
             'Bad — ignored the CHoCH and held on.',
             structure_drawing(
                 [(0.06, 30, None, 'low'), (0.28, 55, 'HH', 'high'), (0.50, 42, 'HL', 'low'),
                  (0.72, 60, None, 'high'), (0.94, 25, None, 'low')],
                 width=227, ref_line=42, ref_color=SHIFT_VIOLET, break_from=2,
                 arrows=[(2, 'down', GOOD_GREEN)], annotation=('Exited here', GOOD_GREEN),
                 annotation_color=GOOD_GREEN),
             'Good — treated the CHoCH as an exit signal.',
         )),
    dict(number=10, title='Moving the Stop Loss Further Away',
         bad="A trade moves against a trader, and instead of accepting the "
             "loss, they drag their stop loss further away \"to give it more "
             "room,\" turning a small planned loss into a large unplanned one.",
         good="A trader honors the original stop loss exactly where the "
              "structure said it should be, takes the small loss, and moves on "
              "to the next setup with capital intact.",
         lesson="Moving your stop to avoid being wrong doesn't change whether "
                "you were wrong — it only changes how much it costs to find out."),
    dict(number=11, title='Trading the Pattern Alone',
         bad="A trader takes a Doji purely because \"Doji means reversal,\" "
             "with no trend context, no level, and no confirmation behind it.",
         good="A trader waits until that same Doji forms at a tested support "
              "level with a strong confirming candle behind it — turning a "
              "three-star pattern into a genuinely tradeable setup (Module 7).",
         lesson="The pattern is the least important ingredient in a good trade "
                "— context is what does most of the work."),
    dict(number=12, title='Revenge Trading After a Loss',
         bad="A trader takes a loss, immediately re-enters a lower-quality "
             "version of the same trade to \"win it back,\" and compounds the damage.",
         good="A trader takes the loss, steps away for the session if needed, "
              "and returns only once they can evaluate the next setup on its own merits.",
         lesson="The market doesn't know or care that you're trying to get "
                "even — trading emotionally after a loss is how one bad trade "
                "becomes three."),
]

# ---------------------------------------------------------------------------
# MODULE 12 — Candlestick Trading Rules
# ---------------------------------------------------------------------------

MODULE12_INTRO = (
    "Every idea in this book eventually compresses into a short list of rules "
    "you can recall in the middle of a live trade, when you don't have time to "
    "re-read a chapter. These are the OneWay FX rules — pin them somewhere you'll "
    "actually see them."
)

MODULE12_RULES = [
    ("Never chase candles.", "If you didn't plan the entry before the candle "
     "formed, you're reacting, not trading — go back to Module 10's checklist instead."),
    ("Wait for candle close.", "A candle can look like anything mid-formation. "
     "Only a closed candle has actually told you who won."),
    ("Never buy into resistance.", "Even a perfect bullish pattern is fighting "
     "the level, not just the trend, if it forms right under resistance."),
    ("Never sell into support.", "The mirror rule — a bearish pattern at "
     "support is fighting a level that has already proven it can hold."),
    ("Always know the trend.", "Module 1 comes before every other module for a "
     "reason: direction changes what every pattern means."),
    ("Risk only 1–2% per trade.", "Position size is the one variable you fully "
     "control — keep it small enough that a losing streak can't end your account."),
    ("Don't trade emotionally.", "Revenge trades, FOMO entries, and moved stop "
     "losses are all the same mistake wearing a different outfit — see Module 11."),
    ("Follow your trading plan.", "A plan you abandon under pressure was never "
     "really a plan — it was a suggestion you agreed with in advance."),
]


def rule_item(num, rule, why):
    return KeepTogether([Paragraph(f'{num}.&nbsp;&nbsp;{rule}', styles['RuleText']),
                          Paragraph(why, styles['RuleWhy']),
                          HR(468, color=PANEL_LINE, thickness=0.6, space_before=0, space_after=8)])

# ---------------------------------------------------------------------------
# Expanded Glossary — 75 intermediate / advanced terms
# ---------------------------------------------------------------------------

GLOSSARY2 = [
    ('Break of Structure (BOS)', "Price breaking through the most recent "
     "significant swing high or low in the direction of the existing trend, "
     "confirming the trend is still in control."),
    ('Change of Character (CHoCH)', "Price breaking structure against the "
     "prevailing trend for the first time, often the earliest sign a reversal "
     "may be starting."),
    ('Liquidity', "The pool of resting buy and sell orders sitting at a price "
     "level; more liquidity makes it easier to enter or exit a position without "
     "moving price."),
    ('Liquidity Grab', "A sharp move into a level known to hold a cluster of "
     "orders — such as stop losses — designed to trigger them before price reverses."),
    ('Liquidity Sweep', "Price briefly pushing past a recent high or low to "
     "trigger resting orders there before snapping back the other way — closely "
     "related to a liquidity grab."),
    ('Supply Zone', "A price area where selling pressure has previously "
     "overwhelmed buyers — similar to a resistance zone, but referring to the "
     "order cluster behind it."),
    ('Demand Zone', "A price area where buying pressure has previously "
     "overwhelmed sellers — similar to a support zone, but referring to the "
     "order cluster behind it."),
    ('Mitigation', "When price returns to an order block or zone and the "
     "orders left behind are finally filled, \"mitigating\" the unfinished "
     "business at that level."),
    ('Order Block', "The last opposing candle before a strong, decisive move, "
     "believed to mark where large institutional orders were placed."),
    ('Fair Value Gap (FVG)', "A gap left between candles by a fast, "
     "one-directional move, which price often returns to \"fill\" before continuing."),
    ('Premium', "The upper portion of a recent price range, generally "
     "considered an area to look for selling rather than buying."),
    ('Discount', "The lower portion of a recent price range, generally "
     "considered an area to look for buying rather than selling."),
    ('Imbalance', "A general term for an area on the chart where buying and "
     "selling were not evenly matched, often visible as a Fair Value Gap."),
    ('Displacement', "A strong, fast, decisive move that shows one side of the "
     "market taking clear control, often leaving a Fair Value Gap behind it."),
    ('Rejection', "A sharp reversal away from a price level, usually shown by "
     "a long wick, signaling that side of the market was firmly turned back."),
    ('Continuation', "Price resuming its prior trend after a pause, rather "
     "than reversing."),
    ('Exhaustion', "A sign that a trend has run out of momentum, often shown "
     "by shrinking candle bodies or a failure to make further progress."),
    ('Compression', "Price action tightening into a smaller and smaller "
     "range, often building up energy for a larger move."),
    ('Consolidation', "A period where price moves sideways within a range "
     "rather than trending."),
    ('Expansion', "A sudden increase in range and volatility after a period "
     "of compression."),
    ('Volatility', "How much and how quickly price moves over a given period."),
    ('Momentum', "The speed and strength of a price move in one direction."),
    ('Confluence', "Multiple independent signals — a pattern, a level, a "
     "trend, an indicator — lining up at the same price at the same time, "
     "strengthening the case for a trade."),
    ('Pullback', "A short, temporary move against the prevailing trend before "
     "the trend resumes."),
    ('Retracement', "A partial reversal within a larger trend, typically "
     "measured as a percentage of the prior move."),
    ('Impulse Move', "A strong, fast move in the direction of the trend, "
     "usually the \"legs\" of a larger structure."),
    ('Correction', "A broader pullback within a trend — larger and more "
     "drawn-out than a simple retracement."),
    ('Trendline', "A line drawn along a series of swing highs or swing lows "
     "to visualize the slope of a trend."),
    ('Channel', "A pair of parallel trendlines containing price, one acting "
     "as dynamic support and the other as dynamic resistance."),
    ('Mean Reversion', "The tendency of price to eventually move back toward "
     "its average after stretching unusually far away from it."),
    ('Session High', "The highest price traded during a specific trading "
     "session, such as the Asian, London, or New York session."),
    ('Session Low', "The lowest price traded during a specific trading session."),
    ('Daily High', "The highest price traded during the current trading day."),
    ('Daily Low', "The lowest price traded during the current trading day."),
    ('Previous Day High', "The prior day's high, often watched as a "
     "short-term support/resistance reference."),
    ('Previous Day Low', "The prior day's low, often watched as a short-term "
     "support/resistance reference."),
    ('Asian Range', "The high-to-low price range formed during the Asian "
     "trading session, often used as a reference for the more volatile "
     "sessions that follow."),
    ('London Open', "The start of the London trading session, one of the "
     "most active windows in the FX trading day."),
    ('New York Open', "The start of the New York trading session, which "
     "overlaps with London and often brings the day's highest volume."),
    ('Kill Zone', "A specific window of time — such as the London Open or New "
     "York Open — when a particular market is expected to see its most "
     "significant, high-probability moves."),
    ('Stop Hunt', "A move designed to trigger a cluster of stop-loss orders "
     "resting just beyond an obvious high or low before reversing — closely "
     "related to a liquidity grab."),
    ('Swing High', "A candle or price point with lower highs on both sides of "
     "it, marking a local turning point to the downside."),
    ('Swing Low', "A candle or price point with higher lows on both sides of "
     "it, marking a local turning point to the upside."),
    ('Internal Structure', "The smaller swing highs and lows that form on a "
     "lower timeframe inside a larger, higher-timeframe structural move."),
    ('External Structure', "The major swing highs and lows that define the "
     "higher-timeframe trend itself."),
    ('Higher Timeframe (HTF)', "A longer-period chart — such as the Daily or "
     "4-Hour — used to establish the dominant trend and context."),
    ('Lower Timeframe (LTF)', "A shorter-period chart — such as the 5-Minute "
     "or 15-Minute — used to fine-tune entries within the higher timeframe's direction."),
    ('Multi-Timeframe Analysis (MTF)', "The practice of checking several "
     "different timeframes together before taking a trade, rather than "
     "relying on just one."),
    ('Top-Down Analysis', "Starting from the highest relevant timeframe to "
     "establish trend and bias, then working down to lower timeframes to time "
     "the entry."),
    ('Accumulation', "A phase where large participants quietly build a "
     "position, often marked by sideways, range-bound price action."),
    ('Distribution', "A phase where large participants quietly sell off a "
     "position, often marked by sideways price action at the top of a move."),
    ('Markup', "The phase of a market cycle where price trends strongly "
     "higher after accumulation."),
    ('Markdown', "The phase of a market cycle where price trends strongly "
     "lower after distribution."),
    ('Smart Money', "A general term for large, well-informed, well-"
     "capitalized market participants — institutions, banks, large funds — "
     "believed to move price more deliberately than retail traders."),
    ('Retail Trap', "A setup that looks attractive to everyday retail traders "
     "but is designed, or happens, to catch them on the wrong side of the move."),
    ('Bull Trap', "A fake breakout above resistance that lures buyers in "
     "before price reverses sharply lower."),
    ('Bear Trap', "A fake breakdown below support that lures sellers in "
     "before price reverses sharply higher."),
    ('Inducement', "A minor move designed to draw in early entries or "
     "trigger stop losses before the real move happens in the opposite direction."),
    ('Equal Highs (EQH)', "Two or more swing highs sitting at almost exactly "
     "the same price, often marking a liquidity target above the market."),
    ('Equal Lows (EQL)', "Two or more swing lows sitting at almost exactly "
     "the same price, often marking a liquidity target below the market."),
    ('Liquidity Pool', "A cluster of resting orders, often stop losses, built "
     "up around equal highs, equal lows, or other obvious levels."),
    ('Point of Interest (POI)', "A specific price area a trader is watching "
     "for a potential reaction, such as an order block, supply/demand zone, "
     "or Fair Value Gap."),
    ('Institutional Candle', "A single candle with an unusually large range "
     "or body relative to recent candles, suggesting large-size participation."),
    ('Wick Rejection', "A long wick showing that price was pushed to an "
     "extreme and firmly rejected before the candle closed."),
    ('Range Expansion', "A sudden increase in the size of candle ranges, "
     "often signaling the start of a stronger directional move."),
    ('Volatility Contraction', "A period where candle ranges shrink and "
     "price moves less, often preceding a breakout."),
    ('Breakout Retest', "Price returning to a broken support or resistance "
     "level to test whether it will now act as the opposite (see Role "
     "Reversal), before continuing."),
    ('Failure Swing', "An attempted new high or low that fails to hold, "
     "often an early warning of a change in structure."),
    ('Spring', "A brief false break below a trading range's support (a "
     "Wyckoff term) that quickly reverses, often marking the real start of a "
     "move higher."),
    ('Upthrust', "A brief false break above a trading range's resistance (a "
     "Wyckoff term) that quickly reverses, often marking the real start of a "
     "move lower."),
    ('Risk-to-Reward Ratio (R:R)', "The size of your potential loss compared "
     "to your potential gain on a trade, usually expressed as a ratio like "
     "1:2 or 1:3."),
    ('Position Sizing', "Deciding how large a trade to take, usually based "
     "on your account size and how much you're willing to risk."),
    ('Drawdown', "The decline in your account balance from a recent peak, "
     "typically measured as a percentage."),
    ('Win Rate', "The percentage of your trades that end as winners, often "
     "less important on its own than your risk-to-reward ratio."),
    ('Expectancy', "The average amount you can expect to make or lose per "
     "trade over the long run, combining your win rate and your risk-to-"
     "reward ratio into a single number."),
]

# ---------------------------------------------------------------------------
# Document template: cover, header/footer, page templates
# ---------------------------------------------------------------------------

def cover_page_canvas(c, doc):
    c.saveState()
    c.setFillColor(NAVY_DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H * 0.28, PAGE_W, PAGE_H * 0.72, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(MARGIN, PAGE_H * 0.28, PAGE_W - MARGIN, PAGE_H * 0.28)
    import random
    random.seed(19)
    base_y = PAGE_H * 0.16
    xs = list(range(int(MARGIN) + 10, int(PAGE_W - MARGIN) - 10, 26))
    levels = []
    lvl = 40
    for i in range(len(xs)):
        lvl += random.choice([-14, -6, 4, 12, 18, -10])
        lvl = max(10, min(90, lvl))
        levels.append(lvl)
    for i, x in enumerate(xs):
        o = levels[i]
        c2 = levels[i] + random.choice([-16, -8, 6, 14, 20])
        c2 = max(5, min(95, c2))
        hi = max(o, c2) + random.randint(3, 10)
        lo = min(o, c2) - random.randint(3, 10)
        bull = c2 >= o
        color = BULL_GREEN if bull else BEAR_RED
        scale = 0.9
        y0 = base_y
        c.setStrokeColor(HexColor('#3A4E6E'))
        c.setLineWidth(1)
        c.line(x, y0 + lo * scale, x, y0 + hi * scale)
        c.setFillColor(color)
        top, bottom = max(o, c2), min(o, c2)
        c.rect(x - 6, y0 + bottom * scale, 12, max((top - bottom) * scale, 2), fill=1, stroke=0)
    c.restoreState()


def header_footer(c, doc, title_text):
    c.saveState()
    c.setStrokeColor(PANEL_LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    c.setFont('Helvetica', 8.3)
    c.setFillColor(SUBTLE)
    c.drawString(MARGIN, PAGE_H - 0.55 * inch, 'ONEWAY FX  |  EDUCATION SERIES  |  VOLUME II')
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.55 * inch, title_text)
    c.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    c.setFont('Helvetica', 8.3)
    c.drawString(MARGIN, 0.46 * inch, 'Reading the Story Behind Price Action')
    c.drawRightString(PAGE_W - MARGIN, 0.46 * inch, f'Page {doc.page - 1}')
    c.restoreState()


def onFirstPage(c, doc):
    cover_page_canvas(c, doc)


def onLaterPages(c, doc):
    header_footer(c, doc, 'onewayfx.com')


def timeframe_table(rows):
    data = [[Paragraph('TIMEFRAME', styles['GlanceLabel']), Paragraph("WHAT IT'S FOR", styles['GlanceLabel'])]]
    for name, desc in rows:
        data.append([Paragraph(f'<b>{name}</b>', styles['GlanceValue']), Paragraph(desc, styles['Body'])])
    t = Table(data, colWidths=[92, 376])
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), PANEL_BG),
        ('LINEBELOW', (0, 0), (-1, 0), 0.75, PANEL_LINE),
        ('LINEBELOW', (0, 1), (-1, -2), 0.4, PANEL_LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]
    t.setStyle(TableStyle(style))
    return t


def module5_pattern_block(idx, p):
    block = []
    block.append(Paragraph(f'PATTERN {idx + 1} OF {len(MODULE5_PATTERNS)}', styles['ChapterKicker']))
    block.append(pattern_header_table(p['name'], p['tagline']))
    block.append(Spacer(1, 10))
    block.append(glance_table(p['bias'], p['reliability'], p['best_seen'], bias_label=p.get('bias_label')))
    story_block = [KeepTogether(block), Spacer(1, 10)]
    drawing = pattern_drawing(p['context'], p['pattern'], p['bias'], p['trend_label'],
                               bias_label=p.get('bias_label'))
    story_block.append(KeepTogether([drawing,
                        Paragraph(f'Figure — {p["name"]}: prior trend, the pattern, and its implied bias.',
                                  styles['Caption'])]))
    story_block.append(KeepTogether([Paragraph('What it looks like', styles['SubHeading']),
                                      Paragraph(p['looks_like'], styles['Body'])]))
    story_block.append(KeepTogether([Paragraph('The psychology behind it', styles['SubHeading']),
                                      Paragraph(p['psychology'], styles['Body'])]))
    story_block.append(KeepTogether([Paragraph('How OneWay FX traders use it', styles['SubHeading']),
                                      Paragraph(p['usage'], styles['Body'])]))
    story_block.append(KeepTogether([Paragraph('Caution', styles['SubHeading']),
                                      Paragraph(p['caution'], styles['Body'])]))
    return story_block


def build():
    doc = BaseDocTemplate(OUT_PATH, pagesize=letter,
                           leftMargin=MARGIN, rightMargin=MARGIN,
                           topMargin=0.95 * inch, bottomMargin=0.85 * inch,
                           title="OneWay FX Volume II — Reading the Story Behind Price Action",
                           author="OneWay FX")

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id='cover', leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0)
    content_frame = Frame(MARGIN, doc.bottomMargin, PAGE_W - 2 * MARGIN,
                           PAGE_H - doc.topMargin - doc.bottomMargin, id='content')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[cover_frame], onPage=onFirstPage),
        PageTemplate(id='Content', frames=[content_frame], onPage=onLaterPages),
    ])

    story = []

    # ---------------- Cover ----------------
    cover_story = [
        Spacer(1, PAGE_H * 0.28),
        Paragraph('ONEWAY FX', ParagraphStyle('brand', fontName='Helvetica-Bold', fontSize=15,
                   textColor=GOLD, alignment=TA_CENTER, tracking=3)),
        Spacer(1, 14),
        Paragraph('Reading the Story<br/>Behind Price Action', styles['CoverTitle']),
        Spacer(1, 10),
        Paragraph('Volume II — Combining Candlesticks with Market Structure,<br/>'
                  'Confirmation, and Probability', styles['CoverSubtitle']),
        Spacer(1, PAGE_H * 0.19),
        Paragraph('Education Series &nbsp;•&nbsp; Volume II', styles['CoverFooter']),
        Paragraph('onewayfxsupport@gmail.com', styles['CoverFooter']),
    ]
    story.append(NextPageTemplate('Cover'))
    story.extend(cover_story)
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # ---------------- Risk disclosure ----------------
    story.append(Paragraph('IMPORTANT NOTICE', styles['ChapterKicker']))
    story.append(Paragraph('Risk Disclosure', styles['ChapterTitle']))
    story.append(gold_rule())
    story.append(Paragraph(
        "This is Volume II of the OneWay FX Education Series, published for "
        "educational purposes only. It builds on Volume I and introduces market "
        "structure, support and resistance, confirmation, advanced candlestick "
        "patterns, and a repeatable strategy framework. Nothing in this book is "
        "financial advice, a recommendation to trade, or a guarantee of any "
        "outcome.", styles['Body']))
    story.append(warn_box('Please read before continuing', [
        "HFX and binary options trading carries a very high level of risk and is "
        "not suitable for every investor — it is possible to lose some, or all, "
        "of your invested capital.",
        "Every case study in Module 11 is an illustrative teaching example, not "
        "a real historical chart or an actual trade. No pattern, framework, or "
        "checklist in this book works every time.",
        "Concepts like liquidity, order blocks, and Fair Value Gaps are widely "
        "used in modern trading education, but remain debated in how precisely "
        "predictive they are — treat them as one more tool, not a guarantee.",
        "Never trade with money you cannot afford to lose. Use proper risk "
        "management, and confirm the products available to you are permitted in "
        "your jurisdiction.",
    ]))
    story.append(PageBreak())

    # ---------------- Table of contents ----------------
    story.append(Paragraph('CONTENTS', styles['ChapterKicker']))
    story.append(Paragraph('Table of Contents', styles['ChapterTitle']))
    story.append(gold_rule())

    toc_parts = [
        ('Introduction', ['How This Volume Builds on Volume I']),
        ('Part I — Structure & Levels', [
            'Module 1 — Understanding Market Structure (12 lessons)',
            'Module 2 — Support & Resistance (8 lessons)',
        ]),
        ('Part II — Psychology & Confirmation', [
            'Module 3 — Candlestick Psychology (14 patterns revisited)',
            'Module 4 — Candlestick Confirmation (6 lessons)',
        ]),
        ('Part III — Advanced Patterns & Reliability', [
            'Module 5 — 12 Advanced Candlestick Patterns',
            'Module 6 — Candlestick Pattern Reliability',
            'Module 7 — Candlestick Pattern Combinations',
            'Module 8 — Fake Candlestick Signals (8 lessons)',
        ]),
        ('Part IV — Execution & Mastery', [
            'Module 9 — Candlesticks on Different Timeframes',
            'Module 10 — The OneWay FX Candlestick Strategy',
            'Module 11 — Trade Case Studies (12 illustrative examples)',
            'Module 12 — Candlestick Trading Rules',
        ]),
        ('Reference', [
            'Glossary of Terms (75 intermediate concepts)',
            'Closing Note from OneWay FX',
        ]),
    ]
    for part_title, entries in toc_parts:
        rows = [[Paragraph(e, styles['TOCEntry'])] for e in entries]
        t = Table(rows, colWidths=[468])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -2), 0.4, PANEL_LINE),
            ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(KeepTogether([Paragraph(part_title, styles['TOCPart']), t]))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ---------------- Introduction ----------------
    story.extend(chapter_block('Introduction', 'How This Volume Builds on Volume I'))
    story.append(Paragraph(
        "Volume I taught you to read a single candle and recognize the patterns "
        "candles form. That's the vocabulary. This volume teaches the grammar — "
        "how to combine that vocabulary with market context, structure, and "
        "probability so it actually says something useful about what to do next.",
        styles['Body']))
    story.append(Paragraph(
        "Twelve modules make up this book. The first two give you the map — "
        "market structure and support/resistance — that every pattern needs in "
        "order to mean anything. The middle modules deepen your understanding of "
        "candlesticks themselves: the psychology behind them, how to confirm "
        "them, twelve advanced patterns beyond Volume I's fourteen, and an "
        "honest look at which patterns actually deserve your trust. The final "
        "modules turn all of it into something usable — a strategy checklist, "
        "illustrative case studies, and a short list of rules you can actually "
        "remember under pressure.", styles['Body']))
    story.append(Paragraph(
        "Read this volume in order. Each module assumes you've absorbed the "
        "ones before it, and the later modules reference earlier ones by name.",
        styles['Body']))
    story.append(PageBreak())

    # ================= MODULE 1 =================
    story.extend(module_opener(1, 'Understanding Market Structure', MODULE1_INTRO))
    for t in MODULE1_TOPICS:
        story.append(render_topic(**t))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ================= MODULE 2 =================
    story.extend(module_opener(2, 'Support & Resistance', MODULE2_INTRO))
    for t in MODULE2_TOPICS:
        story.append(render_topic(**t))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ================= MODULE 3 =================
    story.extend(module_opener(3, 'Candlestick Psychology', MODULE3_INTRO))
    for p in MODULE3_PATTERNS:
        story.append(psychology_card(**p))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ================= MODULE 4 =================
    story.extend(module_opener(4, 'Candlestick Confirmation', MODULE4_INTRO))
    story.append(render_topic(**MODULE4_TOPICS[0]))
    story.append(Spacer(1, 6))
    story.append(KeepTogether(MODULE4_CONFIRM_DRAWING))
    story.append(Spacer(1, 8))
    for t in MODULE4_TOPICS[1:]:
        story.append(render_topic(**t))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ================= MODULE 5 =================
    story.extend(module_opener(5, '12 Advanced Candlestick Patterns', MODULE5_INTRO))
    story.append(PageBreak())
    for idx, p in enumerate(MODULE5_PATTERNS):
        for flow in module5_pattern_block(idx, p):
            story.append(flow)
        story.append(PageBreak())

    # ================= MODULE 6 =================
    story.extend(module_opener(6, 'Candlestick Pattern Reliability', MODULE6_INTRO))
    for tier in MODULE6_TIERS:
        story.append(reliability_tier(tier['stars'], tier['title'], tier['why'], tier['names']))
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ================= MODULE 7 =================
    story.extend(module_opener(7, 'Candlestick Pattern Combinations', MODULE7_INTRO))
    for combo in MODULE7_COMBOS:
        story.append(combo_card(combo['parts'], combo['result'], combo['result_color'], combo['explanation']))
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ================= MODULE 8 =================
    story.extend(module_opener(8, 'Fake Candlestick Signals', MODULE8_INTRO))
    for t in MODULE8_TOPICS:
        story.append(render_topic(**t))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ================= MODULE 9 =================
    story.extend(module_opener(9, 'Candlesticks on Different Timeframes', MODULE9_INTRO))
    story.append(timeframe_table(MODULE9_TIMEFRAMES))
    story.append(Spacer(1, 14))
    story.append(KeepTogether(MODULE9_HTF_DRAWING))
    story.append(PageBreak())

    # ================= MODULE 10 =================
    story.extend(module_opener(10, 'The OneWay FX Candlestick Strategy', MODULE10_INTRO))
    for head, body in MODULE10_CHECKLIST:
        story.append(KeepTogether([Paragraph(head, styles['SubHeading']),
                                    Paragraph(body, styles['Body'])]))
    story.append(Spacer(1, 8))
    story.append(KeepTogether([
        Paragraph('Putting It Together', styles['SectionHeading']),
        Paragraph(
            "Here's what the checklist looks like on an actual setup: a Hammer "
            "forms inside a support zone. The entry sits just above the Hammer's "
            "close, the stop sits just below the zone, and the target sits at "
            "the next meaningful resistance level — every number decided before "
            "the trade, not during it.", styles['Body']),
        Spacer(1, 6), MODULE10_EXAMPLE_DRAWING,
        Paragraph('Figure — Entry, Stop Loss, and Take Profit, all defined before the trade.',
                  styles['Caption']),
    ]))
    story.append(PageBreak())

    # ================= MODULE 11 =================
    story.extend(module_opener(11, 'Trade Case Studies', MODULE11_INTRO))
    for case in MODULE11_CASES:
        story.append(case_study(**case))
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # ================= MODULE 12 =================
    story.extend(module_opener(12, 'Candlestick Trading Rules', MODULE12_INTRO))
    for i, (rule, why) in enumerate(MODULE12_RULES):
        story.append(rule_item(i + 1, rule, why))
    story.append(PageBreak())

    # ---------------- Glossary ----------------
    story.append(Paragraph('REFERENCE', styles['ChapterKicker']))
    story.append(Paragraph('Glossary of Terms', styles['ChapterTitle']))
    story.append(gold_rule())
    story.append(Paragraph(
        "Seventy-five intermediate and advanced terms used across this volume, "
        "many drawn from modern market-structure and smart-money-concept "
        "vocabulary. If a term from Modules 1, 2, or 9 sent you looking for a "
        "definition, it's here.", styles['Body']))
    story.append(Spacer(1, 4))
    navy_hex = _hex(NAVY)
    for term, definition in GLOSSARY2:
        story.append(Paragraph(f'<b><font color="{navy_hex}">{term}</font></b> — {definition}',
                                styles['GlossaryEntry']))
    story.append(PageBreak())

    # ---------------- Closing ----------------
    story.append(Paragraph('CLOSING NOTE', styles['ChapterKicker']))
    story.append(Paragraph('From the OneWay FX Team', styles['ChapterTitle']))
    story.append(gold_rule())
    story.append(Paragraph(
        "You now have both halves of the picture: Volume I's fourteen candlestick "
        "patterns and the deeper toolkit in this book — structure, levels, "
        "psychology, confirmation, twelve more patterns, reliability, "
        "combinations, fakes, timeframes, a repeatable strategy, and a set of "
        "rules to hold yourself to. None of it replaces the other; a candlestick "
        "pattern is still the trigger, and everything in this volume is what "
        "tells you whether that trigger is worth pulling.", styles['Body']))
    story.append(Paragraph(
        "Trade what you can prove on the chart, size every position like the "
        "next ten trades matter more than this one, and let the process — not "
        "any single trade — be the thing you're proud of.", styles['Body']))
    story.append(Spacer(1, 16))
    story.append(Paragraph('OneWay FX', ParagraphStyle('sig2', fontName='Helvetica-Bold', fontSize=13, textColor=NAVY)))
    story.append(Paragraph('onewayfxsupport@gmail.com', styles['Caption']))

    doc.build(story)


if __name__ == '__main__':
    build()
    print('done')
