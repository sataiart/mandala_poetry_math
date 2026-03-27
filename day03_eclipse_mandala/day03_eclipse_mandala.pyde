poem_lines = [
    "闇が円を包みこむ",
    "白い祈りが浮かびあがる",
    "見えるものはまた消える",
    "回転だけが残っている"
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
        layer = {
            "radius": 120 + i * 95,
            "petals": 10 + i * 4,
            "petal_len": 55 + i * 18,
            "weight": 1.2 + i * 0.3,
            "speed": 0.002 + i * 0.0015,
            "phase": i * 0.9,
            "blink_speed": 0.035 + i * 0.01
        }
        layers.append(layer)

def draw():
    pg.beginDraw()
    pg.background(0)
    pg.translate(RENDER_W / 2, RENDER_H / 2)

    # 全体回転
    pg.rotate(frameCount * 0.0025)

    pg.noFill()
    pg.stroke(255)

    # 中心
    pg.strokeWeight(1.4)
    pg.ellipse(0, 0, 36, 36)

    for i, layer in enumerate(layers):
        pg.pushMatrix()
        direction = 1 if i % 2 == 0 else -1
        pg.rotate(frameCount * layer["speed"] * direction)
        draw_layer(pg, layer, i)
        pg.popMatrix()

    pg.endDraw()

    background(0)
    image(pg, 0, 0, width, height)

    if frameCount == OUTPUT_STILL_FRAME:
        pg.save("output/day03_still.png")

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

    # 層全体の見え方を時間で変える
    layer_visibility = (sin(frameCount * layer["blink_speed"] + layer["phase"]) + 1) / 2

    # あまりにも薄いときは描かない
    if layer_visibility < 0.15:
        return

    alpha_value = map(layer_visibility, 0.15, 1.0, 40, 255)
    g.stroke(255, alpha_value)
    g.strokeWeight(layer["weight"])

    for j in range(petals):
        angle = TWO_PI / petals * j

        # 花弁ごとにも少し位相差
        petal_visibility = (sin(frameCount * 0.06 + j * 0.45 + layer["phase"]) + 1) / 2

        if petal_visibility < 0.25:
            continue

        local_alpha = map(petal_visibility, 0.25, 1.0, 30, alpha_value)

        x = cos(angle) * radius
        y = sin(angle) * radius

        pulse = sin(frameCount * 0.05 + j * 0.25 + idx) * 10

        g.pushMatrix()
        g.translate(x, y)
        g.rotate(angle)

        g.stroke(255, local_alpha)

        # 花弁
        g.ellipse(0, 0, petal_len + pulse, petal_len * 0.18 + pulse * 0.12)

        # 装飾線
        g.line(0, 0, -radius * 0.16, 0)

        g.popMatrix()
