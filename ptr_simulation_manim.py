from manim import *

class ShortReadSimulationScene(Scene):
    def construct(self):
        # Title
        title = Text("Short Read Simulation Algorithm").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Genome representation
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
        adj_probs = []
        max_prob = 0
        for i in range(num_bins):
            if ori_bin < ter_bin:
                if i < ori_bin:
                    prob = ptr_value ** (- (ori_bin - i) / (ori_bin - ter_bin))
                elif ori_bin <= i <= ter_bin:
                    prob = ptr_value ** ((i - ori_bin) / (ter_bin - ori_bin))
                else:
                    prob = ptr_value ** (- (i - ter_bin) / (num_bins - ter_bin + ori_bin))
            else:
                if i <= ter_bin:
                    prob = ptr_value ** (- (i - ter_bin) / (num_bins - ori_bin + ter_bin))
                elif ter_bin < i < ori_bin:
                    prob = ptr_value ** ((i - ter_bin) / (ori_bin - ter_bin))
                else:
                    prob = ptr_value ** (- (ori_bin - i) / (num_bins - ori_bin + ter_bin))
            adj_probs.append(prob)
            if prob > max_prob:
                max_prob = prob

        # Normalize probabilities
        total_prob = sum(adj_probs)
        adj_probs = [p / total_prob for p in adj_probs]

        # Display bars representing probabilities
        prob_bars = VGroup()
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

        # Fade out
        self.play(FadeOut(VGroup(
            genome_line, genome_label, bin_lines, bin_labels, ptr_text, ori_indicator, ori_label,
            ter_indicator, ter_label, prob_bars, prob_labels, read_dots, coverage_line, coverage_bars,
            conclusion_text, title
        )))
        self.wait(1)