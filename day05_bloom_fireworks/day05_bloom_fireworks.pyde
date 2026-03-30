poem_lines = [
    "花はひらいてあふれ出す",
    "光は輪になり踊りだす",
    "祝福だけが空へ散る",
    "今日の中心は、咲くためにある"
]

PREVIEW_W = 900
PREVIEW_H = 900

RENDER_W = 1080
RENDER_H = 1080

FPS = 30
DURATION_SEC = 6
TOTAL_FRAMES = FPS * DURATION_SEC

EXPORT_MODE = True
FRAME_DIR = "temp_frames"
OUTPUT_STILL_FRAME = 90

pg = None

RINGS = [
    {"radius": 110, "petals": 14, "length": 70, "speed": 0.0025, "weight": 1.2},
    {"radius": 190, "petals": 20, "length": 95, "speed": -0.0018, "weight": 1.0},
    {"radius": 280, "petals": 28, "length": 120, "speed": 0.0012, "weight": 0.9}
]

def setup():
    global pg
    size(PREVIEW_W, PREVIEW_H)
    frameRate(FPS)
    smooth()
    pg = createGraphics(RENDER_W, RENDER_H)

def draw():
    pg.beginDraw()
    pg.background(255)
    pg.translate(RENDER_W / 2, RENDER_H / 2)
    pg.noFill()
    pg.stroke(0)

    # 中心の小円
    pg.strokeWeight(1.4)
    pg.ellipse(0, 0, 26, 26)

    # 各リングを描画
    for idx, ring in enumerate(RINGS):
        pg.pushMatrix()
        pg.rotate(frameCount * ring["speed"])
        draw_bloom_ring(pg, ring, idx)
        pg.popMatrix()

    # 全体に細い回転線を追加
    pg.pushMatrix()
    pg.rotate(frameCount * 0.001)
    draw_outer_halo(pg, 340, 36)
    pg.popMatrix()

    pg.endDraw()

    background(255)
    image(pg, 0, 0, width, height)

    if frameCount == OUTPUT_STILL_FRAME:
        pg.save("output/day05_still.png")

    if EXPORT_MODE:
        if frameCount <= TOTAL_FRAMES:
            pg.save(FRAME_DIR + "/frame-" + nf(frameCount, 4) + ".png")
        else:
            noLoop()
            exit()

def draw_bloom_ring(g, ring, idx):
    radius = ring["radius"]
    petals = ring["petals"]
    length = ring["length"]
    weight = ring["weight"]

    for j in range(petals):
        angle = TWO_PI / petals * j
        pulse = sin(frameCount * 0.05 + j * 0.25 + idx) * 10
        flare = sin(frameCount * 0.03 + j * 0.18 + idx * 0.5) * 6

        x = cos(angle) * radius
        y = sin(angle) * radius

        g.pushMatrix()
        g.translate(x, y)
        g.rotate(angle)

        g.strokeWeight(weight)

        # 外へ伸びる主線
        g.line(0, 0, length + pulse, 0)

        # 花火っぽい楕円花弁
        g.ellipse(length * 0.55, 0, length * 0.55 + flare, length * 0.18 + pulse * 0.08)

        # 左右の補助花弁
        g.pushMatrix()
        g.translate(length * 0.7, 0)
        g.rotate(0.45)
        g.ellipse(0, 0, length * 0.22 + flare, length * 0.08)
        g.popMatrix()

        g.pushMatrix()
        g.translate(length * 0.7, 0)
        g.rotate(-0.45)
        g.ellipse(0, 0, length * 0.22 + flare, length * 0.08)
        g.popMatrix()

        # 先端の粒
        g.ellipse(length + 18 + flare, 0, 8 + idx * 2, 8 + idx * 2)

        g.popMatrix()

def draw_outer_halo(g, radius, count):
    g.strokeWeight(0.8)
    for i in range(count):
        angle = TWO_PI / count * i
        pulse = sin(frameCount * 0.04 + i * 0.3) * 12
        x = cos(angle) * (radius + pulse)
        y = sin(angle) * (radius + pulse)
        g.ellipse(x, y, 10, 10)
