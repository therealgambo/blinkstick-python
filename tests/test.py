from blinkstick.BlinkStick import get_all

for bstick in get_all():
    bstick.set_random_color()
    print(bstick.get_serial() + " " + bstick.get_color(color_format="hex"))