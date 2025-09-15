from manim import *
import numpy as np

class EnhancedPendulumSimulation(Scene):
    def construct(self):
        # Constants
        PENDULUM_LENGTH = 3
        THETA_MAX = PI / 4  # 45 degrees maximum angle
        G = 9.8
        OMEGA = np.sqrt(G / PENDULUM_LENGTH)  # Angular frequency
        PERIOD = 2 * PI / OMEGA
        PIVOT_POINT = 2 * UP  # Higher pivot for better visibility

        # Time tracking
        time = ValueTracker(0)

        # Starting Text
        starting_text = Text(
            "The time period of a pendulum doesn't depend on its amplitude,\n"
            "but only on its length and the gravitational acceleration.",
            font_size=24
        )
        
        # Animating starting
        self.play(Write(starting_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(starting_text))

        # Pendulum components
        def bob_position():
            theta = THETA_MAX * np.sin(OMEGA * time.get_value())
            return PIVOT_POINT + PENDULUM_LENGTH * np.array([
                np.sin(theta),
                -np.cos(theta),
                0
            ])

        # Create pivot
        pivot = Circle(radius=0.1, color=RED, fill_opacity=1).move_to(PIVOT_POINT)
        
        # Create string
        string = always_redraw(lambda: Line(
            start=PIVOT_POINT,
            end=bob_position(),
            color=BLUE,
            stroke_width=2
        ))

        # Create bob with shadow
        bob = always_redraw(lambda: Circle(
            radius=0.2,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=3
        ).move_to(bob_position()))
        
        shadow = always_redraw(lambda: Circle(
            radius=0.18,
            fill_color=BLACK,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(bob_position() + 0.05 * DOWN))

        # Reference line
        center_line = DashedLine(
            start=PIVOT_POINT,
            end=PIVOT_POINT + 3 * DOWN,
            color=GREY
        )

        # Angle indicator
        angle_arc = always_redraw(lambda: Arc(
            radius=0.5,
            start_angle=PI/2,  # from vertical
            angle=-THETA_MAX * np.sin(OMEGA * time.get_value()),
            arc_center=PIVOT_POINT,
            color=YELLOW,
            stroke_width=3
        ))

        angle_label = always_redraw(lambda: MathTex(
            f"{np.degrees(THETA_MAX * np.sin(OMEGA * time.get_value())):.1f}^\\circ",
            color=YELLOW
        ).next_to(angle_arc.point_from_proportion(0.5), UR, buff=0.1))

        # Angle measurement lines
        def create_angle_lines():
            current_angle = THETA_MAX * np.sin(OMEGA * time.get_value())
            line1 = Line(PIVOT_POINT, PIVOT_POINT + 0.8 * DOWN, color=GREY)
            line2 = Line(PIVOT_POINT, bob_position(), color=GREY)
            return VGroup(line1, line2)

        angle_lines = always_redraw(create_angle_lines)

        # Time display
        time_text = always_redraw(lambda: DecimalNumber(
            time.get_value(),
            num_decimal_places=2,
            color=WHITE
        ).to_edge(LEFT).shift(DOWN))

        time_label = Text("Time (s): ", font_size=24).next_to(time_text, LEFT)
        
        # Period counter
        period_count = always_redraw(lambda: Integer(
            int(time.get_value() / PERIOD),
            color=WHITE
        ).next_to(time_text, RIGHT).shift(0.5*RIGHT))

        period_label = Text("Periods: ", font_size=24).next_to(period_count, LEFT)

        # Formula display
        formula = MathTex("T = 2\\pi\\sqrt{\\frac{L}{g}}", font_size=32).to_edge(UR)

        # Trail effect
        trail = TracedPath(bob.get_center, stroke_color=YELLOW, stroke_width=2, stroke_opacity=0.6)

        # Energy visualization
        def create_energy_bars():
            time_val = time.get_value()
            theta = THETA_MAX * np.sin(OMEGA * time_val)
            omega_val = THETA_MAX * OMEGA * np.cos(OMEGA * time_val)
            
            # Kinetic energy (proportional to ω²)
            ke_height = 2 * (omega_val**2) / (THETA_MAX * OMEGA)**2
            ke_bar = Rectangle(
                height=ke_height, width=0.5, 
                fill_color=BLUE, fill_opacity=0.8,
                stroke_color=WHITE
            ).to_edge(DOWN).shift(2*LEFT)
            
            # Potential energy (proportional to height)
            height = PENDULUM_LENGTH * (1 - np.cos(theta))
            pe_height = 2 * height / (PENDULUM_LENGTH * (1 - np.cos(THETA_MAX)))
            pe_bar = Rectangle(
                height=pe_height, width=0.5, 
                fill_color=RED, fill_opacity=0.8,
                stroke_color=WHITE
            ).next_to(ke_bar, RIGHT, buff=0.5)
            
            return VGroup(ke_bar, pe_bar)

        energy_bars = always_redraw(create_energy_bars)
        energy_labels = VGroup(
            Text("Kinetic", font_size=16).next_to(energy_bars[0], DOWN),
            Text("Potential", font_size=16).next_to(energy_bars[1], DOWN)
        )

        # Build pendulum
        self.play(
            LaggedStart(
                Create(pivot),
                Create(center_line),
                GrowFromPoint(string, PIVOT_POINT),
                FadeIn(bob),
                FadeIn(shadow),
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        
        self.add(angle_arc, angle_label, angle_lines, time_label, time_text, 
                 period_label, period_count, formula, trail, energy_bars, energy_labels)

        # Pendulum motion
        self.play(
            time.animate.set_value(3 * PERIOD),
            rate_func=linear,
            run_time=3 * PERIOD
        )

        # Pendulum fade out
        self.play(FadeOut(
            bob, shadow, string, center_line, angle_arc, angle_label, 
            angle_lines, pivot, trail, energy_bars, energy_labels
        ))

        # Enhanced conclusion
        conclusion_title = Text("Simple Pendulum Properties:", font_size=32)
        conclusion_list = VGroup(
            MathTex("T = 2\\pi\\sqrt{\\frac{L}{g}}", font_size=32),
            Text("• Period depends only on length (L) and gravity (g)", font_size=24),
            Text("• Amplitude doesn't affect period for small angles", font_size=24),
            Text("• Motion follows simple harmonic oscillation", font_size=24),
            Text("• Energy converts between kinetic and potential forms", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        conclusion = VGroup(conclusion_title, conclusion_list).arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(conclusion), run_time=3)
        self.wait(3)