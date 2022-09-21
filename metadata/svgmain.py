import cairosvg

# read svg file -> write png file
cairosvg.svg2png(url="water.svg", write_to="out.png", output_width=16384, output_height=8192)