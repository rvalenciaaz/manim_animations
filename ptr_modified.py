from manim import *
import numpy as np

class ShortReadSimulationScene(Scene):
    def construct(self):
        # Title
        title = Text("Peak-to-trough ratio and growth rates").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Circular genome representation
        genome_circle = Circle(radius=2).shift(DOWN * 0.5)  
        genome_label = Text("(Circular) Bacterial Genome", font_size=24).next_to(genome_circle, UP).shift(UP * 0.5)  
        self.play(Create(genome_circle), FadeIn(genome_label))
        self.wait(1)

        # Animation of genome replication from ori to ter in the circular genome
        # Mark origin and terminus on the circle
        ori_point = genome_circle.point_at_angle(PI / 2)
        ter_point = genome_circle.point_at_angle(-PI / 2)

        # Add labels for origin and terminus
        ori_label = Text("oriC", font_size=20, color=GREEN).next_to(ori_point, UP)
        ter_label = Text("terC", font_size=20, color=RED).next_to(ter_point, DOWN)
        self.play(FadeIn(ori_label), FadeIn(ter_label))
        self.wait(1)

        # Replication forks
        angle_tracker = ValueTracker(0)

        def get_fork1():
            return Arc(radius=2, start_angle=PI / 2, angle=-angle_tracker.get_value(), color=YELLOW, stroke_width=10).shift(DOWN * 0.5) 

        def get_fork2():
            return Arc(radius=2, start_angle=PI / 2, angle=angle_tracker.get_value(), color=YELLOW, stroke_width=10).shift(DOWN * 0.5) 

        fork1 = always_redraw(get_fork1)
        fork2 = always_redraw(get_fork2)

        self.play(Create(fork1), Create(fork2))
        self.wait(1)

        # Animate the forks moving to the terminus
        self.play(angle_tracker.animate.set_value(PI), run_time=3)
        self.wait(1)

        self.play(FadeOut(title), FadeOut(genome_label))
        self.wait(0.1)

        # Move original genome to the upper left corner
        genomes = VGroup(genome_circle, ori_label, ter_label, fork1, fork2)
        self.play(
            genomes.animate.scale(0.5).to_corner(UL),
        )
        self.wait(1)

        # Create multiple genomes in a grid spanning the screen
        genomes_group = VGroup()
        rows, cols = 3, 3  # Adjusted grid size for better screen coverage

        x_positions = np.linspace(-6, 6, cols)
        y_positions = np.linspace(3, -3, rows)

        for row in range(rows):
            for col in range(cols):
                x_pos = x_positions[col]
                y_pos = y_positions[row]
                genome_copy = genomes.copy().move_to([x_pos, y_pos, 0])
                genomes_group.add(genome_copy)

        # Animate each genome copy appearing in sequence (long generation time)
        self.play(
            *[FadeIn(genome_copy, run_time=0.3) for genome_copy in genomes_group],
            lag_ratio=0.5  # Controls delay between each appearance for replication effect
        )
        self.wait(1)

        # Animate each genome copy appearing in sequence (short generation time)
        # Create more genomes to represent faster replication
        genomes_group_short = VGroup()
        rows_short, cols_short = 5, 5  # Larger grid for short generation time

        x_positions_short = np.linspace(-6, 6, cols_short)
        y_positions_short = np.linspace(3, -3, rows_short)

        for row in range(rows_short):
            for col in range(cols_short):
                x_pos = x_positions_short[col]
                y_pos = y_positions_short[row]
                genome_copy = genomes.copy().move_to([x_pos, y_pos, 0])
                genomes_group_short.add(genome_copy)

        # Animate genomes appearing quickly
        self.play(
            *[FadeIn(genome_copy, run_time=0.1) for genome_copy in genomes_group_short],
            lag_ratio=0.05  # Faster appearance for short generation time
        )
        self.wait(1)

        # Fade out circular genome and reads
        self.play(FadeOut(VGroup(genomes_group, genomes_group_short, genomes)))
        self.wait(1)

        # Proceed to the binning and coverage calculation
        # Genome representation as a line
        genome_line = Line(LEFT * 6, RIGHT * 6)
        genome_label = Text("Genome", font_size=24).next_to(genome_line, UP)
        self.play(Create(genome_line), FadeIn(genome_label))
        self.wait(1)

        
        # Divide genome into bins
        num_bins = 12
        bin_lines = VGroup()
        for i in range(1, num_bins):
            x = interpolate(-6, 6, i / num_bins)
            line = Line([x, -0.2, 0], [x, 0.2, 0])
            bin_lines.add(line)
        self.play(*[Create(line) for line in bin_lines])
        self.wait(1)

        # Show bins
        bin_labels = VGroup()
        for i in range(num_bins):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            label = Text(f"Bin {i+1}", font_size=16).move_to([x, -0.5, 0])
            bin_labels.add(label)
        self.play(*[FadeIn(label) for label in bin_labels])
        self.wait(1)

        # Adjusted probabilities
        ptr_value = 2  # PTR = 2
        ori_bin = 3  # Origin at Bin 4
        ter_bin = (ori_bin + num_bins // 2) % num_bins

        # Display PTR
        ptr_text = Tex(f"PTR = {ptr_value}", font_size=36).to_corner(UL)
        self.play(FadeIn(ptr_text))
        self.wait(1)

        # Display origin and terminus
        ori_indicator = Arrow(
            start=[interpolate(-6, 6, (ori_bin + 0.5) / num_bins), 0.3, 0],
            end=[interpolate(-6, 6, (ori_bin + 0.5) / num_bins), 1, 0],
            color=GREEN
        )
        ori_label = Text("Origin (oriC)", font_size=20, color=GREEN).next_to(ori_indicator, UP)
        self.play(Create(ori_indicator), FadeIn(ori_label))
        self.wait(1)

        ter_indicator = Arrow(
            start=[interpolate(-6, 6, (ter_bin + 0.5) / num_bins), 0.3, 0],
            end=[interpolate(-6, 6, (ter_bin + 0.5) / num_bins), 1, 0],
            color=RED
        )
        ter_label = Text("Terminus (terC)", font_size=20, color=RED).next_to(ter_indicator, UP)
        self.play(Create(ter_indicator), FadeIn(ter_label))
        self.wait(1)

        # Calculate adjusted probabilities
        adj_probs = self.compute_adjusted_probabilities(num_bins, ori_bin, ter_bin, ptr_value)

        # Display bars representing probabilities
        prob_bars = VGroup()
        max_prob = max(adj_probs)
        for i, prob in enumerate(adj_probs):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            bar_height = prob / max_prob * 2  # Scale bar height
            bar = Rectangle(
                width=0.8 * 12 / num_bins,
                height=bar_height,
                color=BLUE
            )
            bar.move_to([x, -1, 0], aligned_edge=DOWN)
            prob_bars.add(bar)
        # Animate bars growing from the bottom
        self.play(*[GrowFromEdge(bar, DOWN) for bar in prob_bars])
        self.wait(1)

        # Label probabilities
        prob_labels = VGroup()
        for i, prob in enumerate(adj_probs):
            label = DecimalNumber(prob, num_decimal_places=2, font_size=16)
            label.next_to(prob_bars[i], UP, buff=0.1)
            prob_labels.add(label)
        self.play(*[FadeIn(label) for label in prob_labels])
        self.wait(1)

        # Simulate reads
        num_reads = 1000
        read_counts = [int(prob * num_reads) for prob in adj_probs]

        # Display reads as dots
        read_dots = VGroup()
        for i, count in enumerate(read_counts):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            for j in range(min(count // 50, 5)):  # Limit dots for visibility
                y = -1.5 - j * 0.3
                dot = Dot(point=[x, y, 0], radius=0.05, color=YELLOW)
                read_dots.add(dot)
        self.play(*[FadeIn(dot) for dot in read_dots])
        self.wait(1)

        # Expected coverage plot
        coverage_line = Line([-6, -3.5, 0], [6, -3.5, 0])
        self.play(Create(coverage_line))
        coverage_values = [count / max(read_counts) * 2 for count in read_counts]  # Scale for visibility

        coverage_bars = VGroup()
        for i, coverage in enumerate(coverage_values):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            bar = Rectangle(
                width=0.8 * 12 / num_bins,
                height=coverage,
                color=ORANGE
            )
            bar.move_to([x, -3.5, 0], aligned_edge=DOWN)
            coverage_bars.add(bar)
        # Animate coverage bars growing from the bottom
        self.play(*[GrowFromEdge(bar, DOWN) for bar in coverage_bars])
        self.wait(1)

        # Final notes
        conclusion_text = Text("Expected Coverage Along the Genome", font_size=24)
        conclusion_text.next_to(coverage_line, DOWN, buff=1)
        self.play(Write(conclusion_text))
        self.wait(2)

        # Now, reduce the bin size for fine-grained coverage calculations
        self.play(FadeOut(VGroup(
            bin_lines, bin_labels, prob_bars, prob_labels, read_dots, coverage_bars, conclusion_text
        )))
        self.wait(1)

        # Increase num_bins for fine-grained coverage
        num_bins = 36  # Increase number of bins

        # Divide genome into more bins
        bin_lines = VGroup()
        for i in range(1, num_bins):
            x = interpolate(-6, 6, i / num_bins)
            line = Line([x, -0.2, 0], [x, 0.2, 0])
            bin_lines.add(line)
        self.play(*[Create(line) for line in bin_lines])
        self.wait(1)

        # Show new bins
        bin_labels = VGroup()
        for i in range(num_bins):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            label = Text(f"{i+1}", font_size=12).move_to([x, -0.5, 0])
            bin_labels.add(label)
        self.play(*[FadeIn(label) for label in bin_labels])
        self.wait(1)

        # Recalculate adjusted probabilities
        adj_probs = self.compute_adjusted_probabilities(num_bins, ori_bin, ter_bin, ptr_value)

        # Display new probability bars
        prob_bars = VGroup()
        max_prob = max(adj_probs)
        for i, prob in enumerate(adj_probs):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            bar_height = prob / max_prob * 2  # Scale bar height
            bar = Rectangle(
                width=0.8 * 12 / num_bins,
                height=bar_height,
                color=BLUE
            )
            bar.move_to([x, -1, 0], aligned_edge=DOWN)
            prob_bars.add(bar)
        self.play(*[GrowFromEdge(bar, DOWN) for bar in prob_bars])
        self.wait(1)

        # Simulate reads with new bins
        read_counts = [int(prob * num_reads) for prob in adj_probs]

        # Display new coverage bars
        coverage_line = Line([-6, -3.5, 0], [6, -3.5, 0])
        self.play(Create(coverage_line))
        coverage_values = [count / max(read_counts) * 2 for count in read_counts]  # Scale for visibility

        coverage_bars = VGroup()
        for i, coverage in enumerate(coverage_values):
            x = interpolate(-6, 6, (i + 0.5) / num_bins)
            bar = Rectangle(
                width=0.8 * 12 / num_bins,
                height=coverage,
                color=ORANGE
            )
            bar.move_to([x, -3.5, 0], aligned_edge=DOWN)
            coverage_bars.add(bar)
        self.play(*[GrowFromEdge(bar, DOWN) for bar in coverage_bars])
        self.wait(1)

        # Final notes
        conclusion_text = Text("Fine-Grained Coverage Along the Genome", font_size=24)
        conclusion_text.next_to(coverage_line, DOWN, buff=1)
        self.play(Write(conclusion_text))
        self.wait(2)

        # Fade out
        self.play(FadeOut(VGroup(
            genome_line, genome_label, bin_lines, bin_labels, ptr_text, ori_indicator, ori_label,
            ter_indicator, ter_label, prob_bars, coverage_line, coverage_bars, conclusion_text, title
        )))
        self.wait(1)

    def compute_adjusted_probabilities(self, num_bins, ori_bin, ter_bin, ptr_value):
        # Compute adjusted probabilities based on copy number
        adj_probs = []
        for i in range(num_bins):
            # Compute angle between bin i and ori_bin
            angle = abs((i - ori_bin) % num_bins) * (2 * np.pi / num_bins)
            if angle > np.pi:
                angle = 2 * np.pi - angle
            # Copy number decreases linearly from PTR at ori to 1 at ter
            copy_number = 1 + (ptr_value - 1) * (1 - angle / np.pi)
            adj_probs.append(copy_number)
        # Normalize probabilities
        total = sum(adj_probs)
        adj_probs = [prob / total for prob in adj_probs]
        return adj_probs