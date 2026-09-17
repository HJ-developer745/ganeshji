import turtle
import math

# ─────────────────────────────────────────────
#  Setup
# ─────────────────────────────────────────────
screen = turtle.Screen()
screen.title("Ganesh Ji - Turtle Art by HJ Developer")
screen.bgcolor("#1a0a00")
screen.setup(width=900, height=980)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)

# ─────────────────────────────────────────────
#  Helper Functions
# ─────────────────────────────────────────────

def goto(x, y):
    t.penup(); t.goto(x, y); t.pendown()

def filled_circle(x, y, r, color, outline=None, lw=2):
    t.penup(); t.goto(x, y - r); t.pendown()
    t.fillcolor(color)
    t.pencolor(outline if outline else color)
    t.pensize(lw)
    t.begin_fill()
    t.circle(r)
    t.end_fill()

def filled_ellipse(x, y, rx, ry, color, outline=None, lw=2, steps=60):
    """Draw a filled ellipse centered at (x, y)."""
    t.penup()
    pts = [(x + rx * math.cos(2*math.pi*i/steps),
            y + ry * math.sin(2*math.pi*i/steps)) for i in range(steps+1)]
    t.goto(pts[0]); t.pendown()
    t.fillcolor(color)
    t.pencolor(outline if outline else color)
    t.pensize(lw)
    t.begin_fill()
    for px, py in pts[1:]:
        t.goto(px, py)
    t.end_fill()

def polygon(points, fill, outline=None, lw=2):
    t.fillcolor(fill)
    t.pencolor(outline if outline else fill)
    t.pensize(lw)
    t.penup(); t.goto(points[0]); t.pendown()
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    t.end_fill()

def arc_line(cx, cy, r, start_deg, end_deg, color, lw=3, steps=60):
    t.pencolor(color); t.pensize(lw)
    span = end_deg - start_deg
    t.penup()
    for i in range(steps+1):
        a = math.radians(start_deg + span*i/steps)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        if i == 0: t.goto(x,y); t.pendown()
        else: t.goto(x,y)
    t.penup()

def dot(x, y, size, color):
    t.penup(); t.goto(x, y)
    t.dot(size, color)

# ─────────────────────────────────────────────
#  Color palette (from reference image)
# ─────────────────────────────────────────────
SKIN      = "#f5d5a0"   # cream-peach face
SKIN_D    = "#e8b87a"   # darker skin shadow
GOLD      = "#d4a017"   # deep gold
GOLD_L    = "#f5c842"   # bright gold
GOLD_HL   = "#ffe87a"   # highlight gold
MAROON    = "#7a1828"   # dark maroon robes
MAROON_L  = "#a02035"
RED_FLWR  = "#c0392b"   # garland red
RED_L     = "#e74c3c"
WHITE     = "#ffffff"
OFF_WHITE = "#f8f3e0"
PINK_EAR  = "#f0a0a0"   # inner ear pink
BROWN     = "#5a3010"
DARK_BR   = "#2d1507"
BLUE_BG   = "#2c4a7c"   # background mandala blue
SILVER    = "#c0c0c0"
DARK_GREY = "#3a3a3a"
CREAM     = "#fff5d0"
TIKA_RED  = "#c0392b"
ORANGE    = "#e67e22"
YELLOW    = "#f1c40f"
IVORY     = "#fffff0"

# ─────────────────────────────────────────────
#  1. BACKGROUND MANDALA / FRAME
# ─────────────────────────────────────────────

def draw_background():
    # Outer dark gold frame
    filled_ellipse(0, -30, 420, 480, "#3d2000", GOLD, 4)
    # Inner mandala blue circle
    filled_circle(0, 90, 300, BLUE_BG, "#1a2a4a", 3)
    # Decorative mandala petals
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        px = 290 * math.cos(rad)
        py = 90 + 290 * math.sin(rad)
        filled_ellipse(px, py, 28, 14, GOLD_L, GOLD, 2)
    # Inner gold ring
    arc_line(0, 90, 270, 0, 360, GOLD, 4)
    arc_line(0, 90, 260, 0, 360, GOLD_L, 2)
    # Decorative dots on mandala
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        dot(260*math.cos(rad), 90+260*math.sin(rad), 8, GOLD_HL)

# ─────────────────────────────────────────────
#  2. CROWN (Mukut) — tall golden headdress
# ─────────────────────────────────────────────

def draw_crown():
    # Main crown base — wide arch
    crown_pts = [(-130, 260), (-150, 320), (-120, 370), (-80, 420),
                 (-40, 460), (0, 480), (40, 460), (80, 420),
                 (120, 370), (150, 320), (130, 260)]
    polygon(crown_pts, GOLD, DARK_BR, 3)

    # Crown upper arch fill
    upper = [(-80, 380), (-60, 430), (-20, 470), (0, 485),
             (20, 470), (60, 430), (80, 380)]
    polygon(upper, GOLD_L, GOLD, 2)

    # Central tall spire
    spire = [(-22, 440), (-30, 470), (-12, 500), (0, 520),
             (12, 500), (30, 470), (22, 440)]
    polygon(spire, GOLD_HL, GOLD, 2)
    dot(0, 530, 18, GOLD_L)
    dot(0, 530, 10, WHITE)

    # Crown decorations — vertical ribs
    for ox in [-90, -55, -20, 0, 20, 55, 90]:
        t.pencolor(GOLD_L); t.pensize(2)
        goto(ox, 280); t.pendown()
        t.goto(ox*0.6, 440); t.penup()

    # Jewels on crown
    jewel_positions = [(-100, 310), (-60, 350), (-20, 385),
                        (20, 385), (60, 350), (100, 310)]
    colors = [RED_FLWR, BLUE_BG, "#16a085", RED_FLWR, BLUE_BG, "#16a085"]
    for (jx, jy), jc in zip(jewel_positions, colors):
        filled_ellipse(jx, jy, 10, 8, jc, GOLD, 2)
        dot(jx, jy, 4, WHITE)

    # Center forehead jewel (large)
    filled_ellipse(0, 295, 18, 14, "#1a3a8a", GOLD_L, 3)
    dot(0, 295, 6, WHITE)

    # Crown halo ring — prabha
    arc_line(0, 200, 240, 30, 150, GOLD_L, 5)
    arc_line(0, 200, 232, 35, 145, GOLD, 3)
    # Small flame-tips on halo
    for angle in range(30, 155, 15):
        rad = math.radians(angle)
        tip_x = 248 * math.cos(rad)
        tip_y = 200 + 248 * math.sin(rad)
        filled_ellipse(tip_x, tip_y, 9, 14, GOLD_HL, GOLD, 2)

    # Crown base band
    polygon([(-140, 255), (-135, 280), (135, 280), (140, 255)],
            MAROON, GOLD, 3)
    # Gems on crown band
    for bx in range(-110, 120, 30):
        filled_ellipse(bx, 267, 8, 6, RED_FLWR, GOLD_L, 1)

# ─────────────────────────────────────────────
#  3. EARS — large pink elephant ears
# ─────────────────────────────────────────────

def draw_ears():
    # LEFT ear (viewer right of image)
    left_ear = [(-130, 220), (-200, 200), (-240, 130), (-250, 50),
                (-230, -20), (-190, -60), (-150, -50), (-130, 10), (-120, 120)]
    polygon(left_ear, SKIN_D, SKIN_D, 2)
    # Inner left ear (pink)
    left_inner = [(-148, 190), (-195, 170), (-220, 100), (-225, 30),
                  (-205, -20), (-175, -40), (-155, -20), (-148, 60), (-145, 140)]
    polygon(left_inner, PINK_EAR, PINK_EAR, 1)
    # Ear outline
    t.pencolor(SKIN_D); t.pensize(3)
    pts = left_ear + [left_ear[0]]
    goto(pts[0])
    for p in pts[1:]: t.goto(p)

    # RIGHT ear (viewer left)
    right_ear = [(130, 220), (200, 200), (240, 130), (250, 50),
                 (230, -20), (190, -60), (150, -50), (130, 10), (120, 120)]
    polygon(right_ear, SKIN_D, SKIN_D, 2)
    right_inner = [(148, 190), (195, 170), (220, 100), (225, 30),
                   (205, -20), (175, -40), (155, -20), (148, 60), (145, 140)]
    polygon(right_inner, PINK_EAR, PINK_EAR, 1)

    # Ear jewelry — earrings
    filled_circle(-195, -40, 20, GOLD, DARK_BR, 3)
    filled_circle(-195, -40, 11, RED_FLWR, DARK_BR, 2)
    dot(-195, -40, 5, GOLD_HL)

    filled_circle(195, -40, 20, GOLD, DARK_BR, 3)
    filled_circle(195, -40, 11, RED_FLWR, DARK_BR, 2)
    dot(195, -40, 5, GOLD_HL)

# ─────────────────────────────────────────────
#  4. HEAD / FACE — main oval
# ─────────────────────────────────────────────

def draw_face():
    # Face outline — large rounded head
    filled_ellipse(0, 80, 155, 200, SKIN, SKIN_D, 3)

    # Forehead highlight
    filled_ellipse(0, 200, 110, 70, CREAM, CREAM, 1)

    # Cheek shading
    filled_ellipse(-80, 80, 50, 40, SKIN_D, SKIN_D, 1)
    filled_ellipse(80, 80, 50, 40, SKIN_D, SKIN_D, 1)

# ─────────────────────────────────────────────
#  5. EYES — small kind eyes
# ─────────────────────────────────────────────

def draw_eyes():
    # Left eye
    filled_ellipse(-55, 140, 22, 14, WHITE, DARK_BR, 2)
    filled_circle(-55, 140, 9, DARK_BR, DARK_BR, 1)
    dot(-55, 144, 4, WHITE)  # catchlight
    # Eyelashes left
    arc_line(-55, 140, 22, 180, 360, DARK_BR, 3)
    # Eyebrow left
    t.pencolor(DARK_BR); t.pensize(4)
    arc_line(-55, 152, 26, 195, 345, DARK_BR, 4)

    # Right eye
    filled_ellipse(55, 140, 22, 14, WHITE, DARK_BR, 2)
    filled_circle(55, 140, 9, DARK_BR, DARK_BR, 1)
    dot(55, 144, 4, WHITE)
    arc_line(55, 140, 22, 180, 360, DARK_BR, 3)
    arc_line(55, 152, 26, 195, 345, DARK_BR, 4)

# ─────────────────────────────────────────────
#  6. THIRD EYE / TILAK on forehead
# ─────────────────────────────────────────────

def draw_tilak():
    # Tilak — orange/red mark
    tilak_pts = [(-14, 200), (-6, 230), (0, 240), (6, 230), (14, 200),
                 (6, 198), (0, 196), (-6, 198)]
    polygon(tilak_pts, TIKA_RED, "#8b0000", 2)
    # White dot in center
    dot(0, 212, 10, WHITE)
    dot(0, 212, 5, RED_L)

    # Bindi dots row (chandrakor)
    for bx in [-25, -12, 0, 12, 25]:
        dot(bx, 190, 5, MAROON)

# ─────────────────────────────────────────────
#  7. TRUNK — curved downward trunk
# ─────────────────────────────────────────────

def draw_trunk():
    # Trunk body — curved to the left (as in reference)
    trunk_pts = [
        (-30, 80), (-55, 55), (-75, 20), (-85, -20),
        (-80, -60), (-65, -90), (-50, -100), (-35, -95),
        (-20, -80), (-18, -55),
        (-25, -20), (-25, 20), (-15, 55), (5, 80)
    ]
    # Outer trunk
    polygon(trunk_pts, SKIN_D, SKIN_D, 1)
    # Inner trunk fill (lighter)
    inner_trunk = [
        (-22, 70), (-42, 48), (-58, 15), (-65, -18),
        (-61, -55), (-50, -82), (-39, -90), (-28, -86),
        (-18, -72), (-16, -50),
        (-20, -18), (-19, 18), (-10, 50), (3, 70)
    ]
    polygon(inner_trunk, SKIN, SKIN, 1)
    # Trunk tip curl
    filled_circle(-40, -98, 14, SKIN_D, SKIN_D, 1)
    filled_circle(-38, -96, 10, SKIN, SKIN, 1)
    # Trunk ridges (wrinkles)
    t.pencolor(SKIN_D); t.pensize(2)
    for (rx1, ry1, rx2, ry2) in [
        (-35, 50, -55, 45), (-48, 15, -65, 8),
        (-58, -20, -70, -28), (-60, -55, -68, -62)
    ]:
        goto(rx1, ry1); t.pendown(); t.goto(rx2, ry2); t.penup()

# ─────────────────────────────────────────────
#  8. MOUTH — gentle smile
# ─────────────────────────────────────────────

def draw_mouth():
    # Lips
    # Upper lip
    t.pencolor(DARK_BR); t.pensize(3)
    arc_line(-25, 62, 25, 0, 180, DARK_BR, 3)
    # Lower lip / smile
    arc_line(0, 48, 30, 200, 340, DARK_BR, 3)
    filled_ellipse(0, 55, 22, 10, "#e8957a", DARK_BR, 2)

# ─────────────────────────────────────────────
#  9. NOSE — broad elephant nose bridge
# ─────────────────────────────────────────────

def draw_nose():
    filled_ellipse(0, 95, 20, 12, SKIN_D, SKIN_D, 2)
    dot(-10, 95, 8, DARK_BR)
    dot(10, 95, 8, DARK_BR)

# ─────────────────────────────────────────────
#  10. JEWELRY — necklace, forehead band
# ─────────────────────────────────────────────

def draw_jewelry():
    # Forehead ornament band above eyes
    polygon([(-135, 250), (-120, 260), (120, 260), (135, 250),
             (120, 242), (-120, 242)], GOLD, DARK_BR, 2)
    for jx in range(-110, 120, 22):
        filled_ellipse(jx, 251, 8, 6, RED_FLWR, GOLD, 1)

    # Necklace base
    arc_line(0, -100, 130, 210, 330, GOLD, 6)
    # Necklace gems
    for angle in range(215, 328, 15):
        rad = math.radians(angle)
        nx = 130 * math.cos(rad)
        ny = -100 + 130 * math.sin(rad)
        filled_ellipse(nx, ny, 8, 6,
                       [RED_FLWR, GOLD_L, "#16a085", MAROON_L][angle//15 % 4],
                       DARK_BR, 1)

    # Pearl strands
    for strand_r in [115, 100]:
        for angle in range(215, 328, 9):
            rad = math.radians(angle)
            dot(strand_r*math.cos(rad), -100+strand_r*math.sin(rad), 5, IVORY)

    # Center pendant
    filled_ellipse(0, -225, 16, 20, GOLD_L, DARK_BR, 3)
    filled_ellipse(0, -225, 10, 13, RED_FLWR, DARK_BR, 2)
    dot(0, -225, 4, GOLD_HL)

# ─────────────────────────────────────────────
#  11. RED GARLAND (Haar) draped across chest
# ─────────────────────────────────────────────

def draw_garland():
    # Main garland arc — red flowers
    for angle in range(215, 328, 8):
        rad = math.radians(angle)
        gx = 148 * math.cos(rad)
        gy = -100 + 148 * math.sin(rad)
        filled_circle(gx, gy, 9, RED_FLWR, "#8b0000", 1)
        dot(gx, gy, 4, RED_L)

    # Second inner strand
    for angle in range(220, 322, 10):
        rad = math.radians(angle)
        gx = 162 * math.cos(rad)
        gy = -100 + 162 * math.sin(rad)
        filled_circle(gx, gy, 7, "#c0392b", "#7a0000", 1)

    # Hanging garland tassels below
    tassel_y_start = -228
    for tx, tc in [(-40, RED_FLWR), (0, RED_FLWR), (40, RED_FLWR)]:
        t.pencolor(tc); t.pensize(3)
        goto(tx, tassel_y_start)
        t.pendown(); t.goto(tx, tassel_y_start - 35); t.penup()
        filled_circle(tx, tassel_y_start - 42, 8, tc, "#7a0000", 2)

# ─────────────────────────────────────────────
#  12. SHOULDER SHAWL / UPPER BODY
# ─────────────────────────────────────────────

def draw_body():
    # Shoulders — golden shawl
    shoulder_pts = [(-200, -130), (-175, -150), (-140, -170),
                    (-100, -185), (0, -195), (100, -185),
                    (140, -170), (175, -150), (200, -130),
                    (195, -200), (150, -240), (0, -260),
                    (-150, -240), (-195, -200)]
    polygon(shoulder_pts, GOLD, DARK_BR, 3)
    # Shawl pattern lines
    t.pencolor(GOLD_L); t.pensize(1)
    for ox in range(-150, 170, 20):
        goto(ox, -165); t.pendown()
        t.goto(ox*0.7, -255); t.penup()

    # Maroon dhoti band below shawl
    polygon([(-195, -200), (-150, -240), (0, -260),
             (150, -240), (195, -200),
             (180, -265), (0, -285), (-180, -265)],
            MAROON, "#3d0010", 3)

    # Body center jewel
    filled_ellipse(0, -175, 14, 18, GOLD_L, DARK_BR, 3)
    filled_ellipse(0, -175, 9, 12, BLUE_BG, GOLD, 2)
    dot(0, -175, 4, WHITE)

# ─────────────────────────────────────────────
#  13. TEXT LABEL
# ─────────────────────────────────────────────

def draw_label():
    t.penup()
    t.goto(0, -360)
    t.pencolor(GOLD_L)
    t.write("॥ श्री गणेशाय नमः ॥", align="center",
            font=("Arial", 18, "bold"))
    t.goto(0, -390)
    t.pencolor(GOLD)
    t.write("Ganesh Ji  —  HJ Developer", align="center",
            font=("Arial", 11, "normal"))

# ─────────────────────────────────────────────
#  MAIN RENDER ORDER
# ─────────────────────────────────────────────

draw_background()
draw_crown()
draw_ears()
draw_face()
draw_body()
draw_garland()
draw_jewelry()
draw_trunk()
draw_nose()
draw_eyes()
draw_tilak()
draw_mouth()
draw_label()

screen.update()
turtle.done()
