from manim import *

class MandelbrotExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Exploring the Mandelbrot Set", font_size=60).to_edge(UP)
        self.play(Write(title))

        # Step 1: Introduction to Mandelbrot Set
        step1_title = Text("Step 1: Understanding the Mandelbrot Set", font_size=40).next_to(title, DOWN, buff=1)
        self.play(Write(step1_title))

        mandelbrot_formula = MathTex(
            "z_{n+1} = z_{n}^2 + c", tex_to_color_map={"z_{n+1}": BLUE, "z_{n}": BLUE, "c": ORANGE}
        ).scale(1.2).next_to(step1_title, DOWN, buff=0.5)
        self.play(Write(mandelbrot_formula))

        mandelbrot_definition = Text(
            "The Mandelbrot set is the set of complex numbers $c$ for which the sequence \\{$z_{n}$\\} remains bounded.",
            font_size=24
        ).next_to(mandelbrot_formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(mandelbrot_definition))

        self.wait(2)

        # Step 2: Explanation of Lambda Functions
        step2_title = Text("Step 2: Explaining the Lambda Functions", font_size=40).next_to(mandelbrot_definition, DOWN, buff=1)
        self.play(FadeOut(step1_title), FadeOut(mandelbrot_formula), FadeOut(mandelbrot_definition))
        self.play(Write(step2_title))

        lambda_explanation = Text(
            "Lambda functions are anonymous functions used here to define the Mandelbrot computation inline.\n"
            "They encapsulate the iterative process and operate efficiently on arrays.",
            font_size=24
        ).next_to(step2_title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(lambda_explanation))

        # Show the outer lambda function
        outer_lambda = MathTex(
            r"\lambda f: \lambda \text{Re}, \text{Im}, \text{max\_iter}:",
            r"\text{np.frompyfunc}(f, 3, 1)(\text{Re} + \text{Im} \cdot 1j, 0, \text{max\_iter})",
            r".\text{astype}(\text{np.float64})"
        ).scale(0.8).next_to(lambda_explanation, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(outer_lambda))

        # Show the inner lambda function
        inner_lambda = MathTex(
            r"\lambda c, z, \text{max\_iter}:",
            r"\text{next}((i \text{ for } i \text{ in } \text{range}(\text{max\_iter})",
            r"\text{ if abs}(z := z \cdot z + c) > 2), \text{max\_iter})"
        ).scale(0.8).next_to(outer_lambda, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(inner_lambda))

        self.wait(2)

        # Step 3: Implementing Manim Animation
        step3_title = Text("Step 3: Implementing Manim Animation", font_size=40).next_to(inner_lambda, DOWN, buff=1)
        self.play(FadeOut(step2_title), FadeOut(lambda_explanation), FadeOut(outer_lambda), FadeOut(inner_lambda))
        self.play(Write(step3_title))

        self.wait(2)

        # Generate Mandelbrot set and visualize
        mandelbrot_scene = MandelbrotVisualization()
        self.play(FadeOut(step3_title))
        self.wait(1)
        self.play(Create(mandelbrot_scene), run_time=10)
        self.wait(3)

class MandelbrotVisualization(ThreeDScene):
    def construct(self):
        # Generate the Mandelbrot set
        mandelbrot = (
            lambda f: lambda Re, Im, max_iter:
            np.frompyfunc(f, 3, 1)(Re + 1j*Im, 0, max_iter).astype(np.float64)
        )(
            (lambda c, z, max_iter:
             next((i for i in range(max_iter) if abs(z := z*z + c) > 2), max_iter))
        )

        mandelbrot_image = mandelbrot(
            *np.meshgrid(np.linspace(-2, 1, 1000), np.linspace(-1.5, 1.5, 1000)), 256
        )

        # Convert Mandelbrot set data to Manim image
        mandelbrot_set = ImageMobject(np.flipud(mandelbrot_image))
        mandelbrot_set.set_height(6)
        mandelbrot_set.set_color_gradient(["black", "red", "orange", "yellow", "white"])

        self.add(mandelbrot_set)
        self.wait(10)
