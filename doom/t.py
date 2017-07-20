from PIL import Image

bar = Image.open('STBAR.png').convert('RGBA')

nine = Image.open('STTNUM9.png').convert('RGBA')

bar.paste(nine, (500, 24), nine)
bar.save('test.png')

