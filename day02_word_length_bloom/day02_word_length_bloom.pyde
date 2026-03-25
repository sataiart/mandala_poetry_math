poem_lines = [
    "青い円はひらく",
    "静かな数字が揺れる",
    "詩は回転して咲く",
    "中心で光が眠る"
]

layers = []

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

def setup():
    global pg
    size(PREVIEW_W, PREVIEW_H)
    frameRate(FPS)
    smooth()

    pg = createGraphics(RENDER_W, RENDER_H)

    for i, line in enumerate(poem_lines):
        char_count = len(line)
        layer = {
            "radius": 120 + i * 95,
            "petals": max(8, char_count + 2),
            "petal_len": 20 + char_count * 8,
            "weight": 1.2 + i * 0.3,
            "speed": 0.002 + char_count * 0.00015
        }
        layers.append(layer)

def draw():
    pg.beginDraw()
    pg.background(255)
    pg.translate(RENDER_W / 2, RENDER_H / 2)

    # 全体回転
    pg.rotate(frameCount * 0.0025)

    pg.noFill()
    pg.stroke(0, 220)

    # 中心
    pg.strokeWeight(1.5)
    pg.ellipse(0, 0, 40, 40)

    for i, layer in enumerate(layers):
        pg.pushMatrix()
        pg.rotate(frameCount * layer["speed"] * (1 if i % 2 == 0 else -1))
        draw_layer(pg, layer, i)
        pg.popMatrix()

    pg.endDraw()

    background(0)
    image(pg, 0, 0, width, height)

    if frameCount == OUTPUT_STILL_FRAME:
        pg.save("output/day02_still.png")

    if EXPORT_MODE:
        if frameCount <= TOTAL_FRAMES:
            pg.save(FRAME_DIR + "/frame-" + nf(frameCount, 4) + ".png")
        else:
            noLoop()
            exit()

def draw_layer(g, layer, idx):
    petals = layer["petals"]
    radius = layer["radius"]
    petal_len = layer["petal_len"]

    g.strokeWeight(layer["weight"])

    for j in range(petals):
        angle = TWO_PI / petals * j
        x = cos(angle) * radius
        y = sin(angle) * radius

        pulse = sin(frameCount * 0.06 + j * 0.35 + idx) * 10

        g.pushMatrix()
        g.translate(x, y)
        g.rotate(angle)

        # 花弁
        g.ellipse(0, 0, petal_len + pulse, petal_len * 0.22 + pulse * 0.15)

        # 装飾線
        g.line(0, 0, -radius * 0.18, 0)

        g.popMatrix()
