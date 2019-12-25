from blinkstick.BlinkStick import get_first
from blinkstick.AsyncBlinkStick import AsyncBlinkStick

import asyncio


@asyncio.coroutine
def do_other_stuff(delay, repeats):
    for i in range(1, repeats+1):
        print('Doing stuff {}'.format(i))
        yield from asyncio.sleep(delay)


@asyncio.coroutine
def main():
    device = get_first(blinkstick=AsyncBlinkStick)
    # Both of these tasks take 5 seconds
    yield from asyncio.wait([
        device.pulse(blue=50, repeats=3, duration=1000, channel=0, index=1),
        device.blink(green=100, repeats=5, delay=100, channel=0, index=0),
        do_other_stuff(repeats=10, delay=0.5),
    ])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
