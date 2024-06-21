from manim import *

class MultiThreadedProcessing(Scene):
    def construct(self):
        # Title
        title = Text("Multi-Threaded Processing", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # Introduction to Mandelbrot Set
        mandelbrot_intro = Text("The Mandelbrot Set\nA Computationally Intensive Problem", font_size=36)
        self.play(Write(mandelbrot_intro))
        self.wait(3)
        self.play(FadeOut(mandelbrot_intro))
        
        # Explanation of Single-Threaded Processing
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
        
        # Explain the problem with single-threaded processing
        problem_text = Text("Single-threaded processing can be slow\nbecause it uses only one CPU core.", font_size=24)
        self.play(Write(problem_text))
        self.wait(3)
        self.play(FadeOut(problem_text))
        
        # Introduction to Multi-Threaded Processing
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
        self.play(FadeOut(code_multi_thread), FadeOut(multi_threaded_text))
        
        # Explain how threading works with an example
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
        
        # Detailed Explanation of Multi-Processing using Physical World Examples
        detail_text = Text("Multi-Processing Explained", font_size=36)
        self.play(Write(detail_text))
        self.wait(2)
        self.play(FadeOut(detail_text))
        
        # Physical World Example: Assembly Line
        assembly_text = Text("Imagine an Assembly Line", font_size=36)
        self.play(Write(assembly_text))
        self.wait(2)
        
        workers = [Square().set_fill(YELLOW, opacity=0.5) for _ in range(4)]
        workers_group = VGroup(*workers).arrange(RIGHT, buff=0.5).next_to(assembly_text, DOWN, buff=1)
        task = Rectangle(width=1, height=0.5).set_fill(RED, opacity=0.5)
        task.next_to(workers_group, UP, buff=0.5)
        
        self.play(FadeIn(workers_group), FadeIn(task))
        self.wait(2)
        
        task_splits = [task.copy().set_fill(RED, opacity=0.5).scale(0.25) for _ in range(4)]
        task_splits_group = VGroup(*task_splits).arrange(RIGHT, buff=0.5).next_to(task, DOWN, buff=1)
        
        self.play(
            task.animate.move_to(workers_group[0].get_center()),
            TransformFromCopy(task, task_splits[0]),
            TransformFromCopy(task, task_splits[1]),
            TransformFromCopy(task, task_splits[2]),
            TransformFromCopy(task, task_splits[3])
        )
        self.wait(2)
        
        self.play(
            task_splits[0].animate.move_to(workers_group[0].get_center()),
            task_splits[1].animate.move_to(workers_group[1].get_center()),
            task_splits[2].animate.move_to(workers_group[2].get_center()),
            task_splits[3].animate.move_to(workers_group[3].get_center()),
        )
        self.wait(2)
        
        # Completing the tasks in parallel
        parallel_text = Text("Each worker completes a part in parallel", font_size=24).next_to(workers_group, DOWN, buff=0.5)
        self.play(Write(parallel_text))
        self.wait(3)
        
        speed_text = Text("Work gets done faster!", font_size=36).set_color(GREEN).to_edge(DOWN)
        self.play(Write(speed_text))
        self.wait(2)
        
        self.play(FadeOut(assembly_text), FadeOut(workers_group), FadeOut(task), FadeOut(task_splits_group), FadeOut(parallel_text), FadeOut(speed_text))
        
        # Conclusion
        conclusion = Text("And that's the power of multi-threaded processing!", font_size=36)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))

if __name__ == "__main__":
    scene = MultiThreadedProcessing()
    scene.render()
