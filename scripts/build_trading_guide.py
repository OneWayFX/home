#!/usr/bin/env python3
"""Generate the OneWay FX HFX / Binary Options & Candlestick Trading Guide PDF."""

import math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    NextPageTemplate, PageBreak, KeepTogether, FrameBreak, Flowable, ListFlowable, ListItem
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from reportlab.pdfgen import canvas as pdfcanvas

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
NAVY = HexColor('#0B2545')
NAVY_DARK = HexColor('#071A33')
GOLD = HexColor('#C9962B')
GOLD_LIGHT = HexColor('#E7C878')
BULL_GREEN = HexColor('#26A69A')
BEAR_RED = HexColor('#EF5350')
BULL_STROKE = HexColor('#0F7A6B')
BEAR_STROKE = HexColor('#B33330')
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

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

OUT_PATH = "OneWayFX_HFX_Binary_Options_Candlestick_Guide.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='CoverTitle', fontName='Helvetica-Bold', fontSize=30, leading=36,
    textColor=colors.white, alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='CoverSubtitle', fontName='Helvetica', fontSize=15, leading=20,
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
    name='ChapterTitle', fontName='Helvetica-Bold', fontSize=23, leading=28,
    textColor=NAVY, alignment=TA_LEFT, spaceAfter=14, spaceBefore=0,
))
styles.add(ParagraphStyle(
    name='SectionHeading', fontName='Helvetica-Bold', fontSize=15, leading=19,
    textColor=NAVY, spaceBefore=16, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name='PatternTitle', fontName='Helvetica-Bold', fontSize=16.5, leading=20,
    textColor=colors.white, spaceBefore=0, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name='PatternSub', fontName='Helvetica-Oblique', fontSize=10, leading=13,
    textColor=HexColor('#DCE6F2'), spaceBefore=1,
))
styles.add(ParagraphStyle(
    name='SubHeading', fontName='Helvetica-Bold', fontSize=11.5, leading=15,
    textColor=NAVY, spaceBefore=10, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name='Body', fontName='Helvetica', fontSize=10.3, leading=15,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name='BodyCover', fontName='Helvetica', fontSize=10.3, leading=15.5,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name='BulletItem', fontName='Helvetica', fontSize=10.3, leading=14.5,
    textColor=INK, alignment=TA_LEFT, spaceAfter=3, leftIndent=14,
))
styles.add(ParagraphStyle(
    name='Caption', fontName='Helvetica-Oblique', fontSize=9, leading=12,
    textColor=SUBTLE, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name='WarnHead', fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=HexColor('#8A4B14'),
))
styles.add(ParagraphStyle(
    name='WarnBody', fontName='Helvetica', fontSize=9.7, leading=14,
    textColor=HexColor('#5C3A16'), alignment=TA_JUSTIFY,
))
styles.add(ParagraphStyle(
    name='TOCEntry', fontName='Helvetica', fontSize=11, leading=20,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name='TOCPart', fontName='Helvetica-Bold', fontSize=11.5, leading=24,
    textColor=NAVY, spaceBefore=8,
))
styles.add(ParagraphStyle(
    name='GlanceLabel', fontName='Helvetica-Bold', fontSize=8.6, leading=11,
    textColor=SUBTLE,
))
styles.add(ParagraphStyle(
    name='GlanceValue', fontName='Helvetica-Bold', fontSize=10.3, leading=13,
    textColor=NAVY,
))

# ---------------------------------------------------------------------------
# Candlestick drawing engine
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
    # wick as a hairline through the full body width so it reads as one
    # continuous shadow behind the body, the way real candles render
    d.add(Line(cx, Y(lo), cx, Y(hi), strokeColor=stroke, strokeWidth=wick_w))
    body_h = max(Y(top) - Y(bottom), 1.4)
    body_w = w * 0.62 if not muted else w
    d.add(Rect(cx - body_w / 2.0, Y(bottom), body_w, body_h, fillColor=fill_color,
                strokeColor=stroke, strokeWidth=sw))


def _arrow(d, x0, y0, x1, y1, color, dashed=True):
    d.add(Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=1.8,
               strokeDashArray=[3, 2.4] if dashed else None))
    ang = math.atan2(y1 - y0, x1 - x0)
    size = 6.5
    a = 0.42
    p2 = (x1 - size * math.cos(ang - a), y1 - size * math.sin(ang - a))
    p3 = (x1 - size * math.cos(ang + a), y1 - size * math.sin(ang + a))
    d.add(Polygon(points=[x1, y1, p2[0], p2[1], p3[0], p3[1]],
                  fillColor=color, strokeColor=color))


def _label(d, x, y, text, size=7.6, color=SUBTLE, bold=False, anchor='middle'):
    d.add(String(x, y, text, fontSize=size, fillColor=color,
                 fontName='Helvetica-Bold' if bold else 'Helvetica',
                 textAnchor=anchor))


BEAR_DARK_RED = HexColor('#8B1E1E')

BIAS_STYLE = {
    'bullish': (BULL_GREEN, 'Bullish Reversal'),
    'bearish': (BEAR_DARK_RED, 'Bearish Reversal'),
    'neutral': (HexColor('#8A93A3'), 'Indecision'),
}


def _ghost_candle(d, cx, o, c, hi, lo, w, y0, yscale, color):
    """A dashed, unfilled 'projected' candle representing an expected future bar."""
    def Y(v):
        return y0 + v * yscale
    top, bottom = max(o, c), min(o, c)
    d.add(Line(cx, Y(lo), cx, Y(hi), strokeColor=color, strokeWidth=1.0,
               strokeDashArray=[2, 2]))
    body_h = max(Y(top) - Y(bottom), 1.4)
    body_w = w * 0.62
    d.add(Rect(cx - body_w / 2.0, Y(bottom), body_w, body_h, fillColor=color,
               fillOpacity=0.10, strokeColor=color, strokeWidth=1.0,
               strokeDashArray=[2, 2]))


def pattern_drawing(context, pattern, bias, trend_label, bias_label=None,
                     width=468, height=192):
    """Build a Drawing showing: a multi-candle prior-trend, the pattern boxed
    in a highlight frame, and dashed 'projected' candles + an arrow showing
    the expected trend once the pattern is identified."""
    d = Drawing(width, height)
    y0 = 34
    yscale = 1.1

    def Y(v):
        return y0 + v * yscale

    # bordered figure panel, like a boxed diagram in a printed textbook
    d.add(Rect(1, 4, width - 2, height - 8, fillColor=CHART_BG,
               strokeColor=CHART_BORDER, strokeWidth=0.9))
    # faint price gridlines behind the candles
    for lvl in (20, 40, 60, 80):
        gy = Y(lvl)
        d.add(Line(9, gy, width - 9, gy, strokeColor=CHART_GRID, strokeWidth=0.6,
                   strokeDashArray=[2, 2.5]))
    # baseline
    d.add(Line(8, 22, width - 8, 22, strokeColor=PANEL_LINE, strokeWidth=0.75))

    label_row = height - 12

    # --- prior trend: a longer run of context candles ---
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

    # dashed divider between the trend context and the highlighted pattern
    divider_x = ctx_last_x + cctx_w / 2.0 + 9
    d.add(Line(divider_x, 12, divider_x, height - 18, strokeColor=GOLD_LIGHT,
               strokeWidth=0.8, strokeDashArray=[2, 2.5]))

    # --- the pattern itself, boxed to call it out clearly ---
    x = divider_x + 17
    cw = 28 if len(pattern) == 1 else (22 if len(pattern) == 2 else 18)
    gap = 28 if len(pattern) == 2 else 22
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

    # --- projected candles: what price is expected to do next ---
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


# ---------------------------------------------------------------------------
# Trend context generators
# ---------------------------------------------------------------------------

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


def choppy_context(n=7):
    out = []
    lvl = 40
    up = True
    for i in range(n):
        delta = 6 if up else -5
        o = lvl
        c = lvl + delta
        hi = max(o, c) + 3
        lo = min(o, c) - 3
        out.append((o, c, hi, lo))
        lvl = c
        up = not up
    return out


# ---------------------------------------------------------------------------
# Pattern content
# ---------------------------------------------------------------------------

PATTERNS = [
    dict(
        key='doji', name='Doji',
        tagline='The market pauses to catch its breath',
        bias='neutral', reliability='Low alone / High with context',
        best_seen='After a strong trend, at support or resistance',
        context=choppy_context(),
        pattern=[(50, 51, 76, 25)],
        trend_label='Sideways / trending', bias_label='Indecision',
        looks_like="A Doji forms when a candle's open and close are virtually equal, "
                   "leaving little to no real body — just a thin horizontal line with "
                   "wicks extending above and/or below it. Visually it looks like a "
                   "plus sign or cross sitting on the price chart.",
        psychology="A Doji means the market hasn't decided which direction it wants to "
                   "go — buyers and sellers fought to a draw, with neither side holding "
                   "control into the close. On its own that's just hesitation, but when "
                   "a Doji appears within an established uptrend or downtrend, it's a "
                   "strong signal that the trend is losing steam and the market is "
                   "likely about to reverse.",
        usage="On its own, a Doji is not a trade signal — it's a warning light. "
              "HFX / binary options traders watch the next 1-2 candles closely: a "
              "strong candle breaking away from the Doji confirms which side won and "
              "can be used as an entry trigger for a short-expiry position.",
        caution="Doji candles are extremely common in choppy, low-volatility markets "
                "and mean very little there. Only give weight to a Doji that appears "
                "after a clear, extended trend or at an obvious support/resistance level.",
    ),
    dict(
        key='dragonfly_doji', name='Dragonfly Doji',
        tagline='Sellers tried to take control — and failed',
        bias='bullish', reliability='Medium-High at support',
        best_seen='End of a downtrend, at a support level',
        context=downtrend_context(end_level=70),
        pattern=[(70, 71, 73, 20)],
        trend_label='Downtrend',
        looks_like="A Dragonfly Doji has its open and close near the top of the "
                   "candle's range, a long lower wick, and little to no upper wick. "
                   "The shape resembles a capital letter 'T' or an insect's long "
                   "tail hanging below a flat body.",
        psychology="Price opened, sellers drove it sharply lower during the session, "
                   "but buyers stepped in with enough force to push it all the way "
                   "back up to the open by the close. That long lower wick is a "
                   "rejection of lower prices — a strong signal that demand is "
                   "returning.",
        usage="When a Dragonfly Doji forms after a decline and lands on a known "
              "support level, it is one of the more reliable single-candle bullish "
              "reversal signals. Traders often look for the next candle to confirm "
              "with a higher close before positioning for an upward move.",
        caution="A Dragonfly Doji found in the middle of a range or an uptrend carries "
                "far less meaning. Context — where the candle appears — matters more "
                "than the candle shape itself.",
    ),
    dict(
        key='gravestone_doji', name='Gravestone Doji',
        tagline='Buyers pushed higher — then lost the room',
        bias='bearish', reliability='Medium-High at resistance',
        best_seen='End of an uptrend, at a resistance level',
        context=uptrend_context(end_level=30),
        pattern=[(30, 29, 80, 28)],
        trend_label='Uptrend',
        looks_like="The mirror image of the Dragonfly: open and close sit near the "
                   "bottom of the range, with a long upper wick and virtually no "
                   "lower wick. It looks like an upside-down 'T', or a gravestone "
                   "marker sitting on the chart.",
        psychology="Buyers pushed price sharply higher during the session, but "
                   "sellers overwhelmed them and dragged price back down to near "
                   "the open by the close. That long upper wick shows rejection of "
                   "higher prices — momentum is fading right where buyers needed it "
                   "most.",
        usage="A Gravestone Doji forming after an uptrend, especially at resistance, "
              "warns that the rally may be running out of steam. Traders watch for a "
              "bearish follow-through candle before treating it as a signal to fade "
              "the move.",
        caution="Like all Doji variants, this pattern is noise without context. Always "
                "confirm it sits at the top of a genuine move, not in a flat, "
                "directionless market.",
    ),
    dict(
        key='hammer', name='Hammer',
        tagline='A sharp sell-off gets swallowed by buyers',
        bias='bullish', reliability='Medium-High with confirmation',
        best_seen='After a downtrend',
        context=downtrend_context(end_level=52),
        pattern=[(52, 60, 62, 15)],
        trend_label='Downtrend',
        looks_like="A small real body sitting near the top of the candle's range, "
                   "with a lower wick at least twice the length of the body and "
                   "little to no upper wick. It resembles a hammer with the handle "
                   "pointing down.",
        psychology="Sellers pushed price well below the open during the session, but "
                   "buyers absorbed that pressure and drove price back up near the "
                   "open (or higher) by the close. It shows a decisive intraday "
                   "rejection of lower prices after a decline.",
        usage="You'll typically spot a Hammer sitting at the bottom of a downtrend, "
              "right where selling pressure is running out of steam — that location "
              "is what gives the pattern its meaning. Hammers are one of the "
              "most-watched reversal signals in short-term trading; HFX / binary "
              "options traders typically wait for the next candle to close above "
              "the hammer's body before entering a bullish position, using the "
              "hammer's low as an invalidation reference point.",
        caution="A hammer with no prior downtrend is just a small candle with a long "
                "wick — it has no reversal meaning. The body color (green or red) is "
                "secondary to the shape and location.",
    ),
    dict(
        key='hanging_man', name='Hanging Man',
        tagline='The same shape as a Hammer — a very different message',
        bias='bearish', reliability='Medium, needs confirmation',
        best_seen='After an uptrend',
        context=uptrend_context(end_level=58),
        pattern=[(58, 52, 60, 15)],
        trend_label='Uptrend',
        looks_like="Identical in shape to the Hammer — small body near the top of "
                   "the range with a long lower wick — but it appears after a rally "
                   "instead of a decline.",
        psychology="During the session, sellers managed to push price sharply below "
                   "the open even though the broader trend has been up. Buyers "
                   "recovered price by the close, but the fact that sellers could "
                   "generate that much downside pressure at all is an early warning "
                   "that demand may be drying up.",
        usage="Because it looks exactly like a bullish Hammer, the Hanging Man is "
              "identified purely by its position after an uptrend. Traders wait for "
              "a bearish confirmation candle — a close below the Hanging Man's body "
              "— before acting on it.",
        caution="Never trade a Hanging Man in isolation; it is a caution flag, not a "
                "trigger. Many false signals occur when traders skip the confirmation "
                "step.",
    ),
    dict(
        key='shooting_star', name='Shooting Star',
        tagline='A rally that reaches too far, too fast',
        bias='bearish', reliability='Medium-High with confirmation',
        best_seen='After an uptrend',
        context=uptrend_context(end_level=45),
        pattern=[(45, 40, 85, 38)],
        trend_label='Uptrend',
        looks_like="A small real body near the bottom of the range, with a long "
                   "upper wick at least twice the body's length and little to no "
                   "lower wick — the upside-down mirror of the Hammer.",
        psychology="Buyers pushed price sharply higher intraday, but sellers took "
                   "control and drove it back down near the open by the close. It "
                   "signals that upward momentum was firmly rejected at the highs.",
        usage="You'll typically spot a Shooting Star sitting at the top of a bullish "
              "rally, right where buying pressure is running out of steam — that "
              "location is what gives the pattern its meaning. It's a classic "
              "short-term exhaustion signal; traders look for the next candle to "
              "close below the star's body to confirm sellers are in control before "
              "positioning for a move lower.",
        caution="A Shooting Star in a downtrend or sideways market carries little "
                "significance — the pattern only earns its name after an advance.",
    ),
    dict(
        key='bullish_engulfing', name='Bullish Engulfing Bar',
        tagline='A big green candle swallows the prior red one whole',
        bias='bullish', reliability='High',
        best_seen='After a downtrend',
        context=downtrend_context(end_level=55),
        pattern=[(55, 45, 57, 43), (42, 62, 64, 40)],
        trend_label='Downtrend',
        looks_like="A two-candle pattern: a smaller bearish (red) candle followed by "
                   "a larger bullish (green) candle whose body completely engulfs "
                   "the body of the first — opening at or below the prior close and "
                   "closing above the prior open.",
        psychology="Sellers were in control on the first candle, but buyers stepped "
                   "in decisively on the second, not only reversing the loss but "
                   "overpowering the entire prior session's range. It represents a "
                   "clean, forceful shift from seller control to buyer control.",
        usage="This is one of the most trusted two-candle reversal signals in "
              "HFX / binary options trading. Many traders enter a bullish position "
              "as soon as the engulfing candle closes, using the low of the pattern "
              "as their invalidation level.",
        caution="The strength of the signal scales with the size of the engulfing "
                "candle and the volume/momentum behind it. A marginal engulfing "
                "candle in a strong downtrend is weaker evidence than one that "
                "appears at an established support zone.",
    ),
    dict(
        key='bearish_engulfing', name='Bearish Engulfing Bar',
        tagline='A big red candle erases the prior green one entirely',
        bias='bearish', reliability='High',
        best_seen='After an uptrend',
        context=uptrend_context(end_level=45),
        pattern=[(45, 55, 57, 43), (58, 38, 60, 36)],
        trend_label='Uptrend',
        looks_like="A smaller bullish (green) candle followed by a larger bearish "
                   "(red) candle whose body completely engulfs the first — opening "
                   "at or above the prior close and closing below the prior open.",
        psychology="Buyers held control on the first candle, but sellers overwhelmed "
                   "them on the second, erasing the entire gain and then some. It "
                   "marks a forceful handover from buyer control to seller control.",
        usage="Traders treat a confirmed Bearish Engulfing Bar after an uptrend as a "
              "high-confidence signal to position for a move lower, typically as soon "
              "as the engulfing candle closes.",
        caution="Watch for engulfing patterns that occur into a resistance zone — "
                "the combination of pattern and level meaningfully increases "
                "reliability versus the pattern appearing in open air.",
    ),
    dict(
        key='bullish_harami', name='Bullish Harami',
        tagline='A small candle rests quietly inside a big one',
        bias='bullish', reliability='Medium',
        best_seen='After a downtrend',
        context=downtrend_context(end_level=65),
        pattern=[(65, 35, 67, 33), (45, 55, 57, 43)],
        trend_label='Downtrend',
        looks_like="A large bearish (red) candle followed by a small bullish (green) "
                   "candle whose entire body sits inside the range of the first "
                   "candle's body — the opposite of an engulfing pattern. 'Harami' "
                   "is Japanese for 'pregnant', describing the small candle tucked "
                   "inside the large one.",
        psychology="Selling pressure was dominant and forceful on the first candle, "
                   "but the follow-through evaporates on the second — the sharp "
                   "contraction in range signals sellers are losing conviction, "
                   "even though buyers haven't yet taken control.",
        usage="A Bullish Harami is a softer, earlier warning sign than a Bullish "
              "Engulfing Bar. Many traders wait for a third candle to close higher "
              "before entering, using the harami as an early heads-up rather than a "
              "standalone trigger.",
        caution="Because the second candle is small, this pattern is less decisive "
                "than an engulfing bar. Treat it as 'the trend may be pausing', not "
                "'the trend has reversed', until confirmed.",
    ),
    dict(
        key='bearish_harami', name='Bearish Harami',
        tagline='Momentum contracts sharply after a strong advance',
        bias='bearish', reliability='Medium',
        best_seen='After an uptrend',
        context=uptrend_context(end_level=35),
        pattern=[(35, 65, 67, 33), (55, 45, 57, 43)],
        trend_label='Uptrend',
        looks_like="A large bullish (green) candle followed by a small bearish (red) "
                   "candle fully contained inside the first candle's body.",
        psychology="Strong buying pressure suddenly contracts into a small, "
                   "indecisive candle — a sign that the rally's momentum is fading "
                   "even before sellers have fully asserted control.",
        usage="Traders treat this as an early caution sign after a rally. "
              "Confirmation from a lower close on the next candle strengthens the "
              "case for a bearish position.",
        caution="A Bearish Harami deep inside a strong, high-momentum uptrend can "
                "simply be a pause, not a reversal — always wait for confirmation "
                "before acting.",
    ),
    dict(
        key='morning_star', name='Morning Star',
        tagline='Darkness, hesitation, then a decisive dawn',
        bias='bullish', reliability='High',
        best_seen='After a downtrend',
        context=downtrend_context(end_level=70),
        pattern=[(70, 40, 72, 38), (30, 33, 35, 25), (35, 65, 67, 33)],
        trend_label='Downtrend',
        looks_like="A three-candle pattern: a large bearish candle, followed by a "
                   "small-bodied candle (the 'star') that gaps or dips lower and "
                   "shows indecision, followed by a large bullish candle that closes "
                   "well back into the body of the first candle.",
        psychology="Candle one shows sellers firmly in control. Candle two shows "
                   "that control breaking down into indecision. Candle three shows "
                   "buyers seizing control decisively — the three candles together "
                   "tell a complete story of a trend reversal in progress.",
        usage="The Morning Star is regarded as one of the more reliable multi-candle "
              "reversal patterns. Traders typically wait for the third candle to "
              "close before entering a bullish position, since it confirms the "
              "reversal that the star candle only hinted at.",
        caution="The pattern is strongest when the third candle closes above the "
                "midpoint of the first candle's body — a weak third candle produces "
                "a much less reliable signal.",
    ),
    dict(
        key='evening_star', name='Evening Star',
        tagline='A bright rally, a flicker of doubt, then dusk',
        bias='bearish', reliability='High',
        best_seen='After an uptrend',
        context=uptrend_context(end_level=30),
        pattern=[(30, 60, 62, 28), (68, 65, 72, 63), (63, 33, 65, 31)],
        trend_label='Uptrend',
        looks_like="The mirror of the Morning Star: a large bullish candle, followed "
                   "by a small-bodied 'star' candle that gaps or pushes higher and "
                   "shows indecision, followed by a large bearish candle that closes "
                   "well back into the first candle's body.",
        psychology="Buyers are firmly in control on candle one, momentum stalls into "
                   "indecision on candle two, and sellers take decisive control on "
                   "candle three — a full narrative of a top forming in real time.",
        usage="Traders treat a confirmed Evening Star after an extended uptrend as a "
              "strong signal to position for a move lower, entering once the third "
              "candle closes.",
        caution="As with the Morning Star, the depth of the third candle's close "
                "into the first candle's body determines the strength of the "
                "signal — a shallow close is a weaker warning.",
    ),
    dict(
        key='tweezer_tops', name='Tweezer Tops',
        tagline='Two candles slam into the exact same ceiling',
        bias='bearish', reliability='Medium',
        best_seen='After an uptrend, at resistance',
        context=uptrend_context(end_level=40),
        pattern=[(40, 62, 65, 38), (60, 42, 65, 40)],
        trend_label='Uptrend',
        looks_like="Two (or more) consecutive candles with matching, or nearly "
                   "matching, highs — typically a bullish candle followed by a "
                   "bearish candle — forming a visible 'twin peaks' ceiling on the "
                   "chart, like the two prongs of a pair of tweezers.",
        psychology="Price attempted to push to a new high twice in a row and was "
                   "turned back at almost the identical level both times. That "
                   "repeated rejection marks the level as meaningful resistance and "
                   "suggests buying pressure is exhausted there.",
        usage="Traders use Tweezer Tops as confirmation of a resistance level and "
              "often combine it with other bearish signals (such as a Bearish "
              "Engulfing Bar or Doji) at the same level to strengthen the case for a "
              "short-term reversal trade.",
        caution="The matching highs are the entire signal — the bodies and colors "
                "of the two candles matter less. The more precisely the highs align, "
                "the stronger the resistance implication.",
    ),
    dict(
        key='tweezer_bottoms', name='Tweezer Bottoms',
        tagline='Two candles bounce off the exact same floor',
        bias='bullish', reliability='Medium',
        best_seen='After a downtrend, at support',
        context=downtrend_context(end_level=62),
        pattern=[(62, 40, 64, 25), (42, 60, 63, 25)],
        trend_label='Downtrend',
        looks_like="Two (or more) consecutive candles with matching, or nearly "
                   "matching, lows — typically a bearish candle followed by a "
                   "bullish candle — forming a visible 'double floor' on the chart.",
        psychology="Price tested a low twice and found buyers defending the exact "
                   "same level both times. The repeated rejection of lower prices "
                   "marks strong, tested support and suggests sellers are running "
                   "out of conviction.",
        usage="Traders treat Tweezer Bottoms as confirmation of a support level, "
              "often pairing it with a bullish follow-through candle or another "
              "bullish signal at the same level before entering a long position.",
        caution="As with Tweezer Tops, precise alignment of the lows is what gives "
                "the pattern weight — loosely matching lows are a much weaker "
                "signal.",
    ),
]

# ---------------------------------------------------------------------------
# Anatomy-of-a-candle diagram (Chapter on reading a candle)
# ---------------------------------------------------------------------------

def anatomy_drawing(width=468, height=230):
    d = Drawing(width, height)
    y0 = 26
    yscale = 1.7

    def Y(v):
        return y0 + v * yscale

    d.add(Rect(1, 4, width - 2, height - 8, fillColor=CHART_BG,
               strokeColor=CHART_BORDER, strokeWidth=0.9))
    for lvl in (18, 38, 58, 78):
        gy = Y(lvl)
        d.add(Line(9, gy, width - 9, gy, strokeColor=CHART_GRID, strokeWidth=0.6,
                   strokeDashArray=[2, 2.5]))

    # Bullish candle (left)
    bx = 140
    o, c, hi, lo = 28, 68, 78, 18
    _candle(d, bx, o, c, hi, lo, 56, y0, yscale, fill=BULL_GREEN)
    # Bearish candle (right)
    rx = 330
    o2, c2, hi2, lo2 = 68, 28, 78, 18
    _candle(d, rx, o2, c2, hi2, lo2, 56, y0, yscale, fill=BEAR_RED)

    label_col = HexColor('#26364A')
    # Bullish labels
    d.add(Line(bx + 23, Y(78), bx + 90, Y(78), strokeColor=label_col, strokeWidth=0.6))
    _label(d, bx + 92, Y(78) - 3, 'High', size=8.6, color=label_col, anchor='start', bold=True)
    d.add(Line(bx + 23, Y(68), bx + 90, Y(68), strokeColor=label_col, strokeWidth=0.6))
    _label(d, bx + 92, Y(68) - 3, 'Close (up)', size=8.6, color=label_col, anchor='start', bold=True)
    d.add(Line(bx + 23, Y(28), bx - 96, Y(28), strokeColor=label_col, strokeWidth=0.6))
    _label(d, bx - 98, Y(28) - 3, 'Open', size=8.6, color=label_col, anchor='end', bold=True)
    d.add(Line(bx + 23, Y(18), bx - 96, Y(18), strokeColor=label_col, strokeWidth=0.6))
    _label(d, bx - 98, Y(18) - 3, 'Low', size=8.6, color=label_col, anchor='end', bold=True)
    _label(d, bx, Y(48), 'BODY', size=7.6, color=colors.white, bold=True)
    _label(d, bx, height - 14, 'BULLISH CANDLE', size=9, color=BULL_GREEN, bold=True)
    _label(d, bx, height - 26, '(close above open)', size=7.6, color=SUBTLE)

    # Bearish labels
    d.add(Line(rx + 23, Y(78), rx + 90, Y(78), strokeColor=label_col, strokeWidth=0.6))
    _label(d, rx + 92, Y(78) - 3, 'High', size=8.6, color=label_col, anchor='start', bold=True)
    d.add(Line(rx + 23, Y(68), rx + 90, Y(68), strokeColor=label_col, strokeWidth=0.6))
    _label(d, rx + 92, Y(68) - 3, 'Open', size=8.6, color=label_col, anchor='start', bold=True)
    d.add(Line(rx - 23, Y(28), rx - 90, Y(28), strokeColor=label_col, strokeWidth=0.6))
    _label(d, rx - 92, Y(28) - 3, 'Close (down)', size=8.6, color=label_col, anchor='end', bold=True)
    d.add(Line(rx - 23, Y(18), rx - 90, Y(18), strokeColor=label_col, strokeWidth=0.6))
    _label(d, rx - 92, Y(18) - 3, 'Low', size=8.6, color=label_col, anchor='end', bold=True)
    _label(d, rx, height - 14, 'BEARISH CANDLE', size=9, color=BEAR_RED, bold=True)
    _label(d, rx, height - 26, '(close below open)', size=7.6, color=SUBTLE)

    # Wick labels
    _label(d, bx, Y(78) + 10, 'Upper wick', size=7.4, color=SUBTLE)
    _label(d, bx, Y(18) - 10, 'Lower wick', size=7.4, color=SUBTLE)
    _label(d, rx, Y(78) + 10, 'Upper wick', size=7.4, color=SUBTLE)
    _label(d, rx, Y(18) - 10, 'Lower wick', size=7.4, color=SUBTLE)

    return d


# ---------------------------------------------------------------------------
# Small helper flowables / components
# ---------------------------------------------------------------------------

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


def _hex(c):
    return '#%02X%02X%02X' % (round(c.red * 255), round(c.green * 255), round(c.blue * 255))


def glance_table(bias, reliability, best_seen):
    color, bias_word = BIAS_STYLE[bias]
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
    color, _ = None, None
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


def warn_box(title, body_lines):
    inner = [Paragraph(title, styles['WarnHead'])]
    for line in body_lines:
        inner.append(Paragraph(f'•  {line}', styles['WarnBody']))
    t = Table([[inner]], colWidths=[468])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), WARN_BG),
        ('BOX', (0, 0), (-1, -1), 1, WARN_LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


def gold_rule(width=468):
    return HR(width, color=GOLD, thickness=1.4, space_before=2, space_after=10)


# ---------------------------------------------------------------------------
# Doc template with header/footer + TOC support
# ---------------------------------------------------------------------------

TOC_ENTRIES = []


class BookDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'toc_level'):
            text = flowable.getPlainText() if hasattr(flowable, 'getPlainText') else str(flowable)
            self.notify('TOCEntry', (flowable.toc_level, text, self.page))


def cover_page_canvas(c, doc):
    c.saveState()
    c.setFillColor(NAVY_DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H * 0.28, PAGE_W, PAGE_H * 0.72, fill=1, stroke=0)
    # gold accent lines
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(MARGIN, PAGE_H * 0.28, PAGE_W - MARGIN, PAGE_H * 0.28)
    # decorative candle motif near bottom
    import random
    random.seed(7)
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
    c.drawString(MARGIN, PAGE_H - 0.55 * inch, 'ONEWAY FX  |  EDUCATION SERIES')
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.55 * inch, title_text)
    c.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    c.setFont('Helvetica', 8.3)
    c.drawString(MARGIN, 0.46 * inch, 'HFX / Binary Options & Candlestick Guide')
    c.drawRightString(PAGE_W - MARGIN, 0.46 * inch, f'Page {doc.page - 1}')
    c.restoreState()


def onFirstPage(c, doc):
    cover_page_canvas(c, doc)


def onLaterPages(c, doc):
    header_footer(c, doc, 'onewayfx.com')


def build():
    doc = BookDocTemplate(OUT_PATH, pagesize=letter,
                           leftMargin=MARGIN, rightMargin=MARGIN,
                           topMargin=0.95 * inch, bottomMargin=0.85 * inch,
                           title="OneWay FX — HFX / Binary Options & Candlestick Trading Guide",
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

    # ---------------- Cover page ----------------
    cover_story = [
        Spacer(1, PAGE_H * 0.30),
        Paragraph('ONEWAY FX', ParagraphStyle('brand', fontName='Helvetica-Bold', fontSize=15,
                   textColor=GOLD, alignment=TA_CENTER, tracking=3)),
        Spacer(1, 14),
        Paragraph('HFX / Binary Options<br/>&amp; Candlestick Trading Guide', styles['CoverTitle']),
        Spacer(1, 10),
        Paragraph('A Beginner-to-Practitioner Handbook for Reading Candles<br/>and the Patterns That Move Short-Expiry Markets',
                  styles['CoverSubtitle']),
        Spacer(1, PAGE_H * 0.20),
        Paragraph('Education Series &nbsp;•&nbsp; Volume I', styles['CoverFooter']),
        Paragraph('onewayfxsupport@gmail.com', styles['CoverFooter']),
    ]
    story.append(NextPageTemplate('Cover'))
    story.extend(cover_story)
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # ---------------- Risk disclaimer ----------------
    story.append(Paragraph('IMPORTANT NOTICE', styles['ChapterKicker']))
    story.append(Paragraph('Risk Disclosure', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))
    story.append(Paragraph(
        "This guide is published by OneWay FX for educational purposes only. It is "
        "designed to help readers understand candlestick charting concepts that are "
        "widely used across foreign exchange (FX), HFX, and binary options markets. "
        "Nothing in this document is financial advice, a recommendation to trade, or "
        "a guarantee of any trading outcome.", styles['Body']))
    story.append(warn_box('Please read before continuing', [
        "HFX and binary options trading carries a very high level of risk and is not "
        "suitable for every investor. It is possible to lose some, or all, of your "
        "invested capital, and losses can occur quickly given the short time frames "
        "involved.",
        "Candlestick patterns describe historical probabilities of trader behavior — "
        "they do not predict the future with certainty. No pattern, indicator, or "
        "strategy works every time.",
        "Binary options products are restricted or unavailable to retail clients in "
        "a number of jurisdictions. Confirm the products, leverage, and instruments "
        "available to you are permitted where you live before trading.",
        "Never trade with money you cannot afford to lose. Use proper risk and money "
        "management, start with a demo account, and seek independent financial "
        "advice if you are unsure whether trading is right for you.",
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "By continuing to read, you acknowledge that OneWay FX provides this material "
        "“as is” for educational purposes and accepts no liability for trading "
        "decisions made using this information.", styles['Caption']))
    story.append(PageBreak())

    # ---------------- Table of contents ----------------
    story.append(Paragraph('CONTENTS', styles['ChapterKicker']))
    story.append(Paragraph('Table of Contents', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))

    toc_parts = [
        ('Part I — Foundations', [
            'Chapter 1.  Welcome to OneWay FX',
            'Chapter 2.  What Is HFX / Binary Options Trading?',
            'Chapter 3.  Anatomy of a Candle',
            'Chapter 4.  How to Read a Candle',
        ]),
        ('Part II — The Candlestick Pattern Library', [
            f'4.{i+1}.  {p["name"]}' for i, p in enumerate(PATTERNS)
        ]),
        ('Part III — Applying What You’ve Learned', [
            'Chapter 5.  Putting Patterns to Work in HFX / Binary Options',
            'Chapter 6.  Risk & Money Management',
            'Closing Note from OneWay FX',
        ]),
    ]
    for part_title, entries in toc_parts:
        rows = []
        for e in entries:
            rows.append([Paragraph(e, styles['TOCEntry'])])
        t = Table(rows, colWidths=[468])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -2), 0.4, PANEL_LINE),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(KeepTogether([Paragraph(part_title, styles['TOCPart']), t]))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ---------------- Chapter 1 ----------------
    story.append(Paragraph('CHAPTER 1', styles['ChapterKicker']))
    story.append(Paragraph('Welcome to OneWay FX', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))
    story.append(Paragraph(
        "Welcome, and thank you for picking up the OneWay FX Trading Guide. Whether "
        "you are completely new to the markets or already have some experience and "
        "want to sharpen your chart-reading skills, this book was written to give you "
        "a clear, practical foundation in one of the most widely used tools in "
        "short-term trading: the candlestick chart.", styles['Body']))
    story.append(Paragraph(
        "OneWay FX exists to help traders make sense of fast-moving markets. Candles "
        "and the patterns they form are the visual language that traders around the "
        "world use to read crowd psychology — the ongoing tug-of-war between buyers "
        "and sellers — in real time. Learning to read that language well is one of "
        "the most valuable skills you can build as a trader, in HFX, binary options, "
        "or any other market you go on to trade.", styles['Body']))
    story.append(Paragraph('What this guide covers', styles['SectionHeading']))
    for line in [
        "What HFX and binary options trading actually are, and how they differ from "
        "traditional spot trading.",
        "How a single candle is built, and what its shape tells you about the battle "
        "between buyers and sellers.",
        "A complete, illustrated library of the fourteen candlestick patterns every "
        "trader should recognize on sight.",
        "How to combine candle signals with sound risk management before you ever "
        "place a trade.",
    ]:
        story.append(Paragraph(f'•  {line}', styles['BulletItem']))
    story.append(Paragraph(
        "Read this guide alongside a live or demo chart. Candlestick reading is a "
        "visual, pattern-recognition skill — it sticks best when you see it in "
        "motion, not just on the page.", styles['Body']))
    story.append(PageBreak())

    # ---------------- Chapter 2 ----------------
    story.append(Paragraph('CHAPTER 2', styles['ChapterKicker']))
    story.append(Paragraph('What Is HFX / Binary Options Trading?', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))
    story.append(Paragraph(
        "HFX refers to high-frequency, short-expiry FX trading — taking positions on "
        "the direction of a currency pair (or other instrument) over a compressed "
        "time frame, from as little as sixty seconds up to a few hours. Binary "
        "options are a specific way of structuring that short-term view: instead of "
        "buying or selling the instrument itself, you are predicting whether its "
        "price will be above or below a set level (the strike) at a set expiry time.",
        styles['Body']))
    story.append(Paragraph('The core mechanics', styles['SectionHeading']))
    for line in [
        "<b>Direction, not magnitude.</b> With a binary option, you only need to be "
        "right about direction — up or down — not by how much. The payout is fixed "
        "in advance and does not scale with how far price moves.",
        "<b>Fixed risk, fixed reward.</b> Before you enter, you know exactly what you "
        "stand to gain if you're right and exactly what you stand to lose if you're "
        "wrong — there is no margin call or open-ended loss on the position itself.",
        "<b>Defined expiry.</b> Every position has a set expiry time. When it "
        "arrives, the trade settles automatically based on where price is relative "
        "to the strike.",
        "<b>Compressed decision-making.</b> Because expiries can be short, HFX / "
        "binary options trading rewards traders who can read price action quickly "
        "and decisively — which is exactly where candlestick analysis earns its "
        "keep.",
    ]:
        story.append(Paragraph(f'•  {line}', styles['BulletItem']))
    story.append(Paragraph('Why candles matter so much here', styles['SectionHeading']))
    story.append(Paragraph(
        "Because HFX and binary options trades are decided on direction within a "
        "fixed window, the most useful information you have is what price is doing "
        "<i>right now</i> and what it has just finished doing. Candlestick charts "
        "compress that information into an immediately readable shape — a single "
        "candle can show you who won the last round of the fight between buyers and "
        "sellers, and a sequence of candles can show you whether that fight is about "
        "to change hands. The rest of this guide teaches you to read that shape "
        "fluently.", styles['Body']))
    story.append(PageBreak())

    # ---------------- Chapter 3: Anatomy ----------------
    story.append(Paragraph('CHAPTER 3', styles['ChapterKicker']))
    story.append(Paragraph('Anatomy of a Candle', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=10))
    story.append(Paragraph(
        "Every candlestick, on any time frame, is built from exactly four data "
        "points: the <b>open</b>, <b>high</b>, <b>low</b>, and <b>close</b> of that "
        "period (often shortened to OHLC). Those four numbers are all it takes to "
        "draw the candle.", styles['Body']))
    story.append(Spacer(1, 4))
    story.append(anatomy_drawing())
    story.append(Paragraph('The open, high, low, and close define the body and wicks of every candle.', styles['Caption']))
    story.append(Paragraph('The three parts of every candle', styles['SectionHeading']))
    for line in [
        "<b>The body</b> — the thick rectangle between the open and close. A "
        "<font color='#178A5B'><b>green (bullish)</b></font> body means the close "
        "was higher than the open — buyers won that period. A "
        "<font color='#C0392B'><b>red (bearish)</b></font> body means the close was "
        "lower than the open — sellers won.",
        "<b>The upper wick (or shadow)</b> — the thin line above the body, marking "
        "the highest price reached during the period that the close did not hold.",
        "<b>The lower wick (or shadow)</b> — the thin line below the body, marking "
        "the lowest price reached during the period that the close did not hold.",
    ]:
        story.append(Paragraph(f'•  {line}', styles['BulletItem']))
    story.append(Paragraph(
        "A long body means one side dominated the entire period. A long wick means "
        "price traveled a long way in one direction and was then pushed back — a "
        "sign of rejection. Short wicks with a large body show conviction; long "
        "wicks with a small body show a fight that ended in a draw. Every pattern "
        "in this guide is built from combinations of these simple ideas.", styles['Body']))
    story.append(PageBreak())

    # ---------------- Chapter 4: How to read ----------------
    story.append(Paragraph('CHAPTER 4', styles['ChapterKicker']))
    story.append(Paragraph('How to Read a Candle', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=10))
    story.append(Paragraph(
        "Reading a candle well means asking the same short checklist every time you "
        "look at one. With practice, this becomes instant — but it's worth "
        "practicing deliberately at first.", styles['Body']))
    checklist = [
        ("1. Who won?", "Is the body green (buyers closed higher than they opened) "
         "or red (sellers closed lower than they opened)?"),
        ("2. How strong was the move?", "Compare the size of the body to the candles "
         "around it. A big body means one side pushed hard and won clearly. A small "
         "body means buyers and sellers were evenly matched, and neither side gained "
         "much ground."),
        ("3. Were there rejections?", "Long wicks show price was pushed to an "
         "extreme and then rejected — the longer the wick relative to the body, the "
         "stronger the rejection."),
        ("4. Where did it happen?", "The exact same candle shape means very "
         "different things depending on whether it appears after a long trend, at a "
         "known support/resistance level, or in the middle of a quiet range. Location "
         "is often more important than shape."),
        ("5. What came before and after?", "Almost no single candle should be traded "
         "in isolation. Look at the two or three candles before it for context, and "
         "wait for the next candle to confirm what the signal candle suggested."),
    ]
    for head, body in checklist:
        story.append(Paragraph(head, styles['SubHeading']))
        story.append(Paragraph(body, styles['Body']))
    story.append(Paragraph(
        "Keep this checklist in mind through Part II of this guide — every pattern "
        "below is really just a specific, named answer to these five questions.",
        styles['Caption']))
    story.append(PageBreak())

    # ---------------- Part II intro ----------------
    story.append(Paragraph('PART II', styles['ChapterKicker']))
    story.append(Paragraph('The Candlestick Pattern Library', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))
    story.append(Paragraph(
        "This section illustrates and explains fourteen of the most widely used "
        "candlestick patterns, organized roughly from single-candle patterns to "
        "multi-candle patterns. Each entry follows the same format: an at-a-glance "
        "summary, an illustration showing the pattern in context, what the pattern "
        "looks like, the psychology behind it, how OneWay FX traders typically use "
        "it, and a caution to keep in mind.", styles['Body']))
    story.append(Paragraph(
        "In every illustration, the faded gray candles on the left show the prior "
        "trend leading into the setup, the bold colored candles in the middle are "
        "the pattern itself, and the dashed gold arrow shows the directional bias "
        "the pattern implies.", styles['Body']))
    story.append(PageBreak())

    # ---------------- Pattern sections ----------------
    for idx, p in enumerate(PATTERNS):
        block = []
        block.append(Paragraph(f'PATTERN {idx + 1} OF {len(PATTERNS)}', styles['ChapterKicker']))
        block.append(pattern_header_table(p['name'], p['tagline']))
        block.append(Spacer(1, 10))
        block.append(glance_table(p['bias'], p['reliability'], p['best_seen']))
        story.append(KeepTogether(block))

        story.append(Spacer(1, 10))
        drawing = pattern_drawing(p['context'], p['pattern'], p['bias'], p['trend_label'])
        story.append(KeepTogether([drawing,
                     Paragraph(f'Figure — {p["name"]}: prior trend, the pattern, and its implied bias.', styles['Caption'])]))

        story.append(KeepTogether([Paragraph('What it looks like', styles['SubHeading']),
                     Paragraph(p['looks_like'], styles['Body'])]))
        story.append(KeepTogether([Paragraph('The psychology behind it', styles['SubHeading']),
                     Paragraph(p['psychology'], styles['Body'])]))
        story.append(KeepTogether([Paragraph('How OneWay FX traders use it', styles['SubHeading']),
                     Paragraph(p['usage'], styles['Body'])]))
        story.append(KeepTogether([Paragraph('Caution', styles['SubHeading']),
                     Paragraph(p['caution'], styles['Body'])]))
        story.append(PageBreak())

    # ---------------- Chapter 5 ----------------
    story.append(Paragraph('CHAPTER 5', styles['ChapterKicker']))
    story.append(Paragraph('Putting Patterns to Work in HFX / Binary Options', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=10))
    story.append(Paragraph(
        "Recognizing a pattern is only step one. Turning that recognition into a "
        "disciplined trade decision is what separates consistent traders from "
        "everyone else. Here is a simple framework to apply every pattern in this "
        "guide.", styles['Body']))
    steps = [
        ("Step 1 — Establish context", "Identify the prevailing trend and any "
         "nearby support or resistance levels before you look for a pattern. The "
         "same candle shape means little in the wrong context and a great deal in "
         "the right one."),
        ("Step 2 — Spot the pattern", "Look for one of the fourteen patterns in "
         "this guide forming at a meaningful location — the end of a trend, or at a "
         "tested support/resistance level."),
        ("Step 3 — Wait for confirmation", "Where noted, wait for the next candle "
         "to close in the direction the pattern implies. Confirmation costs you a "
         "small amount of timing but meaningfully improves reliability."),
        ("Step 4 — Check for confluence", "A pattern that lines up with a support/"
         "resistance level, a trendline, or another indicator is a stronger signal "
         "than a pattern appearing on its own."),
        ("Step 5 — Size the trade and set your risk", "Decide your position size "
         "and expiry before you enter — never after. Know exactly what you are "
         "risking and what your maximum loss on the trade is."),
    ]
    for head, body in steps:
        story.append(Paragraph(head, styles['SubHeading']))
        story.append(Paragraph(body, styles['Body']))
    story.append(PageBreak())

    # ---------------- Chapter 6: risk management ----------------
    story.append(Paragraph('CHAPTER 6', styles['ChapterKicker']))
    story.append(Paragraph('Risk & Money Management', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=10))
    story.append(Paragraph(
        "No pattern in this guide wins every time. Even the highest-reliability "
        "setups — engulfing bars and star patterns — fail regularly. Long-term "
        "success in HFX / binary options trading comes from managing risk "
        "consistently across many trades, not from finding a pattern that never "
        "loses.", styles['Body']))
    for head, body in [
        ("Risk only what you can afford to lose", "Never risk capital you need for "
         "living expenses, debt payments, or emergencies. Trading capital should be "
         "money you could lose entirely without it affecting your life."),
        ("Use small, consistent position sizes", "A common guideline is to risk a "
         "small, fixed percentage of your account on any single trade so that a "
         "losing streak — which will happen — does not meaningfully damage your "
         "capital."),
        ("Practice on a demo account first", "Before trading live, practice "
         "identifying and trading these patterns on a demo account until you can "
         "do so consistently and without hesitation."),
        ("Keep a trading journal", "Record every trade: the pattern, the context, "
         "the outcome, and what you would do differently. Patterns are learned "
         "through repetition and honest review."),
        ("Know the rules where you live", "Binary options products are regulated "
         "differently — and in some cases restricted — across different countries. "
         "Confirm what is permitted in your jurisdiction before trading."),
    ]:
        story.append(Paragraph(head, styles['SubHeading']))
        story.append(Paragraph(body, styles['Body']))
    story.append(PageBreak())

    # ---------------- Closing ----------------
    story.append(Paragraph('CLOSING NOTE', styles['ChapterKicker']))
    story.append(Paragraph('From the OneWay FX Team', styles['ChapterTitle']))
    story.append(HR(468, color=GOLD, thickness=2, space_after=14))
    story.append(Paragraph(
        "Candlestick reading is a skill that compounds. The first few dozen charts "
        "you study will feel effortful; over time, pattern recognition becomes "
        "second nature, and you'll start to see the story a chart is telling at a "
        "glance. Keep this guide as a reference, revisit the pattern library often, "
        "and — above all — pair every pattern you learn with disciplined risk "
        "management.", styles['Body']))
    story.append(Paragraph(
        "Thank you for trusting OneWay FX as part of your trading education. We "
        "wish you clear charts and disciplined decisions.", styles['Body']))
    story.append(Spacer(1, 16))
    story.append(Paragraph('OneWay FX', ParagraphStyle('sig', fontName='Helvetica-Bold', fontSize=13, textColor=NAVY)))
    story.append(Paragraph('onewayfxsupport@gmail.com', styles['Caption']))

    doc.build(story)


if __name__ == '__main__':
    build()
    print('done')
