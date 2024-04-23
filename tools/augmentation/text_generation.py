import json
import random
import re
import string
import os
import tqdm
from PIL import Image, ImageFont, ImageDraw

from pnid_recognition_project.common.vector2 import Vector2
from pnid_recognition_project.common.xml_data import XMLData
from pnid_recognition_project.common.symbol_object import SymbolObject

class TextGenerator:
    def __init__(self, patterns):
        self.patterns = patterns

    def load_pattern_json(self, path, flatten_prob=True):
        with open(path, 'r') as f:
            loaded_patterns = json.load(f)
            if flatten_prob:
                loaded_patterns = self._flatten_pattern_prob(loaded_patterns)

        self.patterns = loaded_patterns

    def _flatten_pattern_prob(self, patterns):
        max_num_pattern = 0
        for char in patterns:
            num_pattern = len(patterns[char])
            if num_pattern > max_num_pattern:
                max_num_pattern = num_pattern

        uniform_patterns = []
        for char in patterns:
            num_pattern = len(patterns[char])
            if num_pattern == 0:
                continue

            if num_pattern < max_num_pattern:
                uniform_patterns.extend([random.choice(patterns[char]) for i in range(max_num_pattern)])
            else:
                uniform_patterns.extend(patterns[char])

        return uniform_patterns

    def _random_upper(self, match):
        return random.choice(string.ascii_uppercase)

    def _random_lower(self, match):
        return random.choice(string.ascii_lowercase)

    def _random_number(self, match):
        return random.choice(string.digits)

    def _randomize_characters(self, pattern):
        line = re.sub(r'c', self._random_lower, pattern)
        line = re.sub(r'C', self._random_upper, line)
        line = re.sub(r'n', self._random_number, line)

        return line

    def generate_uniform_pil(self, options):
        count = options['count']
        font_sizes = options['font_sizes']
        padding = options['padding']
        canvas_size = options['canvas_size']
        margin = options['margin']
        out_dir = options['out_dir']

        if not self.patterns:
            print('Patterns are not set!')
            return

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        indices = [random.choice(range(len(self.patterns))) for i in range(count)]
        sampled_patterns = [self.patterns[i] for i in indices]
        pattern_texts = [self._randomize_characters(s) for s in sampled_patterns]

        image_fonts = [ImageFont.truetype('./arial.ttf', size=s) for s in font_sizes]

        img_count = 0
        canvas_x = padding[0]
        canvas_y = padding[1]
        nextline_y = 0
        canvas = Image.new("RGB", canvas_size, (255,255,255))
        txt_draw = ImageDraw.Draw(canvas)
        xml_data = XMLData()

        for text in tqdm.tqdm(pattern_texts):
            image_font = random.choice(image_fonts)
            width = image_font.getlength(text)
            _, top, _, bottom = image_font.getbbox(text)
            width = int(width)
            height = int(bottom - top)
            nextline_y = max(nextline_y, height)

            if canvas_x + width > canvas_size[1] - padding[0]: # to next row
                canvas_x = padding[0]
                canvas_y += (nextline_y + margin[1])
                nextline_y = 0

                if canvas_y + height > canvas_size[0] - padding[1]:  # canvas is full
                    # save img
                    canvas.save(os.path.join(out_dir, f'AugText_{img_count:05d}.png'))
                    # save xml
                    xml_data.write_xml(os.path.join(out_dir, f'AugText_{img_count:05d}.xml'))

                    canvas = Image.new("RGB", canvas_size, (255, 255, 255))
                    xml_data = XMLData()

                    txt_draw = ImageDraw.Draw(canvas)
                    img_count += 1

                    canvas_x = padding[0]
                    canvas_y = padding[1]
                    nextline_y = 0

            txt_draw.text((canvas_x, canvas_y), text, font=image_font, fill=(0, 0, 0), anchor="lt")
            symbol_object = SymbolObject.from_twopoint('text', text, Vector2(canvas_x, canvas_y),
                                                       Vector2(canvas_x, canvas_y) + Vector2(width, height),
                                                       0, False, False)
            xml_data.symbol_object_list.append(symbol_object)

            canvas_x += (width + margin[0])

        # log options
        with open(os.path.join(out_dir, 'options.json'), 'w') as f:
            json.dump(options, f, indent=4)


if __name__ == '__main__':
    options = {
        'pattern_json_path': '/home/diskhkme/Dev/PNID/pnid_recognition_project/tests/output/special_char_pattern.json',
        'canvas_size': (800, 800),
        'count': 1000,
        'out_dir': '/home/diskhkme/Dev/PNID/dataset/text_augmentation_test/dataset',
        'font_sizes': [28,32,36],
        'margin': (40, 20), # x,y margin
        'padding': (50, 50),
    }

    text_gen = TextGenerator(None)
    text_gen.load_pattern_json(options['pattern_json_path'], True)
    text_gen.generate_uniform_pil(options)


