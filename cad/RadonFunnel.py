# %%%% 

from build123d import *
from ocp_vscode import show, set_port

set_port(3939)


# %%%
pcb_width = 60
pcb_depth = 40
funnel_width = 50
funnel_depth = 150
funnel_height = 50
cutout_width = 15
cutout_depth = 150
cutout_height = 10
hole_radius = 45 / 2
hole_depth = 10 * 2
hole_count = 4
taper_top_width = 10
taper_top_depth = 10
taper_height = 30

# with BuildPart() as funnel:
#     # Main funnel body
#     Box(funnel_width, funnel_depth, funnel_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

#     # Cutout in the funnel - základní obdélníkový průřez
#     with Locations((0, 0, cutout_height / 2)):
#         Box(cutout_width, cutout_depth, cutout_height, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)


# %%% 

with BuildSketch() as parallel_lines_with_arcs:
    line_length = 30
    line_spacing = 7
    num_pairs = 10
    arc_radius = line_spacing / 2

    segments = []
    for i in range(num_pairs):
        y1 = i * 2 * line_spacing
        y2 = y1 + line_spacing

        # První přímka v páru (spodní)
        segments.append(Line((0, y1), (line_length, y1)))
        # Druhá přímka v páru (horní)
        segments.append(Line((0, y2), (line_length, y2)))

        # Půlkružnice mezi konci přímek
        # Spojení vpravo, oblouk směrem dolů (z horní na spodní)
        arc = RadiusArc((line_length, y2), (line_length, y1), arc_radius)
        segments.append(arc)
        arc = RadiusArc((0, y1 + line_spacing), (0, y2 + line_spacing), arc_radius)
        segments.append(arc)

    lines_curve = Curve() + tuple(segments)

show(lines_curve)
# %%


