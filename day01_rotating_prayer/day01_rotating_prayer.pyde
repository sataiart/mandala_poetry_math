poem_lines = [
    "光は円を描く",
    "静けさはひらく",
    "数は祈りになる",
    "わたしは中心へ戻る"
]

layers = []

def setup():
    size(1080, 1080)
    smooth()
    frameRate(30)
    noFill()
    stroke(255, 220)

    for i, line in enumerate(poem_lines):
        char_count = len(line)
        layer = {
            "radius": 100 + i * 90,
            "petals": max(6, char_count + i * 2),
            "petal_len": 30 + char_count * 3,
            "weight": 1 + i * 0.4,
            "speed": 0.002 + i * 0.0015
        }
        layers.append(layer)

def draw():
    background(10, 10, 20)
    translate(width/2, height/2)

    # 全体回転
    rotate(frameCount * 0.003)

    # 中心円
    stroke(255, 180)
    strokeWeight(1.5)
    ellipse(0, 0, 40, 40)

    # 各層を描く
    for i, layer in enumerate(layers):
        pushMatrix()
        rotate(frameCount * layer["speed"])
        draw_layer(layer, i)
        popMatrix()

def draw_layer(layer, idx):
    petals = layer["petals"]
    radius = layer["radius"]
    petal_len = layer["petal_len"]

    strokeWeight(layer["weight"])

    for j in range(petals):
        angle = TWO_PI / petals * j
        x = cos(angle) * radius
        y = sin(angle) * radius

        # 花弁の長さを脈動
        pulse = sin(frameCount * 0.05 + j * 0.3 + idx) * 12

        pushMatrix()
        translate(x, y)
        rotate(angle)

        # 花弁っぽい形
        ellipse(0, 0, petal_len + pulse, petal_len * 0.35 + pulse * 0.2)

        # 中心に向かう線
        line(0, 0, -radius * 0.15, 0)
        popMatrix()
