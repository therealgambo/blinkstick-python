from blinkstick.blinkstick import get_first, get_by_serial, blinkstick_remap_color

import time


class BlinkStickPro(object):
    """
    BlinkStickPro class is specifically designed to control the individually
    addressable LEDs connected to the device. The tutorials section contains
    all the details on how to connect them to BlinkStick Pro.

    U{http://www.blinkstick.com/help/tutorials}

    Code example on how you can use this class are available here:

    U{https://github.com/arvydas/blinkstick-python/wiki#code-examples-for-blinkstick-pro}
    """

    def __init__(self, r_led_count=0, g_led_count=0, b_led_count=0, delay=0.002, max_rgb_value=255):
        """
        Initialize BlinkStickPro class.

        @type r_led_count: int
        @param r_led_count: number of LEDs on R channel
        @type g_led_count: int
        @param g_led_count: number of LEDs on G channel
        @type b_led_count: int
        @param b_led_count: number of LEDs on B channel
        @type delay: int
        @param delay: default transmission delay between frames
        @type max_rgb_value: int
        @param max_rgb_value: maximum color value for RGB channels
        """

        self.r_led_count = r_led_count
        self.g_led_count = g_led_count
        self.b_led_count = b_led_count

        self.fps_count = -1

        self.data_transmission_delay = delay

        self.max_rgb_value = max_rgb_value

        # initialise data store for each channel
        # pre-populated with zeroes

        self.data = [[], [], []]

        for i in range(0, r_led_count):
            self.data[0].append([0, 0, 0])

        for i in range(0, g_led_count):
            self.data[1].append([0, 0, 0])

        for i in range(0, b_led_count):
            self.data[2].append([0, 0, 0])

        self.bstick = None

    def set_color(self, channel, index, r, g, b, remap_values=True):
        """
        Set the color of a single pixel

        @type channel: int
        @param channel: R, G or B channel
        @type index: int
        @param index: the index of LED on the channel
        @type r: int
        @param r: red color byte
        @type g: int
        @param g: green color byte
        @type b: int
        @param b: blue color byte
        @type remap_values: bool
        @param remap_values: remap color values
        """

        if remap_values:
            r, g, b = [blinkstick_remap_color(val, self.max_rgb_value) for val in [r, g, b]]

        self.data[channel][index] = [g, r, b]

    def get_color(self, channel, index):
        """
        Get the current color of a single pixel.

        @type  channel: int
        @param channel: the channel of the LED
        @type  index: int
        @param index: the index of the LED

        @rtype: (int, int, int)
        @return: 3-tuple for R, G and B values
        """

        val = self.data[channel][index]
        return [val[1], val[0], val[2]]

    def clear(self):
        """
        Set all pixels to black in the frame buffer.
        """
        for x in range(0, self.r_led_count):
            self.set_color(0, x, 0, 0, 0)

        for x in range(0, self.g_led_count):
            self.set_color(1, x, 0, 0, 0)

        for x in range(0, self.b_led_count):
            self.set_color(2, x, 0, 0, 0)

    def off(self):
        """
        Set all pixels to black in on the device.
        """
        self.clear()
        self.send_data_all()

    def connect(self, serial=None):
        """
        Connect to the first BlinkStick found

        @type serial: str
        @param serial: Select the serial number of BlinkStick
        """

        if serial is None:
            self.bstick = get_first()
        else:
            self.bstick = get_by_serial(serial=serial)

        return self.bstick is not None

    def send_data(self, channel):
        """
        Send data stored in the internal buffer to the channel.

        @param channel:
            - 0 - R pin on BlinkStick Pro board
            - 1 - G pin on BlinkStick Pro board
            - 2 - B pin on BlinkStick Pro board
        """
        packet_data = [item for sublist in self.data[channel] for item in sublist]

        try:
            self.bstick.set_led_data(channel, packet_data)
            time.sleep(self.data_transmission_delay)
        except Exception as e:
            print("Exception: {0}".format(e))

    def send_data_all(self):
        """
        Send data to all channels
        """
        if self.r_led_count > 0:
            self.send_data(0)

        if self.g_led_count > 0:
            self.send_data(1)

        if self.b_led_count > 0:
            self.send_data(2)
