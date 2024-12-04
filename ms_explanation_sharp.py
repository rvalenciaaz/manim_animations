from manim import *
import numpy as np

class MassSpectrometryAnimation(Scene):
    def construct(self):
        # Create axes for mass spectrum
        # Adjust x_range to accommodate m/z from 0 to ~1100 with suitable ticks
        mass_spectrum_axes = Axes(
            x_range=[0, 1100, 200],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
            x_axis_config={"numbers_to_include": [200, 400, 600, 800, 1000]},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8]}
        ).to_corner(LEFT + UP)

        mass_spectrum_label = mass_spectrum_axes.get_axis_labels(
            x_label=Tex("m/z"),
            y_label=Tex("Intensity")
        )

        # Create axes for TIC
        tic_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 50, 10],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_corner(UP + RIGHT)

        tic_label = tic_axes.get_axis_labels(
            x_label=Tex("Time"),
            y_label=Tex("Total Intensity")
        )

        # Create axes for EIC
        eic_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True}
        ).next_to(tic_axes, DOWN, buff=1)

        eic_label = eic_axes.get_axis_labels(
            x_label=Tex("Time"),
            y_label=Tex("Intensity at m/z=600")  # We'll choose one of our m/z values
        )

        # Add axes to the scene
        self.play(Create(mass_spectrum_axes), Write(mass_spectrum_label))
        self.play(Create(tic_axes), Write(tic_label))
        self.play(Create(eic_axes), Write(eic_label))

        # Define m/z values from 200 to 1000
        mz_values = np.array([200, 400, 600, 800, 1000])

        # Simulate data
        times = np.arange(0, 11, 1)
        # Generate random intensities for each time point
        intensities_over_time = [np.random.randint(1, 10, size=len(mz_values)) for _ in times]

        # Initialize lists for TIC and EIC
        tic_values = []
        eic_values = []

        # Choose an m/z value for EIC (for example, m/z=600)
        eic_mz = 600
        eic_index = np.where(mz_values == eic_mz)[0][0]

        # Initialize lines for TIC and EIC
        tic_line = VGroup()
        eic_line = VGroup()

        for i, t in enumerate(times):
            intensities = intensities_over_time[i]

            # Create mass spectrum lines (peaks) for this time
            peaks = VGroup()
            for j, mz in enumerate(mz_values):
                bar_height = intensities[j]

                # Convert data coordinates to scene coordinates
                x0, y0, z0 = mass_spectrum_axes.coords_to_point(mz, 0)
                x1, y1, z1 = mass_spectrum_axes.coords_to_point(mz, bar_height)

                # Create a vertical line to represent the peak
                peak = Line(
                    start=[x0, y0, 0],
                    end=[x1, y1, 0],
                    stroke_color=BLUE,
                    stroke_width=4  # adjust thickness of the peak line
                )
                peaks.add(peak)

            # Show the mass spectrum for this time point as vertical lines
            self.play(Create(peaks), run_time=0.5)
            self.wait(0.5)
            self.play(FadeOut(peaks), run_time=0.5)

            # Update TIC (sum of intensities)
            tic_value = np.sum(intensities)
            tic_values.append(tic_value)

            if i > 0:
                new_tic_line = tic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=tic_values,
                    line_color=RED
                )
                self.play(Transform(tic_line, new_tic_line), run_time=0.5)
            else:
                tic_line = tic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=tic_values,
                    line_color=RED
                )
                self.play(Create(tic_line), run_time=0.5)

            # Update EIC for chosen m/z (600 in this example)
            eic_value = intensities[eic_index]
            eic_values.append(eic_value)

            if i > 0:
                new_eic_line = eic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=eic_values,
                    line_color=GREEN
                )
                self.play(Transform(eic_line, new_eic_line), run_time=0.5)
            else:
                eic_line = eic_axes.plot_line_graph(
                    x_values=times[:i+1],
                    y_values=eic_values,
                    line_color=GREEN
                )
                self.play(Create(eic_line), run_time=0.5)
