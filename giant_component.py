from manim import *
import numpy as np
import random

class GiantComponentScene(Scene):
    def construct(self):
        title = Text("Let's look at a small set of data.", font_size=24).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Create icon-like central nodes and spokes (image/phone/text representation)
        num_clusters = 8
        nodes_per_cluster = 6
        all_nodes = []
        node_groups = []
        edges = []
        cluster_radius = 0.8
        node_radius = 0.12
        center_radius = 3.0
        vertical_offset = 1.5  # shift nodes downward to avoid overlapping text

        for i in range(num_clusters):
            cluster_nodes = []
            cluster_angle = 2 * np.pi * i / num_clusters
            cluster_center = center_radius * np.array([np.cos(cluster_angle), np.sin(cluster_angle), 0]) + DOWN * vertical_offset

            # Create a central node (red, to visually separate)
            center_node = Dot(cluster_center, radius=node_radius + 0.05, color=RED)
            cluster_nodes.append(center_node)
            all_nodes.append(center_node)

            # Add outer nodes (images/phones/etc.) around the center
            for j in range(1, nodes_per_cluster):
                theta = j * 2 * np.pi / (nodes_per_cluster - 1)
                pos = cluster_center + cluster_radius * np.array([np.cos(theta), np.sin(theta), 0])
                node = Dot(pos, radius=node_radius, color=WHITE)
                cluster_nodes.append(node)
                all_nodes.append(node)
            node_groups.append(cluster_nodes)

        # Show nodes
        for group in node_groups:
            self.play(*[FadeIn(node) for node in group], run_time=0.3)

        # Connect outer nodes to central node
        for group in node_groups:
            central_node = group[0]
            local_edges = []
            for node in group[1:]:
                line = Line(central_node.get_center(), node.get_center(), color=WHITE, stroke_width=2)
                local_edges.append(line)
            edges.extend(local_edges)
            self.play(*[Create(edge) for edge in local_edges], run_time=0.4)

        self.wait(1)
        self.play(FadeOut(title))
        warning = Text("But, the issues we saw earlier can cause clusters to get falsely linked?", font_size=24).to_edge(UP)
        self.play(Write(warning))
        self.wait(1)

        # Cross-links between central nodes (false connections)
        cross_links = []
        central_nodes = [group[0] for group in node_groups]
        for _ in range(8):
            node1, node2 = random.sample(central_nodes, 2)
            link = Line(node1.get_center(), node2.get_center(), color=RED, stroke_width=2)
            cross_links.append(link)
        self.play(*[Create(link) for link in cross_links], run_time=2)

        self.wait(1)
        self.play(FadeOut(warning))

        insight_text = Text("Now we can’t tell who’s who. Insights are lost.", font_size=24).to_edge(UP)
        self.play(Transform(warning, insight_text))
        self.wait(2)

        # Optional: subtle jitter for organic look
        self.play(*[node.animate.shift(0.05 * RIGHT * np.random.randn() + 0.05 * UP * np.random.randn()) for node in all_nodes], run_time=1)
        self.wait(1)

        # Fade everything out
        self.play(FadeOut(title), FadeOut(insight_text),
                  *[FadeOut(mob) for mob in all_nodes + edges + cross_links])
        self.wait(1)

