poem_lines = [
    "光は戻る",
    "影はほどける",
    "光はまた戻る",
    "花は内側へ咲いていく"
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

BASE_PETALS = 10
MAX_DEPTH = 4

pg = None

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

    # 全体回転
    pg.rotate(frameCount * 0.003)

    pg.noFill()
    pg.stroke(0)
    pg.strokeWeight(1.2)

    # 中心
    pg.ellipse(0, 0, 28, 28)

    for i in range(BASE_PETALS):
        angle = TWO_PI / BASE_PETALS * i
        pg.pushMatrix()
        pg.rotate(angle)
        draw_recursive_petal(pg, 140, 0, MAX_DEPTH)
        pg.popMatrix()

    pg.endDraw()

    background(255)
    image(pg, 0, 0, width, height)

    if frameCount == OUTPUT_STILL_FRAME:
        pg.save("output/day04_still.png")

    if EXPORT_MODE:
        if frameCount <= TOTAL_FRAMES:
            pg.save(FRAME_DIR + "/frame-" + nf(frameCount, 4) + ".png")
        else:
            noLoop()
            exit()

def draw_recursive_petal(g, length, depth, max_depth):
    if depth >= max_depth or length < 12:
        return

    # 脈動
    pulse = sin(frameCount * 0.05 + depth * 0.8) * 6

    # 主軸
    g.line(0, 0, length + pulse, 0)

    # 花弁
    g.pushMatrix()
    g.translate(length * 0.6, 0)
    g.ellipse(0, 0, length * 0.55 + pulse, length * 0.18 + pulse * 0.08)
    g.popMatrix()

    # 先端へ移動
    g.pushMatrix()
    g.translate(length + pulse * 0.3, 0)

    # 小さな花弁を左右に再帰
    spread = 0.45 + depth * 0.08 + sin(frameCount * 0.03 + depth) * 0.04

    g.pushMatrix()
    g.rotate(spread)
    draw_recursive_petal(g, length * 0.62, depth + 1, max_depth)
    g.popMatrix()

    g.pushMatrix()
    g.rotate(-spread)
    draw_recursive_petal(g, length * 0.62, depth + 1, max_depth)
    g.popMatrix()

    g.popMatrix()
