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
        
        # Generate sample functions from the prior
        x = np.linspace(-3, 3, 100)
        functions = self.sample_gaussian_process(x)
        
        # Plot the sample functions
        function_plots = VGroup()
        colors = [BLUE, GREEN, RED, ORANGE, PURPLE]
        for i, f in enumerate(functions):
            y = f
            plot = axes.plot_line_graph(x, y, add_vertex_dots=False, line_color=colors[i % len(colors)])
            function_plots.add(plot)
        
        self.play(*[Create(plot) for plot in function_plots], run_time=2)
        self.wait(2)
        
        # Introduce data points
        data_x = np.array([-2, -1, 0, 1, 2])
        data_y = np.sin(data_x)  # For example purposes
        data_points = VGroup(*[Dot(axes.c2p(xi, yi), color=YELLOW) for xi, yi in zip(data_x, data_y)])
        self.play(Create(data_points))
        self.wait(1)
        
        # Generate sample functions from the posterior
        functions_post = self.sample_gaussian_process_posterior(x, data_x, data_y)
        
        # Remove prior functions
        self.play(*[Uncreate(plot) for plot in function_plots], run_time=1)
        
        # Plot posterior sample functions
        function_plots_post = VGroup()
        for i, f in enumerate(functions_post):
            y = f
            plot = axes.plot_line_graph(x, y, add_vertex_dots=False, line_color=colors[i % len(colors)])
            function_plots_post.add(plot)
        
        self.play(*[Create(plot) for plot in function_plots_post], run_time=2)
        self.wait(2)

    def sample_gaussian_process(self, x, n_samples=5):
        # Define kernel function (RBF kernel)
        def kernel(a, b, length_scale=1.0, sigma_f=1.0):
            sqdist = cdist(a.reshape(-1,1), b.reshape(-1,1), 'sqeuclidean')
            return sigma_f ** 2 * np.exp(-0.5 / length_scale ** 2 * sqdist)
        
        # Mean and covariance
        mean = np.zeros_like(x)
        cov = kernel(x, x)
        
        # Sample from multivariate normal
        samples = np.random.multivariate_normal(mean, cov, n_samples)
        return samples

    def sample_gaussian_process_posterior(self, x, x_train, y_train, n_samples=5):
        # Define kernel function (RBF kernel)
        def kernel(a, b, length_scale=1.0, sigma_f=1.0):
            sqdist = cdist(a.reshape(-1,1), b.reshape(-1,1), 'sqeuclidean')
            return sigma_f ** 2 * np.exp(-0.5 / length_scale ** 2 * sqdist)
        
        K = kernel(x_train, x_train)
        K_s = kernel(x_train, x)
        K_ss = kernel(x, x)
        K_inv = np.linalg.inv(K + 1e-8 * np.eye(len(x_train)))
        
        # Compute the mean and covariance of the posterior distribution
        mu_s = K_s.T.dot(K_inv).dot(y_train)
        cov_s = K_ss - K_s.T.dot(K_inv).dot(K_s)
        
        # Sample from the posterior
        samples = np.random.multivariate_normal(mu_s, cov_s, n_samples)
        return samples
