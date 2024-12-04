from manim import *

class MicrobialEcologyAnimation(Scene):
    def construct(self):
        # Slide 1: Ecological Modelling of Microbial Communities
        self.slide1()
        self.wait(2)
        self.clear()

        # Slide 2: Integration of Omics Data with Genome-Scale Metabolic Models
        self.slide2()
        self.wait(2)
        self.clear()

        # Slide 3: Experimental Validation and AI for Data-Driven Microbial Ecology
        self.slide3()
        self.wait(2)

    def slide1(self):
        # Title
        title = Text("Ecological Modelling of Microbial Communities")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Lotka-Volterra Equations
        equations = MathTex(
            r"\frac{dx}{dt} = \alpha x - \beta x y",
            r"\frac{dy}{dt} = \delta x y - \gamma y"
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(equations))
        self.wait(2)

        # Predator and Prey Icons
        prey_icon = SVGMobject("fish.svg").scale(0.5).set_color(BLUE).shift(LEFT*3 + DOWN)
        predator_icon = SVGMobject("shark.svg").scale(0.5).set_color(RED).shift(RIGHT*3 + DOWN)
        self.play(FadeIn(prey_icon), FadeIn(predator_icon))
        self.wait(1)

        # Simulate Population Changes
        prey_population = ValueTracker(5)
        predator_population = ValueTracker(2)

        prey_counter = always_redraw(lambda: Integer(
            int(prey_population.get_value()),
            color=BLUE
        ).next_to(prey_icon, DOWN))

        predator_counter = always_redraw(lambda: Integer(
            int(predator_population.get_value()),
            color=RED
        ).next_to(predator_icon, DOWN))

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

    def slide2(self):
        # Title
        title = Text("Integration of Omics Data with Genome-Scale Metabolic Models")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Omics Icons
        genomics_icon = SVGMobject("dna.svg").scale(0.5).shift(LEFT*4 + UP)
        transcriptomics_icon = SVGMobject("rna.svg").scale(0.5).shift(LEFT*2 + UP)
        proteomics_icon = SVGMobject("protein.svg").scale(0.5).shift(ORIGIN + UP)
        metabolomics_icon = SVGMobject("metabolite.svg").scale(0.5).shift(RIGHT*2 + UP)

        omics_icons = VGroup(genomics_icon, transcriptomics_icon, proteomics_icon, metabolomics_icon)
        self.play(FadeIn(omics_icons, shift=DOWN))
        self.wait(1)

        # Arrows to Metabolic Network
        arrows = VGroup(
            Arrow(genomics_icon.get_bottom(), DOWN*1),
            Arrow(transcriptomics_icon.get_bottom(), DOWN*1),
            Arrow(proteomics_icon.get_bottom(), DOWN*1),
            Arrow(metabolomics_icon.get_bottom(), DOWN*1)
        )
        self.play(Create(arrows))
        self.wait(1)

        # Metabolic Network Representation
        network = Circle(radius=1).shift(DOWN*1.5)
        network_text = Text("Metabolic Network").scale(0.5).move_to(network.get_center())
        self.play(Create(network), Write(network_text))
        self.wait(1)

        # Flux Balance Analysis Equation
        fba_equation = MathTex("Sv = 0").next_to(network, DOWN)
        self.play(Write(fba_equation))
        self.wait(2)

    def slide3(self):
        # Title
        title = Text("Experimental Validation and AI for Data-Driven Microbial Ecology")
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Laboratory Icon
        lab_icon = SVGMobject("lab.svg").scale(0.7).shift(LEFT*3 + DOWN*0.5)
        self.play(FadeIn(lab_icon, shift=RIGHT))
        self.wait(1)

        # AI Icon
        ai_icon = SVGMobject("ai.svg").scale(0.7).shift(RIGHT*3 + DOWN*0.5)
        self.play(FadeIn(ai_icon, shift=LEFT))
        self.wait(1)

        # Data Flow Animation
        data_arrow = Arrow(lab_icon.get_right(), ai_icon.get_left(), buff=0.1).set_color(YELLOW)
        self.play(Create(data_arrow))
        self.wait(1)

        # Data Processing Animation
        data_processing = Text("Data Processing", color=YELLOW).scale(0.5).next_to(data_arrow, UP)
        self.play(Write(data_processing))
        self.wait(1)

        # AI Prediction Equation
        ai_equation = MathTex(r"\hat{y} = f_{\theta}(x)").next_to(ai_icon, DOWN)
        self.play(Write(ai_equation))
        self.wait(2)