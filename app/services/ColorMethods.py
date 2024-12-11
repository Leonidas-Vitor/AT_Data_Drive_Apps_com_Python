import random

def gerar_cor_rgb():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def gerar_cor_hex():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "#{:02X}{:02X}{:02X}".format(r, g, b)