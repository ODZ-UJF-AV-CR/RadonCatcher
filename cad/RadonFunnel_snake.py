# %%%% 

from build123d import *
from ocp_vscode import *

set_port(3939)


# %%%

pcb_width = 50.5
pcb_hole_width = 10.16*4
pcb_hole_depth = 10.16/2
pcb_depth = 40
funnel_width = 40
funnel_depth = 170
funnel_height = 40
cutout_width = 15
cutout_depth = 170
cutout_height = 5
hole_radius = 39 / 2
hole_depth = 10 * 2
hole_count = 4
taper_top_width = 10
taper_top_depth = 10
taper_height = 30


# Adding a loft from a circle to a rectangle
length = 20
width = 30
thickness = 10

class LoftPart(BuildPart):
    def __init__(self, length, width, mode=Mode.ADD):
        super().__init__()
        self.length = length
        self.width = width
        self.mode = mode
        self.part = self._create_loft_part()

    def _create_loft_part(self):
        with BuildPart() as loft_part:
            Box(1, 1, 1)
            with BuildSketch(loft_part.faces().group_by(Axis.Z)[0][0]) as loft_sk1:
                Circle(self.length / 3)
            with BuildSketch(loft_sk1.faces()[0].offset(self.length / 2)) as loft_sk2:
                Rectangle(self.length / 6, self.width / 6)
            loft(mode=self.mode)
        return loft_part.part

    def subtract(self, target):
        target -= self.part

    def add(self, target):
        target += self.part


# %%%


with BuildPart(Plane.XZ) as loft_part:
    Box(2, 2, 2)
    with BuildSketch(loft_part.faces().group_by(Axis.Y)[0][0]) as loft_sk1:
        Circle(hole_radius)
    with BuildSketch(loft_part.faces().group_by(Axis.Y)[0][0].offset(20)) as loft_sk2:
        with Locations((0, 10)):
            Rectangle(5, funnel_depth / 6)
            
    loft()

show(loft_part.part, reset_camera=Camera.KEEP)


# %%%

with BuildPart() as funnel:
    # Main funnel body
    outer_box = Box(funnel_width, funnel_depth, funnel_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with Locations((-3, -2, cutout_height / 2)):
        Box(cutout_width, 40, cutout_height, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    with Locations((0, 0, funnel_width/2)):
        with PolarLocations(funnel_depth/2, 2, start_angle=90):
            #Cylinder(hole_radius, hole_depth, mode=Mode.SUBTRACT, rotation=(0, -90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER))

            rotace_do_xz = Rotation((0, 90, 0))
            with Locations( rotace_do_xz ):
                with GridLocations(32, 32, 2, 2, align=(Align.CENTER, Align.CENTER, Align.CENTER)):
                    Cylinder(4/2, 20, mode=Mode.SUBTRACT, rotation=(0, 0, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER))

    for face in [0, -1]:
        with BuildPart(outer_box.faces().sort_by(Axis.Y)[face].offset(0), mode=Mode.SUBTRACT) as loft_part:
            Box(1, 1, 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with BuildSketch(loft_part.faces().group_by(Axis.Y)[0][0]) as loft_sk1:
                Circle(hole_radius)
            with BuildSketch(loft_part.faces().group_by(Axis.Y)[0][0].offset(-70 if face == 0 else 70)) as loft_sk2:
                with Locations((-14.5, 3.5)):
                    Rectangle(4, 16)
            loft(mode=Mode.ADD)
    

    with BuildPart():
        line_length = 2
        line_spacing = 11
        num_pairs = 10
        arc_radius = line_spacing / 2

        # Create a rectangular profile with rounded corners
        rect_width = 7
        rect_height = 80
        corner_radius = 0.5

        with BuildPart() as meandr:
            segments = []
            for i in range(num_pairs):
                y1 = i * 2 * line_spacing - (num_pairs * line_spacing)
                y2 = y1 + line_spacing

                segments.append(Line((-line_length / 2, y1), (line_length / 2, y1)))
                segments.append(Line((-line_length / 2, y2), (line_length / 2, y2)))

                arc = RadiusArc((line_length / 2, y2), (line_length / 2, y1), arc_radius)
                segments.append(arc)
                arc = RadiusArc((-line_length / 2, y1 + line_spacing), (-line_length / 2, y2 + line_spacing), arc_radius)
                segments.append(arc)

            lines_curve = Curve() + tuple(segments)

            with Locations((0, 44, 0), (0, -44, 0)):
                Box(40, 50, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with BuildPart(mode=Mode.SUBTRACT) as extruded_profile:
                with BuildSketch(Plane.YZ) as rounded_rectangle:
                    Rectangle(rect_width, rect_height, align=(Align.CENTER, Align.CENTER))
                    Circle(corner_radius, mode=Mode.SUBTRACT)
                sweep(path=lines_curve)

    with Locations((0, 0, 0)):
        with Locations((10, 0, 0)):
            with Locations((-pcb_hole_depth, -pcb_hole_width/2, 1.6), (-pcb_hole_depth, pcb_hole_width/2, 1.6)):
                Cylinder(3, 9, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.ADD)
                Cylinder(1.2, 8, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with Locations((0, 0, 0)):
        with Locations((10, 0, 0)):
            Box(50, pcb_width, 1.6, mode=Mode.SUBTRACT, align=(Align.MAX, Align.CENTER, Align.MIN))
            with Locations((-13, 2, 1.6)):
                Box(15, 27, 4, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

            # with Locations((-pcb_hole_depth, -pcb_hole_width/2, 1.6), (-pcb_hole_depth, pcb_hole_width/2, 1.6)):
            #     Cylinder(4, 10, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.ADD)
            #     Cylinder(1.2, 8, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

show (funnel, reset_camera=Camera.KEEP)
# %%%


with BuildSketch() as parallel_lines_with_arcs:


show(meandr, funnel, reset_camera=Camera.KEEP)
# %%%


export_stl(funnel.part, "funnel.stl")
# %%%



with BuildPart() as end:
    outer_data = Box(funnel_width, 25, 90, align=(Align.CENTER, Align.CENTER, Align.CENTER))

    with BuildPart(outer_data.faces().sort_by(Axis.Y)[-1], mode=Mode.SUBTRACT) as mounting_holes:
        with GridLocations(32, 32, 2, 2, align=(Align.CENTER, Align.CENTER, Align.CENTER)):
            Cylinder(3.5/2, 100, mode=Mode.ADD, rotation=(0, 0, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER))
        Cylinder(38/2-2, 40, mode=Mode.ADD, rotation=(0, 0, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER))
    
    with Locations((0, 0, 0)):
        Box(25, 5, 80, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

    with Locations((0, 10, 32), (0, 10, -32)):
        Box(25, 20, 20, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

show(end.part, reset_camera=Camera.KEEP)

export_stl(end.part, "end.stl")