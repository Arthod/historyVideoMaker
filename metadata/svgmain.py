import cairosvg

# read svg file -> write png file
cairosvg.svg2png(url="out.svg", write_to="out2.png", output_width=32766, output_height=16384)