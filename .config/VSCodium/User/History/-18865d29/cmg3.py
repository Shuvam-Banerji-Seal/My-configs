from manim import *

class MultiThreadedProcessing(Scene):
    def construct(self):
        title = Text("Multi-Threaded Processing", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # Introduce the Mandelbrot Set and the problem
        problem_text = Text("The Mandelbrot Set\nComputationally Intensive Problem", font_size=36)
        self.play(Write(problem_text))
        self.wait(3)
        self.play(FadeOut(problem_text))
        
        # Single-threaded processing
        single_threaded_text = Text("Single-Threaded Processing", font_size=36)
        self.play(Write(single_threaded_text))
        self.wait(2)
        
        code_single_thread = Code(
            code="""def compute_mandelbrot_single_threaded(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)

    return n3""",
            language="python", font_size=18
        )
        self.play(Write(code_single_thread))
        self.wait(5)
        self.play(FadeOut(code_single_thread), FadeOut(single_threaded_text))
        
        # Multi-threaded processing
        multi_threaded_text = Text("Multi-Threaded Processing", font_size=36)
        self.play(Write(multi_threaded_text))
        self.wait(2)
        
        code_multi_thread = Code(
            code="""def compute_mandelbrot_parallel(xmin, xmax, ymin, ymax, width, height, max_iter, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    segment_size = (width + num_processes - 1) // num_processes
    segments = [(xmin, xmax, ymin, ymax, width, height, max_iter, i * segment_size, min((i + 1) * segment_size, width)) for i in range(num_processes)]

    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(compute_mandelbrot_segment, segments)
    pool.close()
    pool.join()

    n3 = np.vstack(results)
    return n3""",
            language="python", font_size=18
        )
        self.play(Write(code_multi_thread))
        self.wait(5)
        self.play(FadeOut(code_multi_thread))
        
        # Visualization of threading
        threading_text = Text("How Threading Works", font_size=36)
        self.play(Write(threading_text))
        self.wait(2)
        
        cpu_text = Text("CPU Cores", font_size=24).to_edge(UP)
        self.play(Write(cpu_text))
        
        cores = [Circle().set_fill(BLUE, opacity=0.5) for _ in range(4)]
        cores_group = VGroup(*cores).arrange(RIGHT, buff=0.5).next_to(cpu_text, DOWN, buff=0.5)
        self.play(FadeIn(cores_group))
        
        workload_text = Text("Workload", font_size=24).next_to(cores_group, DOWN, buff=0.5)
        self.play(Write(workload_text))
        
        workload = Square().set_fill(RED, opacity=0.5).scale(0.7)
        workload.next_to(workload_text, DOWN, buff=0.5)
        self.play(FadeIn(workload))
        
        # Splitting the workload
        split_text = Text("Splitting the Workload", font_size=24).next_to(workload, DOWN, buff=0.5)
        self.play(Write(split_text))
        
        workloads = [Square().set_fill(RED, opacity=0.5).scale(0.35) for _ in range(4)]
        workloads_group = VGroup(*workloads).arrange(RIGHT, buff=0.5).next_to(split_text, DOWN, buff=0.5)
        
        self.play(
            workload.animate.move_to(cores_group[0].get_center()),
            TransformFromCopy(workload, workloads[0]),
            TransformFromCopy(workload, workloads[1]),
            TransformFromCopy(workload, workloads[2]),
            TransformFromCopy(workload, workloads[3])
        )
        self.wait(2)
        
        self.play(
            workloads[0].animate.move_to(cores_group[0].get_center()),
            workloads[1].animate.move_to(cores_group[1].get_center()),
            workloads[2].animate.move_to(cores_group[2].get_center()),
            workloads[3].animate.move_to(cores_group[3].get_center()),
        )
        self.wait(2)
        
        # Completing the process
        complete_text = Text("Each core works on its part\nin parallel", font_size=24).next_to(workloads_group, DOWN, buff=0.5)
        self.play(Write(complete_text))
        self.wait(3)
        
        final_text = Text("Faster Processing!", font_size=36).set_color(GREEN).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)
        
        self.play(FadeOut(cpu_text), FadeOut(cores_group), FadeOut(workload_text), FadeOut(workload), FadeOut(split_text), FadeOut(workloads_group), FadeOut(complete_text), FadeOut(final_text), FadeOut(threading_text))
        
        conclusion = Text("And that's the power of multi-threaded processing!", font_size=36)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))

if __name__ == "__main__":
    scene = MultiThreadedProcessing()
    scene.render()
