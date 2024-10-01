from manim import *

config.pixel_height = 2160  # Set to 4K resolution (2160p)
config.pixel_width = 3840
config.frame_rate = 60      # Higher frame rate for smoother animation
config.quality = "production_quality"

class FBA3DPolytope(ThreeDScene):
    def construct(self):
        # Define maximum values based on vertex coordinates
        max_x = 8
        max_y = 8
        max_z = 8

        # Create the 3D axes for the flux variables v1, v2, and v3
        axes = ThreeDAxes(
            x_range=[0, max_x, 5], 
            y_range=[0, max_y, 5], 
            z_range=[0, max_z, 5], 
            axis_config={"color": BLUE},
            x_length=6,  # Adjust physical length for better scaling
            y_length=6,
            z_length=6
        )
        labels = axes.get_axis_labels(x_label="v_{1}", y_label="v_{2}", z_label="v_{3}")

        # Rotate camera to get a better view angle of the 3D space
        self.set_camera_orientation(phi=22.5 * DEGREES, theta=0 * DEGREES, zoom=0.7, frame_center=(-2,2,0))

        # Rotate labels to face the camera
        for label in labels:
            label.rotate(0 * DEGREES, axis=RIGHT)  # Aligns with the camera's phi angle
            label.rotate(0 * DEGREES, axis=OUT)    # Aligns with the camera's theta angle

        # Display the axes and labels
        self.play(Create(axes), Write(labels))
        self.wait(1)

        # Define vertices of the polytope
        vertices = [
            axes.coords_to_point(0, 0, 0),          # Point (0, 0, 0)
            axes.coords_to_point(3,2,6),   # Point (8.5, 12.3, 9.8)
            axes.coords_to_point(2,3,6),  # Point (15.2, 7.6, 18.4)
            axes.coords_to_point(1,3,5), # Point (22.7, 19.4, 14.1)
            axes.coords_to_point(1,2,4), # Point (11.3, 25.8, 20.5)
            axes.coords_to_point(2,1,4), # Point (17.6, 13.9, 24.3)
            axes.coords_to_point(3,1,5) , # Point (14.4, 21.2, 17.7)
        ]

        # Create faces of the polytope
        faces = [
            [vertices[0], vertices[1], vertices[2]],
            [vertices[0], vertices[2], vertices[3]],
            [vertices[0], vertices[3], vertices[4]],
            [vertices[0], vertices[4], vertices[5]],
            [vertices[0], vertices[5], vertices[6]],
            [vertices[0], vertices[6], vertices[1]]
        ]

        # Animate the creation of the polytope with semi-transparent faces
        for face in faces:
            polygon = Polygon(*face, color=BLUE, fill_opacity=0.3, stroke_color=WHITE, sheen_factor=1)
            self.play(Create(polygon), run_time=0.5)

        self.wait(1)

        # Optimal solution point (somewhere on the polytope)
        optimal_solution = Dot3D(
            axes.coords_to_point(2,1,4),  # Example coordinates of optimal point
            color=YELLOW,
            radius=0.2
        )

        # Mark the optimal solution
        self.play(FadeIn(optimal_solution))
        self.wait(0.5)

        # Add a label for the optimal solution
        optimal_label = Text("Optimal Solution").scale(0.5).next_to(optimal_solution, UP)

         # Rotate the optimal solution label to face the camera
        optimal_label.rotate(-65 * DEGREES, axis=RIGHT)  # Align with the camera's phi angle
        optimal_label.rotate(15 * DEGREES, axis=OUT)    # Align with the camera's theta angle

        self.play(Write(optimal_label))
        self.wait(2)
