from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QColorDialog, QFileDialog,QLineEdit
from PyQt5.QtGui import QColor, QPixmap,QIntValidator
import os
import math
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        self.color1 = QColor(213, 211, 214)
        self.color2 = QColor(109, 125, 137)

        self.width = 150
        self.height = 800
        self.stroke_width = 2
        self.font_path = 'D:\字体\HarmonyOS_Sans\HarmonyOS_Sans_SC_Regular.ttf'
        self.font_size = 40

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        color1_label = QLabel('左边的颜色:')
        self.color1_button = QPushButton()
        self.color1_button.clicked.connect(self.choose_color1)
        self.update_color1_button()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(color1_label)
        hbox1.addWidget(self.color1_button)

        color2_label = QLabel('右边的颜色:')
        self.color2_button = QPushButton()
        self.color2_button.clicked.connect(self.choose_color2)
        self.update_color2_button()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(color2_label)
        hbox2.addWidget(self.color2_button)

        width_label = QLabel('矩形宽度:')
        self.width_edit = QLineEdit()
        self.width_edit.setValidator(QIntValidator())
        self.width_edit.setText(str(self.width))
        self.width_edit.textChanged.connect(self.update_width)

        height_label = QLabel('矩形高度:')
        self.height_edit = QLineEdit()
        self.height_edit.setValidator(QIntValidator())
        self.height_edit.setText(str(self.height))
        self.height_edit.textChanged.connect(self.update_height)

        stroke_width_label = QLabel('描边宽度:')
        self.stroke_width_edit = QLineEdit()
        self.stroke_width_edit.setValidator(QIntValidator())
        self.stroke_width_edit.setText(str(self.stroke_width))
        self.stroke_width_edit.textChanged.connect(self.update_stroke_width)

        font_path_label = QLabel('字体路径:')
        self.font_path_edit = QLineEdit()
        self.font_path_edit.setText(self.font_path)
        self.font_path_edit.textChanged.connect(self.update_font_path)
        self.font_path_button = QPushButton('选择')
        self.font_path_button.clicked.connect(self.choose_font_path)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(font_path_label)
        hbox3.addWidget(self.font_path_edit)
        hbox3.addWidget(self.font_path_button)

        font_size_label = QLabel('字体大小:')
        self.font_size_edit = QLineEdit()
        self.font_size_edit.setValidator(QIntValidator())
        self.font_size_edit.setText(str(self.font_size))
        self.font_size_edit.textChanged.connect(self.update_font_size)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(width_label)
        hbox4.addWidget(self.width_edit)
        hbox4.addWidget(height_label)
        hbox4.addWidget(self.height_edit)
        hbox4.addWidget(stroke_width_label)
        hbox4.addWidget(self.stroke_width_edit)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(font_size_label)
        hbox5.addWidget(self.font_size_edit)

        save_path_label = QLabel('保存路径:')
        self.save_path_edit = QLineEdit()
        self.save_path_edit.setReadOnly(True)
        self.save_path_button = QPushButton('浏览')
        self.save_path_button.clicked.connect(self.choose_save_path)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(save_path_label)
        hbox6.addWidget(self.save_path_edit)
        hbox6.addWidget(self.save_path_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox6)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.update_preview()

        vbox.addWidget(self.preview_label)

        self.setLayout(vbox)

    def choose_color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color1 = color
            self.update_color1_button()
            self.update_preview()

    def update_color1_button(self):
        color_name = get_color_name(self.color1.getRgb())
        self.color1_button.setText('{} - {}'.format(color_name, self.color1.name()))

    def choose_color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color2 = color
            self.update_color2_button()
            self.update_preview()

    def update_color2_button(self):
        color_name = get_color_name(self.color2.getRgb())
        self.color2_button.setText('{} - {}'.format(color_name, self.color2.name()))

    def update_width(self, text):
        if text:
            self.width = int(text)
            self.update_preview()

    def update_height(self, text):
        if text:
            self.height = int(text)
            self.update_preview()

        color1_label = QLabel('右边的颜色:')
        self.color1_button = QPushButton()
        self.color1_button.clicked.connect(self.choose_color1)
        self.update_color1_button()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(color1_label)
        hbox1.addWidget(self.color1_button)


        color2_label = QLabel('右边的颜色:')
        self.color2_button = QPushButton()
        self.color2_button.clicked.connect(self.choose_color2)
        self.update_color2_button()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(color2_label)
        hbox2.addWidget(self.color2_button)

        save_label = QLabel('保存路径:')
        self.save_path_label = QLabel()
        self.save_button = QPushButton('选择保存路径')
        self.save_button.clicked.connect(self.choose_save_path)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(save_label)
        hbox3.addWidget(self.save_path_label)
        hbox3.addWidget(self.save_button)

        generate_button = QPushButton('生成图片')
        generate_button.clicked.connect(self.generate_image)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(generate_button)

        self.setLayout(vbox)


    def choose_color1(self):
        color = QColorDialog.getColor(self.color1, self, '选择左边的颜色')
        if color.isValid():
            self.color1 = color
            self.update_color1_button()

    def update_color1_button(self):
        self.color1_button.setStyleSheet('QPushButton {background-color: %s;}' % self.color1.name())

    def choose_color2(self):
        color = QColorDialog.getColor(self.color2, self, '选择右边的颜色')
        if color.isValid():
            self.color2 = color
            self.update_color2_button()

    def update_color2_button(self):
        self.color2_button.setStyleSheet('QPushButton {background-color: %s;}' % self.color2.name())

    def choose_save_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "选择保存路径", "", "Images (*.png);;All Files (*)", options=options)
        if save_path:
            self.save_path_label.setText(save_path)

    def generate_image(self):
        if not self.save_path_label.text():
            print("请先选择保存路径")
            return

        rgb1 = self.color1.red(), self.color1.green(), self.color1.blue()
        rgb2 = self.color2.red(), self.color2.green(), self.color2.blue()

        unified_draw_rectangles(self.width, self.height, rgb1, rgb2, self.stroke_width, self.font_path, self.font_size, self.save_path_label.text())

        pixmap = QPixmap(self.save_path_label.text())
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        preview_label = QLabel()
        preview_label.setPixmap(pixmap)
        preview_label.setWindowTitle('预览')
        preview_label.show()

def color_en2zh(color):
    color_map = {
        # 先定义一个中英文颜名称映射表
    'black': '黑',
    'navy': '海军蓝',
    'darkblue': '深蓝',
    'mediumblue': '中蓝',
    'blue': '蓝',
    'darkgreen': '深绿',
    'green': '绿',
    'teal': '青',
    'darkcyan': '深青',
    'deepskyblue': '深天蓝',
    'darkturquoise': '深宝石绿',
    'mediumspringgreen': '中春绿',
    'lime': '绿黄',
    'springgreen': '春绿',
    'aqua': '水蓝',
    'cyan': '青',
    'midnightblue': '暗蓝',
    'dodgerblue': '闪蓝',
    'lightseagreen': '浅海洋绿',
    'forestgreen': '森林绿',
    'seagreen': '海洋绿',
    'darkslategray': '深石板灰',
    'limegreen': '青柠绿',
    'mediumseagreen': '中海洋绿',
    'turquoise': '宝石绿',
    'royalblue': '皇家蓝',
    'steelblue': '钢蓝',
    'darkslateblue': '深岩蓝',
    'mediumturquoise': '中宝石绿',
    'indigo': '靛蓝',
    'darkolivegreen': '深橄榄绿',
    'cadetblue': '军校蓝',
    'cornflowerblue': '矢车菊蓝',
    'rebeccapurple': '丽贝卡紫',
    'mediumaquamarine': '中绿松石',
    'dimgray': '暗灰',
    'slateblue': '灰石',
    'olivedrab': '橄榄褐',
    'slategray': '石板灰',
    'lightslategray': '亮石板灰',
    'mediumslateblue': '中型岩蓝',
    'lawngreen': '草坪绿',
    'chartreuse': '查特酒绿',
    'aquamarine': '绿松石',
    'maroon': '栗',
    'purple': '紫',
    'olive': '橄榄',
    'gray': '灰',
    'skyblue': '天蓝',
    'lightskyblue': '亮天蓝',
    'blueviolet': '蓝紫',
    'darkred': '深红',
    'darkmagenta': '深品红',
    'saddlebrown': '马鞍棕',
    'darkseagreen': '深海洋绿',
    'lightgreen': '浅绿',
    'mediumpurple': '中紫',
    'darkviolet': '深紫罗兰',
    'palegreen': '苍绿',
    'darkorchid': '深兰花紫',
    'yellowgreen': '黄绿',
    'sienna': '赭',
    'brown': '棕',
    'darkgray': '深灰',
    'lightblue': '浅蓝',
    'greenyellow': '黄绿',
    'paleturquoise': '苍宝石绿',
    'lightsteelblue': '亮钢蓝',
    'powderblue': '火药蓝',
    'firebrick': '砖红',
    'darkgoldenrod': '深金黄',
    'mediumorchid': '中兰花紫',
    'rosybrown': '玫瑰棕',
    'darkkhaki': '深卡其',
    'silver': '银白',
    'mediumvioletred': '中洋红',
    'indianred': '印度红',
    'peru': '秘鲁',
    'chocolate': '巧克力',
    'tan': '棕褐',
    'lightgray': '浅灰',
    'thistle': '蓟',
    'orchid': '兰花紫',
    'goldenrod': '金黄',
    'palevioletred': '紫罗兰红',
    'crimson': '绯红',
    'gainsboro': '亮灰',
    'plum': '洋李',
    'burlywood': '硬木',
    'lightcyan': '浅青',
    'lavender': '淡紫',
    'darksalmon': '深橙红',
    'violet': '紫罗兰',
    'palegoldenrod': '苍金黄',
    'lightcoral': '浅珊瑚',
    'khaki': '卡其',
    'aliceblue': '爱丽丝蓝',
    'honeydew': '蜜瓜',
    'azure': '浅天蓝',
    'sandybrown': '沙棕',
    'wheat': '小麦',
    'beige': '米',
    'whitesmoke': '烟白',
    'mintcream': '薄荷乳白',
    'ghostwhite': '幽灵白',
    'salmon': '橙红',
    'antiquewhite': '古董白',
    'linen': '亚麻',
    'lightgoldenrodyellow': '亮金黄',
    'oldlace': '老花',
    'red': '红',
    'fuchsia': '紫红',
    'magenta': '品红',
    'deeppink': '深粉',
    'orangered': '橙红',
    'tomato': '番茄',
    'hotpink': '热粉红',
    'coral': '珊瑚',
    'darkorange': '深橙',
    'lightsalmon': '亮橙红',
    'orange': '橙',
    'lightpink': '浅粉',
    'pink': '粉红',
    'gold': '金',
    'peachpuff': '桃',
    'navajowhite': '纳瓦霍白',
    'moccasin': '鹿皮',
    'bisque': '陶坯黄',
    'mistyrose': '浅玫瑰',
    'blanchedalmond': '杏仁白',
    'papayawhip': '西瓜',
    'lavenderblush': '淡紫红',
    'seashell': '贝壳',
    'cornsilk': '玉米穗黄',
    'lemonchiffon': '柠檬绸',
    'floralwhite': '花白',
    'snow': '雪白',
    'yellow': '黄',
    'lightyellow': '浅黄',
    'ivory': '象牙白',
    'white': '白',
        }
    return color_map.get(color, color)

def get_color_name(rgb):
    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
    try:
        closest_name = CSS3_NAMES_TO_HEX[hex_color].lower()
        return color_en2zh(closest_name)
    except KeyError:
        pass

    # 如果找不到准确的颜色，则使用欧几里得距离计算最接近的颜色
    def color_distance(c1, c2):
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    min_distance = float("inf")
    min_color = None
    for name, value in CSS3_NAMES_TO_HEX.items():
        distance = color_distance(rgb, hex_to_rgb(value))
        if distance < min_distance:
            min_distance = distance
            min_color = name

    return color_en2zh(min_color.lower())

def draw_rect(color1, color2, width, height):
    img = Image.new('RGB', (2*width, height))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width, height), fill=color1)
    draw.rectangle((width, 0, 2*width, height), fill=color2)
    img.show()

def draw_rectangles(width, height, color1, color2, stroke_width=4, font_path='arial.ttf', font_size=20, save_path=None):
    image_width = width * 2
    image_height = height

    image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(image)

    # 绘制左侧矩形
    left_rect = (0, 0, width, height)
    draw.rectangle(left_rect, fill=color1)

    # 绘制右侧矩形
    right_rect = (width, 0, image_width, height)
    draw.rectangle(right_rect, fill=color2)

    # 绘制两个圆
    radius = height // 16 * 2
    center1 = (width, height * 5 // 16)
    center2 = (width, height * 11 // 16)

    # 添加白色描边
    draw.ellipse((center1[0] - radius - stroke_width, center1[1] - radius - stroke_width, 
                  center1[0] + radius + stroke_width, center1[1] + radius + stroke_width), fill='white')
    draw.ellipse((center2[0] - radius - stroke_width, center2[1] - radius - stroke_width, 
                  center2[0] + radius + stroke_width, center2[1] + radius + stroke_width), fill='white')

    # 绘制原来的圆形
    draw.ellipse((center1[0] - radius, center1[1] - radius, 
                  center1[0] + radius, center1[1] + radius), fill=color1)
    draw.ellipse((center2[0] - radius, center2[1] - radius, 
                  center2[0] + radius, center2[1] + radius), fill=color2)

    # 绘制文字
    font = ImageFont.truetype(font_path, font_size)
    color_name1 = get_color_name(color1)
    color_name2 = get_color_name(color2)

    text_width1, text_height1 = draw.textsize(color_name1, font=font)
    text_width2, text_height2 = draw.textsize(color_name2, font=font)

    draw.text((center1[0] - text_width1 // 2, center1[1] - text_height1 // 2), 
              color_name1, font=font, fill=color2)
    draw.text((center2[0] - text_width2 // 2, center2[1] - text_height2 // 2), 
              color_name2, font=font, fill=color1)

    if save_path:
        image.save(save_path)
    else:
        image.show()


def unified_draw_rectangles(width, height, rgb1, rgb2, stroke_width=4, font_path="arial.ttf", font_size=20, save_path=None):
    draw_rectangles(width, height, rgb1, rgb2, stroke_width, font_path, font_size, save_path)

# # 示例调用
# save_path = 'G:\\小红书\\1688源运\\04.png'
# unified_draw_rectangles(150, 800, (213, 211, 214), (109, 125, 137), stroke_width=2, font_path="D:\字体\HarmonyOS_Sans\HarmonyOS_Sans_SC_Regular.ttf", font_size=40, save_path=save_path)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    color_picker = ColorPicker()
    color_picker.show()

    sys.exit(app.exec_())
