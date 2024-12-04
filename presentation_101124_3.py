from manim import *

class ExperimentalAI(Scene):
    def construct(self):
        # Title
        title = Text("Experimental Validation and AI for Data-Driven Microbial Ecology").scale(0.6)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Laboratory Icon
        lab_icon = SVGMobject("lab.svg").scale(1).shift(LEFT*3 + DOWN*0.5)
        self.play(FadeIn(lab_icon, shift=RIGHT))
        self.wait(1)

        # AI Icon
        ai_icon = SVGMobject("ai.svg").scale(1).shift(RIGHT*3 + DOWN*0.5)
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