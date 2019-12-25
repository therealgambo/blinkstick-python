from blinkstick.BlinkStick import BlinkStick, blinkstick_remap_rgb_value_reverse

import asyncio


class AsyncBlinkStick(BlinkStick):
    """
    Controls BlinkStick devices in exactly the same was as the BlinkStick
    class, but uses asyncio.sleep instead of time.sleep so that it plays nice
    with code written using asyncio
    """

    @asyncio.coroutine
    def pulse(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hexadecimal=None, repeats=1, duration=1000,
              steps=50):
        """
        Morph to the specified color from black and back again.

        @type channel: int
        @param channel: led channel
        @type index: int
        @param index: led channel index
        @type  red: int
        @param red: Red color intensity 0 is off, 255 is full red intensity
        @type  green: int
        @param green: Green color intensity 0 is off, 255 is full green intensity
        @type  blue: int
        @param blue: Blue color intensity 0 is off, 255 is full blue intensity
        @type  name: str
        @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
        @type  hexadecimal: str
        @param hexadecimal: Specify color using hexadecimal color value e.g. '#FF3366'
        @type  repeats: int
        @param repeats: Number of times to pulse the LED
        @type  duration: int
        @param duration: Duration for pulse in milliseconds
        @type  steps: int
        @param steps: Number of gradient steps
        """
        r, g, b = self._determine_rgb(red=red, green=green, blue=blue, name=name, hexadecimal=hexadecimal)

        self.turn_off()
        for x in range(repeats):
            yield from self.morph(channel=channel, index=index, red=r, green=g, blue=b, duration=duration, steps=steps)
            yield from self.morph(channel=channel, index=index, red=0, green=0, blue=0, duration=duration, steps=steps)

    @asyncio.coroutine
    def blink(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hexadecimal=None, repeats=1, delay=500):
        """
        Blink the specified color.

        Asyncio friendly version

        @type channel: int
        @param channel: led channel
        @type index: int
        @param index: led channel index
        @type  red: int
        @param red: Red color intensity 0 is off, 255 is full red intensity
        @type  green: int
        @param green: Green color intensity 0 is off, 255 is full green intensity
        @type  blue: int
        @param blue: Blue color intensity 0 is off, 255 is full blue intensity
        @type  name: str
        @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
        @type  hexadecimal: str
        @param hexadecimal: Specify color using hexadecimal color value e.g. '#FF3366'
        @type  repeats: int
        @param repeats: Number of times to pulse the LED
        @type  delay: int
        @param delay: time in milliseconds to light LED for, and also between blinks
        """
        r, g, b = self._determine_rgb(red=red, green=green, blue=blue, name=name, hexadecimal=hexadecimal)
        ms_delay = float(delay) / float(1000)
        for x in range(repeats):
            if x:
                yield from asyncio.sleep(ms_delay)
            self.set_color(channel=channel, index=index, red=r, green=g, blue=b)
            yield from asyncio.sleep(ms_delay)
            self.set_color(channel=channel, index=index)

    @asyncio.coroutine
    def morph(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hexadecimal=None, duration=1000, steps=50):
        """
        Morph to the specified color.

        @type channel: int
        @param channel: led channel
        @type index: int
        @param index: led channel index
        @type  red: int
        @param red: Red color intensity 0 is off, 255 is full red intensity
        @type  green: int
        @param green: Green color intensity 0 is off, 255 is full green intensity
        @type  blue: int
        @param blue: Blue color intensity 0 is off, 255 is full blue intensity
        @type  name: str
        @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
        @type  hexadecimal: str
        @param hexadecimal: Specify color using hexadecimal color value e.g. '#FF3366'
        @type  duration: int
        @param duration: Duration for morph in milliseconds
        @type  steps: int
        @param steps: Number of gradient steps (default 50)
        """
        r_end, g_end, b_end = self._determine_rgb(red=red, green=green, blue=blue, name=name, hexadecimal=hexadecimal)

        r_start, g_start, b_start = blinkstick_remap_rgb_value_reverse(self._get_color_rgb(index), self.max_rgb_value)

        gradient = self._get_grandient_values(r_start, g_start, b_start, r_end, g_end, b_end, steps)

        ms_delay = float(duration) / float(1000 * steps)

        self.set_color(channel=channel, index=index, red=r_start, green=g_start, blue=b_start)

        for grad in gradient:
            grad_r, grad_g, grad_b = grad

            self.set_color(channel=channel, index=index, red=grad_r, green=grad_g, blue=grad_b)
            yield from asyncio.sleep(ms_delay)

        self.set_color(channel=channel, index=index, red=r_end, green=g_end, blue=b_end)
