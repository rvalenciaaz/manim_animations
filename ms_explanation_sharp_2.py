from manim import *
import numpy as np

class MassSpectrometryAnimation(Scene):
    def construct(self):
        # Adjust layout and scaling to fit everything
        scale_factor = 0.75

        # Create axes for mass spectrum
        mass_spectrum_axes = Axes(
            x_range=[0, 1100, 200],
            y_range=[0, 10, 2],
            x_length=4,
            y_length=2,
            tips=False,
            axis_config={"include_numbers": True},
            x_axis_config={"numbers_to_include": [200, 400, 600, 800, 1000]},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8]}
        )
        mass_spectrum_label = mass_spectrum_axes.get_axis_labels(
            x_label=Tex("m/z").scale(0.7),
            y_label=Tex("Intensity").scale(0.7)
        )

        # Create axes for TIC
        tic_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 50, 10],
            x_length=4,
            y_length=2,
            tips=False,
            axis_config={"include_numbers": True}
        )
        tic_label = tic_axes.get_axis_labels(
            x_label=Tex("Time").scale(0.7),
            y_label=Tex("Total Intensity").scale(0.7)
        )

        # Create axes for EIC
        eic_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 2],
            x_length=4,
            y_length=2,
            tips=False,
            axis_config={"include_numbers": True}
        )
        eic_label = eic_axes.get_axis_labels(
            x_label=Tex("Time").scale(0.7),
            y_label=Tex("Intensity at m/z=600").scale(0.7)
        )

        # Arrange them in a row with some spacing and move up
        mass_spectrum_group = VGroup(mass_spectrum_axes, mass_spectrum_label).scale(scale_factor).to_edge(UP+LEFT, buff=0.5)
        tic_group = VGroup(tic_axes, tic_label).scale(scale_factor).next_to(mass_spectrum_group, RIGHT, buff=0.5)
        eic_group = VGroup(eic_axes, eic_label).scale(scale_factor).next_to(tic_group, RIGHT, buff=0.5)
        group_all = VGroup(mass_spectrum_group, tic_group, eic_group) #.move_to(UP*2.5)

        group_all.shift(DOWN*1)
        self.play(Create(mass_spectrum_axes), Write(mass_spectrum_label))
        self.play(Create(tic_axes), Write(tic_label))
        self.play(Create(eic_axes), Write(eic_label))

	# Add TIC and XIC titles above their respective chromatograms
        spectrum_title = Tex("Spectrum").scale(0.7).next_to(mass_spectrum_group, UP, buff=0.1)
        tic_title = Tex("TIC").scale(0.7).next_to(tic_group, UP, buff=0.1)
        xic_title = Tex("XIC").scale(0.7).next_to(eic_group, UP, buff=0.1)
        self.play(Write(spectrum_title),Write(tic_title), Write(xic_title))

	# Define m/z values and colors for each peak
        mz_values = np.array([200, 400, 600, 800, 1000])
        mz_colors = [BLUE, GREEN, YELLOW, RED, PURPLE]

        # Simulate data
        times = np.arange(0, 11, 1)
        intensities_over_time = [np.random.randint(1, 10, size=len(mz_values)) for _ in times]

        # Initialize lists for TIC and EIC
        tic_values = []
        eic_values = []

        # Choose an m/z value for EIC
        eic_mz = 600
        eic_index = np.where(mz_values == eic_mz)[0][0]

        # Initialize lines for TIC and EIC
        tic_line = VGroup()
        eic_line = VGroup()

        # Ion detector animation area at the bottom
        ion_path_start = LEFT*4 + DOWN*1.5
        ion_path_end = RIGHT*4 + DOWN*1.5
        ion_detector_pos = RIGHT*3 + DOWN*1.5

        ion_path_line = Line(start=ion_path_start, end=ion_path_end, color=GREY)
        detector_line = Line(
            start=ion_detector_pos + UP*0.5,
            end=ion_detector_pos + DOWN*0.5,
            color=WHITE
        )

        self.play(Create(ion_path_line), Create(detector_line))

        for i, t in enumerate(times):
            intensities = intensities_over_time[i]

            # Create mass spectrum lines (peaks) for display after ions arrive
            peaks = VGroup()
            for j, (mz, color) in enumerate(zip(mz_values, mz_colors)):
                bar_height = intensities[j]
                x0, y0, z0 = mass_spectrum_axes.coords_to_point(mz, 0)
                x1, y1, z1 = mass_spectrum_axes.coords_to_point(mz, bar_height)
                peak = Line(
                    start=[x0, y0, 0],
                    end=[x1, y1, 0],
                    stroke_color=color,
                    stroke_width=4
                )
                peaks.add(peak)

            # Ions animation: Represent ions as small dots
            ion_group = VGroup()
            x_start = ion_path_start[0]
            x_end = ion_detector_pos[0]

            for j, (mz, color) in enumerate(zip(mz_values, mz_colors)):
                count = intensities[j]
                y_center = ion_path_start[1]
                x_offset=j*0.1
                for k in range(count):
                    ion = Dot(point=[x_start+x_offset, y_center + (k - count/2)*0.1, 0], radius=0.05, color=color)
                    ion_group.add(ion)

            # 1. Ions appear and move towards the detector first
            self.play(FadeIn(ion_group), run_time=0.5)
            self.play(ion_group.animate.shift(RIGHT*(x_end - x_start)), run_time=1)

            # 2. Once ions have arrived, remove them
            self.play([FadeOut(ion_group), Create(peaks)], run_time=0.5)

            # 3. After ions arrival, show mass spectrum and then update TIC/EIC
            # Show mass spectrum peaks now
            #self.play(Create(peaks), run_time=0.5)

            # Update TIC (sum of intensities)
            tic_value = np.sum(intensities)
            tic_values.append(tic_value)

            if i > 0:
                new_tic_line = tic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=tic_values,
                    line_color=WHITE
                )
                self.play(Transform(tic_line, new_tic_line), run_time=0.5)
            else:
                tic_line = tic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=tic_values,
                    line_color=WHITE
                )
                self.play(Create(tic_line), run_time=0.5)

            # Update EIC for chosen m/z (600 in this example)
            eic_value = intensities[eic_index]
            eic_values.append(eic_value)

            if i > 0:
                new_eic_line = eic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=eic_values,
                    line_color=YELLOW
                )
                self.play(Transform(eic_line, new_eic_line), run_time=0.5)
            else:
                eic_line = eic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=eic_values,
                    line_color=YELLOW
                )
                self.play(Create(eic_line), run_time=0.5)

            # Fade out the peaks before the next time step
            self.play(FadeOut(peaks), run_time=0.5)

        self.wait(2)
