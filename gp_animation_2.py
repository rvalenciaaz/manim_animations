from manim import *
import numpy as np
from scipy.spatial.distance import cdist

class GaussianProcessVisualization(Scene):
    def construct(self):
        # Set up the axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        
        self.play(Create(axes))
        
        # Display the prior equations
        prior_equation = MathTex(
            r"f(x) \sim \mathcal{GP}\left(0, k(x, x')\right)"
        ).scale(0.6).to_edge(UP).shift(RIGHT * 3)
        kernel_equation = MathTex(
            r"k(x, x') = \sigma_f^2 \exp\left(-\frac{(x - x')^2}{2\ell^2}\right)"
        ).scale(0.6).next_to(prior_equation, DOWN)
        
        self.play(Write(prior_equation))
        self.play(Write(kernel_equation))
        self.wait(2)
        
        # Generate sample functions from the prior
        x = np.linspace(-3, 3, 200)
        functions = self.sample_gaussian_process(x)
        
        # Plot the sample functions
        function_plots = VGroup()
        colors = [BLUE, GREEN, RED, ORANGE, PURPLE]
        for i, f in enumerate(functions):
            y = f
            plot = axes.plot_line_graph(
                x, y, add_vertex_dots=False, line_color=colors[i % len(colors)]
            )
            function_plots.add(plot)
        
        self.play(*[Create(plot) for plot in function_plots], run_time=2)
        self.wait(2)
        
        # Remove prior functions
        self.play(*[Uncreate(plot) for plot in function_plots], run_time=1)
        self.wait(1)  # Pause before showing data points

        # Display the posterior equations
        self.play(FadeOut(prior_equation), FadeOut(kernel_equation))
        
        # Introduce data points
        data_x = np.array([-2, -1, 0, 1, 2])
        data_y = np.sin(data_x)  # For example purposes
        data_points = VGroup(
            *[Dot(axes.c2p(xi, yi), color=YELLOW) for xi, yi in zip(data_x, data_y)]
        )
        self.play(Create(data_points))
        self.wait(2)
        
        
        posterior_equation = MathTex(
            r"f(x^*) \mid \mathbf{x}, \mathbf{y} \sim \mathcal{N}(\mu(x^*), \sigma^2(x^*))"
        ).scale(0.5).to_edge(UP).shift(RIGHT * 3)
        mean_equation = MathTex(
            r"\mu(x^*) = K_{x^*x}\left(K_{xx} + \sigma_n^2 I\right)^{-1}\mathbf{y}"
        ).scale(0.5).next_to(posterior_equation, DOWN)
        variance_equation = MathTex(
            r"\sigma^2(x^*) = K_{x^*x^*} - K_{x^*x}\left(K_{xx} + \sigma_n^2 I\right)^{-1}K_{xx^*}"
        ).scale(0.5).next_to(mean_equation, DOWN)
        self.play(Write(posterior_equation))
        self.play(Write(mean_equation))
        self.play(Write(variance_equation))
        self.wait(2)
        
        # Generate sample functions from the posterior
        functions_post, mu_s, std_s = self.sample_gaussian_process_posterior(
            x, data_x, data_y
        )
        
        # Plot the confidence intervals
        upper = mu_s + 2 * std_s
        lower = mu_s - 2 * std_s
        ci_polygon = self.get_confidence_interval(axes, x, upper, lower)
        ci_polygon.set_fill(BLUE, opacity=0.2)
        ci_polygon.set_stroke(width=0)
        
        self.play(FadeIn(ci_polygon))
        
        # Plot the posterior mean
        mean_plot = axes.plot_line_graph(
            x, mu_s, add_vertex_dots=False, line_color=BLACK
        )
        self.play(Create(mean_plot))
        
        # Plot posterior sample functions
        function_plots_post = VGroup()
        for i, f in enumerate(functions_post):
            y = f
            plot = axes.plot_line_graph(
                x,
                y,
                add_vertex_dots=False,
                line_color=colors[i % len(colors)],
                stroke_opacity=0.6,
            )
            function_plots_post.add(plot)
        
        self.play(*[Create(plot) for plot in function_plots_post], run_time=2)
        self.wait(2)
    
    def sample_gaussian_process(self, x, n_samples=5):
        # Define kernel function (RBF kernel)
        def kernel(a, b, length_scale=1.0, sigma_f=1.0):
            sqdist = cdist(a.reshape(-1, 1), b.reshape(-1, 1), "sqeuclidean")
            return sigma_f ** 2 * np.exp(-0.5 / length_scale ** 2 * sqdist)
        
        # Mean and covariance
        mean = np.zeros_like(x)
        cov = kernel(x, x)
        
        # Sample from multivariate normal
        samples = np.random.multivariate_normal(
            mean, cov + 1e-8 * np.eye(len(cov)), n_samples
        )
        return samples
    
    def sample_gaussian_process_posterior(self, x, x_train, y_train, n_samples=5):
        # Define kernel function (RBF kernel)
        def kernel(a, b, length_scale=1.0, sigma_f=1.0):
            sqdist = cdist(a.reshape(-1, 1), b.reshape(-1, 1), "sqeuclidean")
            return sigma_f ** 2 * np.exp(-0.5 / length_scale ** 2 * sqdist)
        
        K = kernel(x_train, x_train)
        K_s = kernel(x_train, x)
        K_ss = kernel(x, x)
        sigma_n = 0.1  # Noise term
        K_inv = np.linalg.inv(K + sigma_n ** 2 * np.eye(len(x_train)))
        
        # Compute the mean and covariance of the posterior distribution
        mu_s = K_s.T.dot(K_inv).dot(y_train)
        cov_s = K_ss - K_s.T.dot(K_inv).dot(K_s)
        std_s = np.sqrt(np.diag(cov_s))
        
        # Sample from the posterior
        samples = np.random.multivariate_normal(
            mu_s, cov_s + 1e-8 * np.eye(len(cov_s)), n_samples
        )
        return samples, mu_s, std_s
    
    def get_confidence_interval(self, axes, x, upper, lower):
        # Create a polygon representing the confidence interval
        points = np.vstack(
            (np.column_stack((x, upper)), np.column_stack((x[::-1], lower[::-1])))
        )
        points = [axes.c2p(px, py) for px, py in points]
        polygon = Polygon(*points, color=BLUE, fill_opacity=0.2, stroke_width=0)
        return polygon
