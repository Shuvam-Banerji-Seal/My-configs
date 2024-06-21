from manim import *

# Set the aspect ratio to 16:9 and video quality to 4K
#config.frame_height = 1080
#config.frame_width = 1920
#config.quality = "4k_quality"

class KochCurve(VMobject):
    def __init__(self, order=4, **kwargs):
        super().__init__(**kwargs)
        self.order = order
        self.start_points = [
            np.array([-3, 0, 0]),
            np.array([3, 0, 0]),
        ]
        self.generate_curve()

    def generate_curve(self):
        points = self.start_points
        for _ in range(self.order):
            points = self.iterate(points)
        self.set_points_as_corners(points)

    def iterate(self, points):
        new_points = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i+1]
            segment = p2 - p1
            new_points.append(p1)
            new_points.append(p1 + segment / 3)
            new_points.append(p1 + segment / 3 + self.rotate_60_deg(segment / 3))
            new_points.append(p1 + 2 * segment / 3)
        new_points.append(points[-1])
        return new_points

    def rotate_60_deg(self, vector):
        rotation_matrix = np.array([
            [0.5, -np.sqrt(3) / 2, 0],
            [np.sqrt(3) / 2, 0.5, 0],
            [0, 0, 1],
        ])
        return np.dot(rotation_matrix, vector)

class KochSnowflake(VMobject):
    def __init__(self, order=4, **kwargs):
        super().__init__(**kwargs)
        self.order = order
        self.start_points = self.create_initial_triangle()
        self.generate_snowflake()

    def create_initial_triangle(self):
        return [
            np.array([0, 2 * np.sqrt(3), 0]),
            np.array([-3, 0, 0]),
            np.array([3, 0, 0]),
            np.array([0, 2 * np.sqrt(3), 0]),
        ]

    def generate_snowflake(self):
        points = self.start_points
        for _ in range(self.order):
            new_points = []
            for i in range(len(points) - 1):
                new_points.extend(self.iterate(points[i], points[i+1]))
            new_points.append(points[-1])
            points = new_points
        self.set_points_as_corners(points)

    def iterate(self, p1, p2):
        segment = p2 - p1
        return [
            p1,
            p1 + segment / 3,
            p1 + segment / 3 + self.rotate_60_deg(segment / 3),
            p1 + 2 * segment / 3,
        ]

    def rotate_60_deg(self, vector):
        rotation_matrix = np.array([
            [0.5, -np.sqrt(3) / 2, 0],
            [np.sqrt(3) / 2, 0.5, 0],
            [0, 0, 1],
        ])
        return np.dot(rotation_matrix, vector)

class KochCurveExplainer(ThreeDScene):
    def construct(self):
        title = Text("Koch Curve and Koch Snowflake").to_edge(UP)
        self.play(Write(title))

        # Explain the Koch Curve
        koch_curve = KochCurve(order=4)
        koch_curve.set_color_by_gradient(BLUE, GREEN, YELLOW, ORANGE, RED)
        curve_label = Text("Koch Curve").next_to(koch_curve, UP)
        
        self.play(Create(koch_curve))
        self.play(Write(curve_label))

        # Add recursive explanation
        explanation_text = Text(
            "The Koch Curve is created by recursively dividing each segment into 3 parts, \n"
            "constructing an equilateral triangle on the middle segment, and removing the base."
        ).scale(0.5).to_edge(DOWN)
        self.play(Write(explanation_text))

        self.wait(3)
        self.play(FadeOut(curve_label), FadeOut(explanation_text))

        # Explain the iterative process in detail
        iteration_text = Text(
            "Iterative Process:\n"
            "1. Divide each segment into three equal parts.\n"
            "2. Construct an equilateral triangle on the middle part.\n"
            "3. Remove the base of the triangle.\n"
            "4. Repeat for each new segment."
        ).scale(0.5).to_edge(DOWN)
        self.play(Write(iteration_text))

        self.wait(3)
        self.play(FadeOut(iteration_text))

        # Explain the Koch Snowflake
        koch_snowflake = KochSnowflake(order=4)
        koch_snowflake.set_color_by_gradient(BLUE, GREEN, YELLOW, ORANGE, RED)
        snowflake_label = Text("Koch Snowflake").next_to(koch_snowflake, UP)
        
        self.play(Transform(koch_curve, koch_snowflake))
        self.play(Write(snowflake_label))

        snowflake_explanation = Text(
            "The Koch Snowflake is created by applying the Koch Curve process to each side of an equilateral triangle."
        ).scale(0.5).to_edge(DOWN)
        self.play(Write(snowflake_explanation))

        self.wait(3)
        self.play(FadeOut(snowflake_label), FadeOut(snowflake_explanation))

        # Explain the mathematical properties
        properties_text = Text(
            "Mathematical Properties:\n"
            "1. The length of the curve increases by a factor of 4/3 with each iteration.\n"
            "2. The perimeter of the snowflake grows infinitely.\n"
            "3. The area of the snowflake converges to a finite value."
        ).scale(0.5).to_edge(DOWN)
        self.play(Write(properties_text))

        self.wait(3)
        self.play(FadeOut(properties_text))

        # Detailed mathematical explanation
        detailed_math = Text(
            "Mathematical Explanation:\n"
            "Starting with an equilateral triangle of side length s:\n"
            "Perimeter after n iterations: (3 * 4^n / 3^n) * s = 3 * s * (4/3)^n\n"
            "Area converges to: (2 * s^2 * sqrt(3)) / 5\n"
            "Even though the perimeter grows infinitely, the area remains finite."
        ).scale(0.5).to_edge(DOWN)
        self.play(Write(detailed_math))

        self.wait(3)
        self.play(FadeOut(detailed_math))

        # 3D Koch Curve
        koch_curve_3d = KochCurve(order=4).rotate(PI / 2, axis=UP)
        koch_curve_3d.set_color_by_gradient(BLUE, GREEN, YELLOW, ORANGE, RED)
        curve_3d_label = Text("3D Koch Curve").next_to(koch_curve_3d, UP)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(koch_curve_3d))
        self.play(Write(curve_3d_label))

        self.wait(3)
        self.play(FadeOut(koch_curve_3d), FadeOut(curve_3d_label), FadeOut(title))
        self.wait()

if __name__ == "__main__":
    from manim import command_line_interface
    command_line_interface.main()
