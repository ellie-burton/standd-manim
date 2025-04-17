from manim import *
import random

class UnitedStatesMap(VGroup):
    def __init__(self, svg_path="us_states.svg", scale_factor=2.5, default_color=GRAY, **kwargs):
        super().__init__(**kwargs)
        self.svg_path = svg_path
        self.default_color = default_color
        self.highlight_color = YELLOW
        self.scale_factor = scale_factor

        self.map = SVGMobject(self.svg_path, fill_opacity=1, stroke_width=0.5)
        self.map.scale(self.scale_factor)

        state_codes = [
            "MA", "MN", "MT", "ND", "HI", "ID", "WA", "AZ", "CA", "CO",
            "NV", "NM", "OR", "UT", "WY", "AR", "IA", "KS", "MO", "NE",
            "OK", "SD", "LA", "TX", "CT", "NH", "RI", "VT", "AL", "FL",
            "GA", "MS", "SC", "IL", "IN", "KY", "NC", "OH", "TN", "VA",
            "WI", "WV", "DE", "DC", "MD", "NJ", "NY", "PA", "ME", "MI", "AK"
        ]

        self.state_dict = {}
        for state_obj, code in zip(self.map.submobjects, state_codes):
            state_obj.set_fill(self.default_color, opacity=1)
            self.state_dict[code] = state_obj

        self.add(self.map)

    def highlight_states(self, state_list, color=YELLOW):
        return [self.state_dict[s].animate.set_fill(color) for s in state_list if s in self.state_dict]

    def unhighlight_states(self, state_list, color=None):
        if color is None:
            color = self.default_color
        return [self.state_dict[s].animate.set_fill(color, opacity=1) for s in state_list if s in self.state_dict]

class HighlightMapScene(Scene):
    def construct(self):
        us_map = UnitedStatesMap(svg_path="us_states.svg")
        us_map.move_to(ORIGIN)
        self.play(FadeIn(us_map), run_time=0.5)

        step1_text = Text("We may see the same image in multiple ads\nin nearby states.", font_size=24).to_edge(UP)
        self.play(Write(step1_text))

        real_person = ImageMobject("real_person.png").scale(0.5)
        real_person.to_edge(RIGHT, buff=1)
        self.play(FadeIn(real_person), run_time=0.5)

        nearby_states_sequence = ["AL", "TN", "AL", "GA", "MS", "AL"]
        final_states = set()
        arrows = []
        for state in nearby_states_sequence:
            state_center = us_map.state_dict[state].get_center()
            arrow = Arrow(start=real_person.get_left(), end=state_center, buff=0.1, stroke_width=2, color=BLUE)
            self.play(
                us_map.state_dict[state].animate.set_fill(YELLOW),
                Create(arrow),
                run_time=0.5
            )
            arrows.append(arrow)
            self.wait(0.3)
            self.play(FadeOut(arrow), us_map.state_dict[state].animate.set_fill(us_map.default_color), run_time=0.5)
            final_states.add(state)
        
        self.play(FadeOut(step1_text))

        link_text = Text("Through our algorithm, we will link these ads\nto be the same individual.", font_size=24).to_edge(UP)
        self.play(Write(link_text))
        self.wait(1)

        self.play(*us_map.highlight_states(list(final_states)), run_time=1)
        self.wait(1)
        self.play(FadeOut(link_text))

        step2_text = Text("However, if a separate individual across the country\nsteals this image, we encounter an issue of false linkages.", font_size=24).to_edge(UP)
        self.play(Write(step2_text))

        new_image_position = us_map.get_left() + LEFT * 0.25
        self.play(real_person.animate.move_to(new_image_position), run_time=1.5)

        ca_center = us_map.state_dict["CA"].get_center()
        ca_arrow = Arrow(start=real_person.get_right(), end=ca_center, buff=0.1, stroke_width=2, color=BLUE)
        self.play(
            us_map.state_dict["CA"].animate.set_fill(YELLOW),
            Create(ca_arrow),
            run_time=1
        )

        self.wait(1)
        self.play(FadeOut(step2_text))
        self.wait(0.5)

        step3_text = Text("Generic content, scams, and stolen images\ntie up individuals nationwide", font_size=24).to_edge(UP)
        self.play(Write(step3_text))

        snapchat_logo = ImageMobject("snapchat.jpg").scale(0.5).to_corner(DL, buff=1)
        generic_text = ImageMobject("generic_text.png").scale(0.5).to_corner(DR, buff=1)
        self.play(FadeIn(snapchat_logo), FadeIn(generic_text), run_time=0.5)

        all_states = list(us_map.state_dict.keys())
        random.shuffle(all_states)

        for state in all_states:
            self.play(*us_map.highlight_states([state]), run_time=0.05)

        self.wait(1)

        self.play(
            FadeOut(snapchat_logo), 
            FadeOut(generic_text), 
            FadeOut(real_person), 
            FadeOut(ca_arrow),
            run_time=1
        )
        self.play(FadeOut(us_map), FadeOut(step3_text), run_time=1)
        self.wait(1)
