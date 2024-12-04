from manim import *

class OmicsIntegration(Scene):
    def construct(self):
        # Title
        title = Text("Integration of Omics Data with Genome-Scale Metabolic Models").scale(0.7)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Omics Icons
        genomics_icon = SVGMobject("dna.svg").scale(0.8).shift(LEFT*5 + UP*0.5)
        transcriptomics_icon = SVGMobject("rna.svg").scale(0.8).shift(LEFT*2.5 + UP*0.5)
        proteomics_icon = SVGMobject("protein.svg").scale(0.8).shift(RIGHT*0 + UP*0.5)
        metabolomics_icon = SVGMobject("metabolite.svg").scale(0.8).shift(RIGHT*2.5 + UP*0.5)

        omics_icons = VGroup(genomics_icon, transcriptomics_icon, proteomics_icon, metabolomics_icon)
        self.play(FadeIn(omics_icons, shift=DOWN))
        self.wait(1)

        # Arrows to Metabolic Network
        network_position = DOWN*1.5
        arrows = VGroup(
            Arrow(genomics_icon.get_bottom(), network_position + UP*0.5),
            Arrow(transcriptomics_icon.get_bottom(), network_position + UP*0.5),
            Arrow(proteomics_icon.get_bottom(), network_position + UP*0.5),
            Arrow(metabolomics_icon.get_bottom(), network_position + UP*0.5)
        )
        self.play(Create(arrows))
        self.wait(1)

        # Metabolic Network Representation
        network = Circle(radius=1.5).shift(network_position)
        network_text = Text("Metabolic Network").scale(0.5).move_to(network.get_center())
        self.play(Create(network), Write(network_text))
        self.wait(1)

        # Flux Balance Analysis Equation
        fba_equation = MathTex("Sv = 0").next_to(network, DOWN)
        self.play(Write(fba_equation))
        self.wait(2)