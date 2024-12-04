from manim import *

class EcologicalModelling(Scene):
    def construct(self):
        # Title
        title = Text("Ecological Modelling of Microbial Communities").scale(0.7)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Lotka-Volterra Equations
        equations = MathTex(
            r"\frac{dx}{dt} = \alpha x - \beta x y",
            r"\frac{dy}{dt} = \delta x y - \gamma y"
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP*0.5)
        self.play(Write(equations))
        self.wait(2)

        # Predator and Prey Icons
        prey_icon = SVGMobject("fish.svg").scale(1).set_color(BLUE).shift(LEFT*3 + DOWN*1)
        predator_icon = SVGMobject("shark.svg").scale(1).set_color(RED).shift(RIGHT*3 + DOWN*1)
        self.play(FadeIn(prey_icon), FadeIn(predator_icon))
        self.wait(1)

        # Simulate Population Changes
        prey_population = ValueTracker(5)
        predator_population = ValueTracker(2)

        prey_counter = always_redraw(lambda: Integer(
            int(prey_population.get_value()),
            color=BLUE
        ).scale(1).next_to(prey_icon, DOWN))

        predator_counter = always_redraw(lambda: Integer(
            int(predator_population.get_value()),
            color=RED
        ).scale(1).next_to(predator_icon, DOWN))

        self.play(Write(prey_counter), Write(predator_counter))
        self.wait(1)

        # Animate Population Dynamics
        for _ in range(5):
            self.play(
                prey_population.animate.set_value(prey_population.get_value() * 1.2),
                predator_population.animate.set_value(predator_population.get_value() * 1.1),
                run_time=0.5
            )
            self.play(
                prey_population.animate.set_value(prey_population.get_value() * 0.8),
                predator_population.animate.set_value(predator_population.get_value() * 0.9),
                run_time=0.5
            )
        self.wait(2)
