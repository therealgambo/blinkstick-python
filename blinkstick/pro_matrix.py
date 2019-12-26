from blinkstick.pro import BlinkStickPro
from blinkstick.blinkstick import blinkstick_remap_color


class BlinkStickProMatrix(BlinkStickPro):
    """
    BlinkStickProMatrix class is specifically designed to control the individually
    addressable LEDs connected to the device and arranged in a matrix. The tutorials section contains
    all the details on how to connect them to BlinkStick Pro with matrices.

    U{http://www.blinkstick.com/help/tutorials/blinkstick-pro-adafruit-neopixel-matrices}

    Code example on how you can use this class are available here:

    U{https://github.com/arvydas/blinkstick-python/wiki#code-examples-for-blinkstick-pro}

    Matrix is driven by using L{BlinkStickProMatrix.set_color} with [x,y] coordinates and class automatically
    divides data into subsets and sends it to the matrices.

    For example, if you have 2 8x8 matrices connected to BlinkStickPro and you initialize
    the class with

        >>> matrix = BlinkStickProMatrix(r_columns=8, r_rows=8, g_columns=8, g_rows=8)

    Then you can set the internal framebuffer by using {set_color} command:

        >>> matrix.set_color(x=10, y=5, r=255, g=0, b=0)
        >>> matrix.set_color(x=6, y=3, r=0, g=255, b=0)

    And send data to both matrices in one go:

        >>> matrix.send_data_all()

    """

    def __init__(self, r_columns=0, r_rows=0, g_columns=0, g_rows=0, b_columns=0, b_rows=0, delay=0.002, max_rgb=255):
        """
        Initialize BlinkStickProMatrix class.

        @type r_columns: int
        @param r_columns: number of matric columns for R channel
        @type g_columns: int
        @param g_columns: number of matric columns for R channel
        @type b_columns: int
        @param b_columns: number of matric columns for R channel
        @type delay: int
        @param delay: default transmission delay between frames
        @type max_rgb: int
        @param max_rgb: maximum color value for RGB channels
        """
        r_leds = r_columns * r_rows
        g_leds = g_columns * g_rows
        b_leds = b_columns * b_rows

        self.r_columns = r_columns
        self.r_rows = r_rows
        self.g_columns = g_columns
        self.g_rows = g_rows
        self.b_columns = b_columns
        self.b_rows = b_rows

        super(BlinkStickProMatrix, self).__init__(
            r_led_count=r_leds,
            g_led_count=g_leds,
            b_led_count=b_leds,
            delay=delay,
            max_rgb_value=max_rgb
        )

        self.rows = max(r_rows, g_rows, b_rows)
        self.cols = r_columns + g_columns + b_columns

        # initialise data store for matrix pre-populated with zeroes
        self.matrix_data = []

        for i in range(0, self.rows * self.cols):
            self.matrix_data.append([0, 0, 0])

    def set_color(self, x, y, r, g, b, remap_values=True):
        """
        Set the color of a single pixel in the internal framebuffer.

        @type x: int
        @param x: the x location in the matrix
        @type y: int
        @param y: the y location in the matrix
        @type r: int
        @param r: red color byte
        @type g: int
        @param g: green color byte
        @type b: int
        @param b: blue color byte
        @type remap_values: bool
        @param remap_values: Automatically remap values based on the {max_rgb_value} supplied in the constructor
        """

        if remap_values:
            r, g, b = [blinkstick_remap_color(val, self.max_rgb_value) for val in [r, g, b]]

        self.matrix_data[self._coord_to_index(x, y)] = [g, r, b]

    def _coord_to_index(self, x, y):
        return y * self.cols + x

    def get_color(self, x, y):
        """
        Get the current color of a single pixel.

        @type  x: int
        @param x: x coordinate of the internal framebuffer
        @type  y: int
        @param y: y coordinate of the internal framebuffer

        @rtype: (int, int, int)
        @return: 3-tuple for R, G and B values
        """

        val = self.matrix_data[self._coord_to_index(x, y)]
        return [val[1], val[0], val[2]]

    def shift_left(self, remove=False):
        """
        Shift all LED values in the matrix to the left

        @type remove: bool
        @param remove: whether to remove the pixels on the last column or move the to the first column
        """

        temp = []
        if not remove:
            for y in range(0, self.rows):
                temp.append(self.get_color(0, y))

        for y in range(0, self.rows):
            for x in range(0, self.cols - 1):
                r, g, b = self.get_color(x + 1, y)

                self.set_color(x, y, r, g, b, False)

        if remove:
            for y in range(0, self.rows):
                self.set_color(self.cols - 1, y, 0, 0, 0, False)
        else:
            for y in range(0, self.rows):
                col = temp[y]
                self.set_color(self.cols - 1, y, col[0], col[1], col[2], False)

    def shift_right(self, remove=False):
        """
        Shift all LED values in the matrix to the right

        @type remove: bool
        @param remove: whether to remove the pixels on the last column or move the to the first column
        """

        temp = []
        if not remove:
            for y in range(0, self.rows):
                temp.append(self.get_color(self.cols - 1, y))

        for y in range(0, self.rows):
            for x in reversed(range(1, self.cols)):
                r, g, b = self.get_color(x - 1, y)

                self.set_color(x, y, r, g, b, False)

        if remove:
            for y in range(0, self.rows):
                self.set_color(0, y, 0, 0, 0, False)
        else:
            for y in range(0, self.rows):
                col = temp[y]
                self.set_color(0, y, col[0], col[1], col[2], False)

    def shift_down(self, remove=False):
        """
        Shift all LED values in the matrix down

        @type remove: bool
        @param remove: whether to remove the pixels on the last column or move the to the first column
        """

        temp = []
        if not remove:
            for x in range(0, self.cols):
                temp.append(self.get_color(x, self.rows - 1))

        for y in reversed(range(1, self.rows)):
            for x in range(0, self.cols):
                r, g, b = self.get_color(x, y - 1)

                self.set_color(x, y, r, g, b, False)

        if remove:
            for x in range(0, self.cols):
                self.set_color(x, 0, 0, 0, 0, False)
        else:
            for x in range(0, self.cols):
                col = temp[x]
                self.set_color(x, 0, col[0], col[1], col[2], False)

    def shift_up(self, remove=False):
        """
        Shift all LED values in the matrix up

        @type remove: bool
        @param remove: whether to remove the pixels on the last column or move the to the first column
        """

        temp = []
        if not remove:
            for x in range(0, self.cols):
                temp.append(self.get_color(x, 0))

        for x in range(0, self.cols):
            for y in range(0, self.rows - 1):
                r, g, b = self.get_color(x, y + 1)

                self.set_color(x, y, r, g, b, False)

        if remove:
            for x in range(0, self.cols):
                self.set_color(x, self.rows - 1, 0, 0, 0, False)
        else:
            for x in range(0, self.cols):
                col = temp[x]
                self.set_color(x, self.rows - 1, col[0], col[1], col[2], False)

    def number(self, x, y, n, r, g, b):
        """
        Render a 3x5 number n at location x,y and r,g,b color

        @type x: int
        @param x: the x location in the matrix (left of the number)
        @type y: int
        @param y: the y location in the matrix (top of the number)
        @type n: int
        @param n: number digit to render 0..9
        @type r: int
        @param r: red color byte
        @type g: int
        @param g: green color byte
        @type b: int
        @param b: blue color byte
        """
        if n == 0:
            self.rectangle(x, y, x + 2, y + 4, r, g, b)
        elif n == 1:
            self.line(x + 1, y, x + 1, y + 4, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x, y + 1, r, g, b)
        elif n == 2:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x + 2, y + 1, r, g, b)
            self.set_color(x, y + 3, r, g, b)
        elif n == 3:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x + 2, y + 1, r, g, b)
            self.set_color(x + 2, y + 3, r, g, b)
        elif n == 4:
            self.line(x, y, x, y + 2, r, g, b)
            self.line(x + 2, y, x + 2, y + 4, r, g, b)
            self.set_color(x + 1, y + 2, r, g, b)
        elif n == 5:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x, y + 1, r, g, b)
            self.set_color(x + 2, y + 3, r, g, b)
        elif n == 6:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x, y + 1, r, g, b)
            self.set_color(x + 2, y + 3, r, g, b)
            self.set_color(x, y + 3, r, g, b)
        elif n == 7:
            self.line(x + 1, y + 2, x + 1, y + 4, r, g, b)
            self.line(x, y, x + 2, y, r, g, b)
            self.set_color(x + 2, y + 1, r, g, b)
        elif n == 8:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x, y + 1, r, g, b)
            self.set_color(x + 2, y + 1, r, g, b)
            self.set_color(x + 2, y + 3, r, g, b)
            self.set_color(x, y + 3, r, g, b)
        elif n == 9:
            self.line(x, y, x + 2, y, r, g, b)
            self.line(x, y + 2, x + 2, y + 2, r, g, b)
            self.line(x, y + 4, x + 2, y + 4, r, g, b)
            self.set_color(x, y + 1, r, g, b)
            self.set_color(x + 2, y + 1, r, g, b)
            self.set_color(x + 2, y + 3, r, g, b)

    def rectangle(self, x1, y1, x2, y2, r, g, b):
        """
        Draw a rectangle with it's corners at x1:y1 and x2:y2

        @type x1: int
        @param x1: the x1 location in the matrix for first corner of the rectangle
        @type y1: int
        @param y1: the y1 location in the matrix for first corner of the rectangle
        @type x2: int
        @param x2: the x2 location in the matrix for second corner of the rectangle
        @type y2: int
        @param y2: the y2 location in the matrix for second corner of the rectangle
        @type r: int
        @param r: red color byte
        @type g: int
        @param g: green color byte
        @type b: int
        @param b: blue color byte
        """

        self.line(x1, y1, x1, y2, r, g, b)
        self.line(x1, y1, x2, y1, r, g, b)
        self.line(x2, y1, x2, y2, r, g, b)
        self.line(x1, y2, x2, y2, r, g, b)

    def line(self, x1, y1, x2, y2, r, g, b):
        """
        Draw a line from x1:y1 and x2:y2

        @type x1: int
        @param x1: the x1 location in the matrix for the start of the line
        @type y1: int
        @param y1: the y1 location in the matrix for the start of the line
        @type x2: int
        @param x2: the x2 location in the matrix for the end of the line
        @type y2: int
        @param y2: the y2 location in the matrix for the end of the line
        @type r: int
        @param r: red color byte
        @type g: int
        @param g: green color byte
        @type b: int
        @param b: blue color byte
        """
        points = []
        is_steep = abs(y2 - y1) > abs(x2 - x1)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        delta_x = x2 - x1
        delta_y = abs(y2 - y1)
        error = int(delta_x / 2)
        y = y1
        y_step = None

        if y1 < y2:
            y_step = 1
        else:
            y_step = -1
        for x in range(x1, x2 + 1):
            if is_steep:
                # print y, "~", x
                self.set_color(y, x, r, g, b)
                points.append((y, x))
            else:
                # print x, " ", y
                self.set_color(x, y, r, g, b)
                points.append((x, y))
            error -= delta_y
            if error < 0:
                y += y_step
                error += delta_x
                # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points

    def clear(self):
        """
        Set all pixels to black in the cached matrix
        """
        for y in range(0, self.rows):
            for x in range(0, self.cols):
                self.set_color(x, y, 0, 0, 0)

    def send_data(self, channel):
        """
        Send data stored in the internal buffer to the channel.

        @param channel:
            - 0 - R pin on BlinkStick Pro board
            - 1 - G pin on BlinkStick Pro board
            - 2 - B pin on BlinkStick Pro board
        """

        start_col = 0
        end_col = 0

        if channel == 0:
            start_col = 0
            end_col = self.r_columns

        if channel == 1:
            start_col = self.r_columns
            end_col = start_col + self.g_columns

        if channel == 2:
            start_col = self.r_columns + self.g_columns
            end_col = start_col + self.b_columns

        self.data[channel] = []

        # slice the huge array to individual packets
        for y in range(0, self.rows):
            start = y * self.cols + start_col
            end = y * self.cols + end_col

            self.data[channel].extend(self.matrix_data[start: end])

        super(BlinkStickProMatrix, self).send_data(channel)
