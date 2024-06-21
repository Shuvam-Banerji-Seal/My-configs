
from manim import *

class LambdaFunctions(Scene):
    def construct(self):
        # Introduction to Lambda Functions
        title = Text("Lambda Functions in Python").to_edge(UP)
        self.play(Write(title))
        intro_text = Text("""
        Lambda functions are small anonymous functions.
        They are defined using the lambda keyword.
        """)
        self.play(FadeIn(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # Syntax of Lambda Functions
        syntax_title = Text("Syntax of Lambda Functions").to_edge(UP)
        syntax_text = Text("""
        lambda arguments: expression
        """)
        self.play(Transform(title, syntax_title))
        self.play(Write(syntax_text))
        self.wait(2)

        # Example of Lambda Function
        example_title = Text("Example of Lambda Function").to_edge(UP)
        example_code = Code("""
        # Regular function
        def add(x, y):
            return x + y

        # Equivalent lambda function
        add = lambda x, y: x + y
        """, language="python")
        self.play(Transform(title, example_title))
        self.play(FadeOut(syntax_text))
        self.play(FadeIn(example_code))
        self.wait(3)
        self.play(FadeOut(example_code))

        # Introduction to Lambda Calculus
        calculus_title = Text("Lambda Calculus").to_edge(UP)
        calculus_text = Text("""
        Lambda calculus is a formal system in mathematical logic
        for expressing computation based on function abstraction and application.
        """)
        self.play(Transform(title, calculus_title))
        self.play(FadeIn(calculus_text))
        self.wait(3)
        self.play(FadeOut(calculus_text))

        # Syntax of Lambda Calculus
        lambda_calculus_syntax = Text("""
        Syntax:
        (λx.x)   - Identity function
        (λx.x)(y) - Application of the identity function to y
        """)
        self.play(Write(lambda_calculus_syntax))
        self.wait(3)
        self.play(FadeOut(lambda_calculus_syntax))

        # Mandelbrot Set Example
        mandelbrot_title = Text("Mandelbrot Set with Lambda").to_edge(UP)
        mandelbrot_code = Code("""
        import numpy as np, matplotlib.pyplot as plt; plt.imshow((lambda f: lambda Re, Im, max_iter: np.frompyfunc(f, 3, 1)(Re + 1j*Im, 0, max_iter).astype(np.float64))((lambda c, z, max_iter: next((i for i in range(max_iter) if abs(z := z*z + c) > 2), max_iter)))(*np.meshgrid(np.linspace(-2, 1, 1000), np.linspace(-1.5, 1.5, 1000)), 256), extent=(-2, 1, -1.5, 1.5), cmap='hot'); plt.colorbar(); plt.show()
        """, language="python", insert_line_no=False, style="monokai")

        self.play(Transform(title, mandelbrot_title))
        self.play(FadeIn(mandelbrot_code))
        self.wait(3)

        # Explanation of the Mandelbrot code
        self.play(FadeOut(mandelbrot_code))
        explanation_text = Text("""
        The Mandelbrot set code can be broken down as follows:
        1. Define a lambda function to compute the Mandelbrot set.
        2. Use np.frompyfunc to vectorize the lambda function.
        3. Create a meshgrid of complex numbers.
        4. Plot the Mandelbrot set using matplotlib.
        """)
        self.play(FadeIn(explanation_text))
        self.wait(5)
        self.play(FadeOut(explanation_text))

        # Detailed step-by-step explanation
        detailed_title = Text("Step-by-Step Explanation").to_edge(UP)
        self.play(Transform(title, detailed_title))

        step_1 = Text("1. Define a lambda function to compute the Mandelbrot set.")
        self.play(FadeIn(step_1))
        self.wait(2)
        self.play(FadeOut(step_1))

        step_2 = Text("2. Use np.frompyfunc to vectorize the lambda function.")
        self.play(FadeIn(step_2))
        self.wait(2)
        self.play(FadeOut(step_2))

        step_3 = Text("3. Create a meshgrid of complex numbers.")
        self.play(FadeIn(step_3))
        self.wait(2)
        self.play(FadeOut(step_3))

        step_4 = Text("4. Plot the Mandelbrot set using matplotlib.")
        self.play(FadeIn(step_4))
        self.wait(2)
        self.play(FadeOut(step_4))

        conclusion = Text("This concludes our explanation of lambda functions and the Mandelbrot set.").to_edge(DOWN)
        self.play(FadeIn(conclusion))
        self.wait(3)

        # Final one-liner display
        oneliner_title = Text("Mandelbrot Set One-Liner").to_edge(UP)
        oneliner_code = Code("""
        import numpy as np, matplotlib.pyplot as plt; plt.imshow((lambda f: lambda Re, Im, max_iter: np.frompyfunc(f, 3, 1)(Re + 1j*Im, 0, max_iter).astype(np.float64))((lambda c, z, max_iter: next((i for i in range(max_iter) if abs(z := z*z + c) > 2), max_iter)))(*np.meshgrid(np.linspace(-2, 1, 1000), np.linspace(-1.5, 1.5, 1000)), 256), extent=(-2, 1, -1.5, 1.5), cmap='hot'); plt.colorbar(); plt.show()
        """, language="python", insert_line_no=False, style="monokai")

        self.play(Transform(title, oneliner_title))
        self.play(FadeIn(oneliner_code))
        self.wait(5)