# Manage PPT Files


# Return an integer value out of a given value.
def parseInt(ss):
    safe = ''
    for s in ss:
        if s.isdigit() or s == '.' or s == '-':
            safe = safe + s
    
    return int(round(float(safe)))


# Remove all newlines and odd characters from a string
def prettyString(s):
    
    # remove linebreaks
    s = s.replace('\r', '').replace('\n', '')
    
    # tabs
    s = s.replace('\t', ' ')

    # remove double spaces
    i = len(s)
    s = s.replace('  ', ' ')
    
    while len(s) < i:
        i = len(s)
        s = s.replace('  ', ' ')

    # trim
    return s.strip()


class ScaledPage():

    def __init__(self, pptHtmlPage, WIDTH):
        self.WIDTH = WIDTH
        self.RATIO = 0.0
        self.HEIGHT = 0  # set in set_jpg, as we don't know aspect ratio yet.

        self.page = pptHtmlPage
        self.title = pptHtmlPage.title
        self.order = pptHtmlPage.order
        self.set_jpg()
        self.set_src()
        self.set_text()
        self.set_points()

    def set_points(self):
        self.points = []
        for point in self.page.ppthtmlpagepoint_set.order_by('order').all():
            self.points.append(point.text)

    def set_jpg(self):

        if self.page.pptjpg_id is None:
            self.jpg = None
            return

        jpg = self.page.pptjpg
        self.RATIO = (1.0 * self.WIDTH) / jpg.width
        self.HEIGHT = self.RATIO * jpg.height
        
        self.jpg = {
            'src': jpg.get_absolute_url(),
            'height': self.HEIGHT,
            'width': self.WIDTH,
        }

    # Convert images to a nice format. Note that measurements are by %.
    def set_src(self):
        self.srcs = []
        for src in self.page.ppthtmlpagesrc_set.all():
            self.srcs.append({
                'src': src.get_absolute_url(),
                'height': int(src.pos_height * self.HEIGHT / 100),
                'width': int(src.pos_width * self.WIDTH / 100),
                'left': int(src.pos_left * self.WIDTH / 100),
                'top': int(src.pos_top * self.HEIGHT / 100),
                'template': src.ppthtmlimage.template,
            })

    # Convert texts into a nice format. Note that measurements are by %
    def set_text(self):
        self.texts = []

        for text in self.page.ppthtmlpagetext_set.all():
            self.texts.append({
                'text': text.text,
                'height': int(text.pos_height * self.HEIGHT / 100),
                'width': int(text.pos_width * self.WIDTH / 100),
                'left': int(text.pos_left * self.WIDTH / 100),
                'top': int(text.pos_top * self.HEIGHT / 100),
            })
