from manim import *

class SINDyExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Sparse Identification of Nonlinear Dynamics (SINDy)", font_size=24)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))

        # Introduction
        intro_lines = [
            "SINDy is a data-driven method to discover",
            "the governing equations of dynamical systems.",
            "",
            "It assumes that the dynamics can be represented",
            "with a sparse combination of candidate functions.",
            "",
            "The key idea is to find the simplest model",
            "that describes the observed data."
        ]
        intro_text = VGroup(*[Text(line, font_size=14) for line in intro_lines]).arrange(DOWN, aligned_edge=LEFT)
        self.play(FadeIn(intro_text, lag_ratio=0.1))
        self.wait(8)
        self.play(FadeOut(intro_text))

        # Step 1: Collect Data
        step1_title = Text("1. Collect Data", font_size=36).to_edge(UP)
        self.play(Write(step1_title))
        self.wait(2)
        # Example Data Plot
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(DOWN)
        labels = axes.get_axis_labels(x_label="t", y_label="x(t)")
        sine_curve = axes.plot(lambda t: np.sin(t), x_range=[0, 10], color=BLUE)
        self.play(Create(axes), Write(labels))
        self.play(Create(sine_curve), run_time=3)
        self.wait(2)
        data_note = Text("Collect measurements of the system's state over time.", font_size=28).shift(3*DOWN)
        self.play(Write(data_note))
        self.wait(3)

        # Transition to scatter plot
        sample_points = [axes.coords_to_point(t, np.sin(t)) for t in np.linspace(0, 10, 20)]
        dots = VGroup(*[Dot(point=pt, color=YELLOW) for pt in sample_points])
        self.play(FadeOut(sine_curve), FadeIn(dots))
        sample_note = Text("Sampled data points from measurements.", font_size=28).shift(3*DOWN)
        self.play(ReplacementTransform(data_note, sample_note))
        self.wait(3)
        self.play(FadeOut(sample_note))
        self.play(FadeOut(axes), FadeOut(labels), FadeOut(dots))
        self.play(FadeOut(step1_title))

        # Step 2: Compute Derivatives
        step2_title = Text("2. Compute Derivatives", font_size=36).to_edge(UP)
        self.play(Write(step2_title))
        self.wait(2)
        # Show finite differences
        derivative_eq = MathTex(r"\dot{x}(t) \approx \frac{x(t+\Delta t) - x(t)}{\Delta t}")
        self.play(Write(derivative_eq))
        self.wait(2)

        # Show tangent line at a point
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(DOWN)
        sine_curve = axes.plot(lambda t: np.sin(t), x_range=[0, 10], color=BLUE)
        self.play(Create(axes), Create(sine_curve))

        # Choose a point and show tangent
        t0 = 5
        x0 = np.sin(t0)
        point = Dot(axes.coords_to_point(t0, x0), color=YELLOW)
        self.play(FadeIn(point))
        # Tangent line
        slope = np.cos(t0)
        tangent_line = axes.plot(
            lambda t: slope * (t - t0) + x0,
            x_range=[t0 - 1, t0 + 1],
            color=RED,
        )
        self.play(Create(tangent_line))
        derivative_note = Text("Estimate derivative at each point.", font_size=28).shift(3*DOWN)
        self.play(Write(derivative_note))
        self.wait(3)
        self.play(FadeOut(derivative_eq), FadeOut(derivative_note))
        self.play(FadeOut(point), FadeOut(tangent_line), FadeOut(sine_curve), FadeOut(axes))
        self.play(FadeOut(step2_title))

        # Step 3: Construct Library of Candidate Functions
        step3_title = Text("3. Construct Library of Candidate Functions", font_size=36).to_edge(UP)
        self.play(Write(step3_title))
        self.wait(2)
        library_eq = MathTex(r"\Theta(\mathbf{X}) = \begin{bmatrix} 1 & \mathbf{X} & \mathbf{X}^2 & \mathbf{X}^3 & \dots \end{bmatrix}")
        self.play(Write(library_eq))
        self.wait(2)

        # Show candidate functions graphically
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(2*LEFT + DOWN)
        self.play(Create(axes))
        # Plot x, x^2, x^3
        x_func = axes.plot(lambda x: x, x_range=[-2, 2], color=BLUE)
        x2_func = axes.plot(lambda x: x**2, x_range=[-2, 2], color=GREEN)
        x3_func = axes.plot(lambda x: x**3, x_range=[-2, 2], color=RED)
        functions = VGroup(x_func, x2_func, x3_func)
        self.play(Create(functions), run_time=3)
        legend = VGroup(
            VGroup(Line(color=BLUE), Text("x", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(Line(color=GREEN), Text("x²", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(Line(color=RED), Text("x³", font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(axes, RIGHT)
        self.play(FadeIn(legend))
        self.wait(3)

        # Trigonometric functions
        axes_trig = Axes(
            x_range=[-2*np.pi, 2*np.pi, np.pi],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(2*RIGHT + DOWN)
        self.play(Create(axes_trig))
        sin_func = axes_trig.plot(lambda x: np.sin(x), x_range=[-2*np.pi, 2*np.pi], color=ORANGE)
        cos_func = axes_trig.plot(lambda x: np.cos(x), x_range=[-2*np.pi, 2*np.pi], color=PURPLE)
        trig_functions = VGroup(sin_func, cos_func)
        self.play(Create(trig_functions), run_time=3)
        legend_trig = VGroup(
            VGroup(Line(color=ORANGE), Text("sin(x)", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(Line(color=PURPLE), Text("cos(x)", font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(axes_trig, RIGHT)
        self.play(FadeIn(legend_trig))
        self.wait(3)

        self.play(FadeOut(axes), FadeOut(functions), FadeOut(legend),
                  FadeOut(axes_trig), FadeOut(trig_functions), FadeOut(legend_trig),
                  FadeOut(library_eq), FadeOut(step3_title))

        # Step 4: Perform Sparse Regression
        step4_title = Text("4. Perform Sparse Regression", font_size=36).to_edge(UP)
        self.play(Write(step4_title))
        self.wait(2)
        regression_eq = MathTex(r"\dot{\mathbf{X}} = \Theta(\mathbf{X}) \mathbf{\Xi}")
        self.play(Write(regression_eq))
        self.wait(2)
        # Explain the optimization problem
        optimization_eq = MathTex(
            r"\min_{\mathbf{\Xi}} \left\| \dot{\mathbf{X}} - \Theta(\mathbf{X}) \mathbf{\Xi} \right\|_2^2",
            r"+ \lambda \left\| \mathbf{\Xi} \right\|_1"
        )
        self.play(Write(optimization_eq))
        self.wait(3)
        # Visualize sparsity
        xi_matrix = Matrix([
            ["\\xi_{11}", "\\xi_{12}", "\\xi_{13}", "..."],
            ["\\xi_{21}", "\\xi_{22}", "\\xi_{23}", "..."],
            ["\\xi_{31}", "\\xi_{32}", "\\xi_{33}", "..."],
            ["...", "...", "...", "..."]
        ]).shift(2*DOWN)
        zero_entries = VGroup(
            Cross(xi_matrix.get_entries()[1]),
            Cross(xi_matrix.get_entries()[2]),
            Cross(xi_matrix.get_entries()[5]),
            Cross(xi_matrix.get_entries()[6]),
            Cross(xi_matrix.get_entries()[9]),
            Cross(xi_matrix.get_entries()[10])
        )
        self.play(Write(xi_matrix))
        self.wait(1)
        sparsity_text = Text("Sparse coefficients", font_size=28).next_to(xi_matrix, LEFT)
        self.play(Write(sparsity_text))
        self.play(Create(zero_entries))
        self.wait(3)
        self.play(FadeOut(xi_matrix), FadeOut(zero_entries), FadeOut(sparsity_text))
        self.play(FadeOut(regression_eq), FadeOut(optimization_eq), FadeOut(step4_title))

        # Step 5: Obtain Governing Equations
        step5_title = Text("5. Obtain Governing Equations", font_size=36).to_edge(UP)
        self.play(Write(step5_title))
        self.wait(2)
        # Example equation
        example_eq = MathTex(r"\dot{x} = -\omega x")
        self.play(Write(example_eq))
        self.wait(2)
        # Compare data and model prediction
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(DOWN)
        sine_curve = axes.plot(lambda t: np.sin(t), x_range=[0, 10], color=BLUE)
        model_curve = axes.plot(lambda t: np.exp(-t), x_range=[0, 10], color=RED)
        self.play(Create(axes))
        self.play(Create(sine_curve), run_time=3)
        self.play(Create(model_curve), run_time=3)
        legend = VGroup(
            VGroup(Line(color=BLUE), Text("Original Data", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(Line(color=RED), Text("Model Prediction", font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(axes, RIGHT)
        self.play(FadeIn(legend))
        self.wait(3)
        validation_text = VGroup(
            Text("Validate the discovered model by:", font_size=28).shift(1*UP),
            BulletedList(
                "Comparing predicted trajectories with data",
                "Analyzing residuals",
                "Cross-validation",
                font_size=28
            ).next_to(example_eq, DOWN)
        )
        self.play(Write(validation_text))
        self.wait(5)
        self.play(FadeOut(validation_text))
        self.play(FadeOut(axes), FadeOut(sine_curve), FadeOut(model_curve), FadeOut(legend))
        self.play(FadeOut(step5_title), FadeOut(example_eq))

        # Applications
        applications_title = Text("Applications of SINDy", font_size=36).to_edge(UP)
        self.play(Write(applications_title))
        self.wait(2)
        applications_list = BulletedList(
            "Physics (e.g., discovering laws of motion)",
            "Biology (e.g., modeling population dynamics)",
            "Engineering (e.g., control systems)",
            "Economics (e.g., modeling financial systems)",
            "Ecology (e.g., predator-prey models)",
            font_size=28
        ).shift(0.5*DOWN)
        self.play(FadeIn(applications_list, lag_ratio=0.1))
        self.wait(6)
        self.play(FadeOut(applications_title), FadeOut(applications_list))

        # Conclusion
        conclusion_lines = [
            "SINDy allows us to discover the underlying equations",
            "governing a system directly from data.",
            "",
            "It's particularly powerful for systems with sparse dynamics.",
            "",
            "By leveraging sparsity, we obtain interpretable models",
            "that can provide insights into the system's behavior."
        ]
        conclusion_text = VGroup(*[Text(line, font_size=28) for line in conclusion_lines]).arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(conclusion_text, run_time=8))
        self.wait(8)
        self.play(FadeOut(conclusion_text))

        # End Title
        end_title = Text("Thank You!", font_size=48)
        self.play(Write(end_title))
        self.wait(2)
