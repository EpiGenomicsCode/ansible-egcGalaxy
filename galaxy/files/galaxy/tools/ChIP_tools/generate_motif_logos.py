import numpy as np
import re
import xml.dom.minidom as dom
import gzip
import os
import argparse

def is_gz_file(filepath):
    """
    Check first byte of file to see if it is gzipped
    """
    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'

def openfile(filepath, mode='r'):
    if is_gz_file(filepath):
        return gzip.open(filepath, mode)
    return open(filepath, mode)

class DNASymbol:
    path = None
    color = None
    max_bits = 2
    DNA_alphabet = ()

    @classmethod
    def get_symbol(cls, i):
        return cls.DNA_alphabet[i]

class DNA_A(DNASymbol):
    path = 'M 0 100 L 33 0 L 66 0 L 100 100 L 75 100 L 66 75 L 33 75 L 25 100 L 0 100 M 41 55 L 58 55 L 50 25 L 41 55'
    color = '#FF0000'

class DNA_C(DNASymbol):
    path = 'M 100 28 C 100 -13 0 -13 0 50 C 0 113 100 113 100 72 L 75 72 C 75 90 30 90 30 50 C 30 10 75 10 75 28 Z'
    color = '#0000FF'

class DNA_G(DNASymbol):
    path = 'M 100 28 C 100 -13 0 -13 0 50 C 0 113 100 113 100 72 L 100 48 L 55 48 L 55 72 L 75 72 C 75 90 30 90 30 50 C 30 10 75 5 75 28 Z'
    color = '#FFA500'

class DNA_T(DNASymbol):
    path = 'M 0 0 L 0 20 L 35 20 L 35 100 L 65 100 L 65 20 L 100 20 L 100 0 Z'
    color = '#228B22'

DNASymbol.DNA_alphabet = (DNA_A, DNA_C, DNA_G, DNA_T)

def pwm2logo(pwm, out_fn, symbol=DNASymbol, glyph_width=100, stack_height=200):
    width = len(pwm)

    document = dom.Document()
    svg = document.appendChild(document.createElement('svg'))
    svg.setAttribute('baseProfile', 'full')
    svg.setAttribute('version', '1.1')
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    svg.setAttribute('viewBox', '{} 0 {} {}'.format(-50, width * glyph_width + 50, stack_height + 25))
    svg.setAttribute('font-family', 'Helvetica')

    defs = svg.appendChild(document.createElement('defs'))
    for base in symbol.DNA_alphabet:
        path = defs.appendChild(document.createElement('path'))
        path.setAttribute('id', base.__name__)
        path.setAttribute('d', base.path)
        path.setAttribute('fill', base.color)

    left_axis = svg.appendChild(document.createElement('g'))
    left_axis_line = left_axis.appendChild(document.createElement('line'))
    left_axis_line.setAttribute('x1', '-2')
    left_axis_line.setAttribute('x2', '-2')
    left_axis_line.setAttribute('y1', '0')
    left_axis_line.setAttribute('y2', str(stack_height))
    left_axis_line.setAttribute('stroke', 'black')
    left_axis_line.setAttribute('stroke-width', '1')
    for i in range(symbol.max_bits + 1):
        left_axis_tick = left_axis.appendChild(document.createElement('line'))
        left_axis_tick.setAttribute('x1', '-7')
        left_axis_tick.setAttribute('x2', '-2')
        left_axis_tick.setAttribute('y1', str(stack_height * i / symbol.max_bits))
        left_axis_tick.setAttribute('y2', str(stack_height * i / symbol.max_bits))
        left_axis_tick.setAttribute('stroke', 'black')
        left_axis_tick.setAttribute('stroke-width', '1')
        left_axis_tick_label = left_axis.appendChild(document.createElement('text'))
        left_axis_tick_label.setAttribute('x', '-10')
        left_axis_tick_label.setAttribute('y', str(stack_height * i / symbol.max_bits + 5))
        left_axis_tick_label.setAttribute('text-anchor', 'end')
        left_axis_tick_label.setAttribute('font-size', '20')
        left_axis_tick_label.appendChild(document.createTextNode(str(i)))
    left_axis_label = left_axis.appendChild(document.createElement('text'))
    left_axis_label.setAttribute('x', '-25')
    left_axis_label.setAttribute('y', str(stack_height / 2))
    left_axis_label.setAttribute('text-anchor', 'middle')
    left_axis_label.setAttribute('font-size', '20')
    left_axis_label.setAttribute('transform', 'rotate(-90 -25 {})'.format(stack_height / 2))
    left_axis_label.appendChild(document.createTextNode('bits'))

    for i, pwv in enumerate(pwm):
        n = np.sum(pwv)
        if n == 0:
            continue
        vec = pwv / n
        vec[vec > 0] *= np.log2(vec[vec > 0])
        bits = sum(vec, symbol.max_bits)
        heights = pwv / n * bits / symbol.max_bits * stack_height
        idx = np.argsort(pwv)

        stack = svg.appendChild(document.createElement('g'))
        stack.setAttribute('transform', 'translate({} 0)'.format(i * glyph_width))
        bottom_tick_label = stack.appendChild(document.createElement('text'))
        bottom_tick_label.setAttribute('x', str(glyph_width / 2))
        bottom_tick_label.setAttribute('y', str(stack_height + 25))
        bottom_tick_label.setAttribute('text-anchor', 'middle')
        bottom_tick_label.setAttribute('font-size', '20')
        bottom_tick_label.appendChild(document.createTextNode(str(i + 1)))

        y_offset = 0
        for j in idx:
            base = symbol.get_symbol(j)
            y_offset += heights[j]
            glyph = stack.appendChild(document.createElement('use'))
            glyph.setAttribute('href', '#{}'.format(base.__name__))
            glyph.setAttribute('transform', 'matrix({} 0 0 {} 0 {})'.format(glyph_width / 100., heights[j] / 100., stack_height - y_offset))

    with open(out_fn, 'w') as f:
        svg.writexml(f, addindent='    ', newl='\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('meme_fn', help='MEME file')
    args = parser.parse_args()

    pattern = re.compile(r'letter-probability matrix')
    n = 1
    with openfile(args.meme_fn, 'rt') as f:
        for line in f:
            if pattern.match(line):
                pwm = []
                for line in f:
                    if not re.match(r'\d', line.strip()):
                        break
                    pwm.append(list(map(float, line.split())))
                pwm2logo(np.array(pwm), 'MEME-{}_forward.svg'.format(n))
                pwm2logo(np.flip(np.array(pwm)), 'MEME-{}_reverse.svg'.format(n))
                n += 1
