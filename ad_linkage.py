from manim import *
import numpy as np

class AdLinkingVisualization(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define colors as instance variables so they're available in all methods
        self.node_color = "#2C73D2"
        self.text_node_color = "#FF6F61"
        self.highlight_color = "#27AE60"
    
    def construct(self):
        # Step 1: Create the first ad box
        self.create_first_ad()
        
        # Step 2: Transform ad elements into circular nodes
        self.transform_ad_to_nodes()
        
        # Step 3: Connect nodes into a graph structure
        self.connect_nodes_in_graph()
        
        # Step 4: Create second ad
        self.create_second_ad()
        
        # Step 5: Highlight matching nodes
        self.highlight_matching_nodes()
        
        # Step 6: Merge the graphs
        self.merge_graphs()
    
    def create_person_icon(self, height=1, width=1.5, color=WHITE):
        # Create visible border box for the person icon
        border = Rectangle(height=height, width=width, color=color)
        
        # Calculate proportions
        head_radius = height * 0.2
        body_width = width * 0.6
        
        # Head (circle)
        head = Circle(radius=head_radius, color=color, fill_opacity=1)
        head_position = border.get_top() + DOWN * head_radius * 1.5
        head.move_to(head_position)
        
        # Body (semi-circle facing down)
        
        # Create body using a half-circle
        # The body is a half-circle facing down
        # The angle is set to PI (180 degrees)
        body = Arc(radius=body_width/3, angle=PI, color=color, fill_opacity=1)
        
        # Move the body to the top of the head
        body_top = head.get_bottom() + DOWN * 0.05  # Adjust the position slightly below the head
        body.move_to(body_top)

        #body.move_to(body_top + DOWN * (body_width/2 - 0.05))
        
        # Create "Image" text label
        image_label = Text("Image", font_size=18, color=color)
        image_label.next_to(border, DOWN, buff=0.1)
        
        # Group everything including the border and label
        person = VGroup(border, head, body, image_label)
        
        return person
        
    def create_first_ad(self):
        # Clear any previous text first        
        step1_text = Text("We start with web scraped data of commerial sex ads.").scale(0.8).to_edge(UP)
        self.play(Write(step1_text))
        self.step1_text = step1_text
        
        # Create Ad 1 box
        ad1_box = Rectangle(height=4, width=5, color=WHITE)
        ad1_label = Text("Ad 1", color=WHITE).next_to(ad1_box, UP)
        
        # Ad content
        ad_title = Text("Escort Ad 1", color=WHITE, font_size=24)
        ad_text = Text("Example Ad Text", color=WHITE, font_size=20)
        phone = Text("XXX-XXX-XXXX", color=WHITE, font_size=20)
        
        # Image placeholders with person icon
        img1 = self.create_person_icon(1, 1.5, WHITE)
        img2 = self.create_person_icon(1, 1.5, WHITE)
        
        # Position elements
        ad_title.next_to(ad1_box.get_top(), DOWN, buff=0.3)
        ad_text.next_to(ad_title, DOWN, buff=0.2)
        phone.next_to(ad_text, DOWN, buff=0.2)
        
        img1.next_to(phone, DOWN, buff=0.2).shift(LEFT * 1)
        img2.next_to(phone, DOWN, buff=0.2).shift(RIGHT * 1)
        
        # Group all ad elements
        ad1_content = VGroup(ad_title, ad_text, phone, img1, img2)
        ad1_content.move_to(ad1_box.get_center())
        
        self.ad1_elements = [ad_title, ad_text, phone, img1, img2]
        self.ad1_box = ad1_box
        self.ad1_label = ad1_label
        
        # Show the ad
        self.play(
            Create(ad1_box),
            Write(ad1_label)
        )
        self.play(
            Write(ad_title),
            Write(ad_text),
            Write(phone),
            Create(img1),
            Create(img2),
            run_time=2
        )
        self.wait()
    
    def transform_ad_to_nodes(self):
        # Ensure the previous text is fully faded out before the new one appears
        step2_text = Text("Each piece of information can \nbe represented as a data point.").scale(0.8).to_edge(UP)
        self.play(
            FadeOut(self.step1_text, run_time=0.5),
        )
        self.play(
            Write(step2_text)
        )
        self.step2_text = step2_text
        
        # Create nodes for each ad element
        nodes = []
        node_labels = []
        
        # Define node positions (in a circular arrangement)
        center = self.ad1_box.get_center()
        radius = 1.5
        angles = np.linspace(0, 2 * np.pi, len(self.ad1_elements), endpoint=False)
        positions = [center + radius * np.array([np.cos(angle), np.sin(angle), 0]) for angle in angles]
        
        # Pre-create all the circles and labels at the exact positions
        for i, element in enumerate(self.ad1_elements):
            if i == 0:  # Title node (will be the center node)
                node = Circle(radius=0.4, color=self.text_node_color, fill_opacity=0.7)
                label = Text("Title", font_size=16)
            elif i == 1:  # Description
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text("Text", font_size=16)
            elif i == 2:  # Phone
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text("Phone", font_size=16)
            else:  # Images
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text(f"Img{i-2}", font_size=16)
            
            # Position the node and label precisely
            node.move_to(positions[i])
            label.move_to(node.get_center())
            nodes.append(node)
            node_labels.append(label)
        
        # For a cleaner transition, fade out the box and label first
        self.play(
            FadeOut(self.ad1_box),
            FadeOut(self.ad1_label),
            run_time=0.5
        )
        
        # FIX 1: Transform all elements simultaneously instead of one by one
        transforms = [ReplacementTransform(element, node) for element, node in zip(self.ad1_elements, nodes)]
        self.play(*transforms, run_time=1)
        
        # Update tracking list
        self.ad1_elements = nodes
        
        # FIX 2: Write all labels simultaneously instead of one by one
        self.play(*[Write(label) for label in node_labels], run_time=1)
        
        self.nodes1 = nodes
        self.node_labels1 = node_labels
        self.wait(0.5)
    
    def connect_nodes_in_graph(self):
        # Ensure the previous text is fully faded out before the new one appears
        # Make text over 2 lines
        step3_text = Text("Next, we can create a graph representation where data \nis linked together when seen in the same ad.").scale(0.8).to_edge(UP)
        self.play(
            FadeOut(self.step2_text, run_time=0.5),
        )
        self.play(
            Write(step3_text)
        )
        self.step3_text = step3_text
        
        # Move title node to center
        title_node = self.ad1_elements[0]  # Using the transformed elements
        title_pos = self.ad1_box.get_center()
        
        # Reposition nodes in a better graph layout
        self.play(
            title_node.animate.move_to(title_pos),
            self.node_labels1[0].animate.move_to(title_pos),
            run_time=1
        )
        
        # Create edges from center (title) to all other nodes
        edges = []
        for i in range(1, len(self.ad1_elements)):
            edge = Line(
                title_node.get_center(),
                self.ad1_elements[i].get_center(),
                color=WHITE
            )
            edges.append(edge)
        
        # FIX 5: Show all edges simultaneously
        self.play(*[Create(edge) for edge in edges], run_time=1)
        self.edges1 = edges
        
        # Group into a graph 1
        self.graph1_elements = VGroup(*[elem for elem in self.ad1_elements], *self.node_labels1, *edges)
        
        self.wait(0.5)
    
    def create_second_ad(self):
        # Ensure the previous text is fully faded out before the new one appears
        step4_text = Text("Now, let's look at what happens \nwhen we have multiple ads.").scale(0.8).to_edge(UP)
        self.play(
            FadeOut(self.step3_text, run_time=0.5),
        )
        self.play(
            Write(step4_text)
        )
        self.step4_text = step4_text
        
        # Shift first graph to the left
        self.play(
            self.graph1_elements.animate.shift(LEFT * 3),
            run_time=1.5
        )
        
        # Create second ad elements (reusing code with modifications)
        ad2_box = Rectangle(height=4, width=5, color=WHITE)
        ad2_label = Text("Ad 2", color=WHITE).next_to(ad2_box, UP)
        
        ad2_box.shift(RIGHT * 3)
        ad2_label.shift(RIGHT * 3)
        
        # Second ad content with one matching element (phone number)
        ad2_title = Text("Escort Ad 2", color=WHITE, font_size=24)
        ad2_text = Text("Example Ad Text", color=WHITE, font_size=20)
        ad2_phone = Text("XXX-XXX-XXXX", color=WHITE, font_size=20)  # Same phone number
        
        # Image placeholder with person icon
        ad2_img1 = self.create_person_icon(1, 1.5, WHITE)
        
        # Position elements properly inside the box
        ad2_title.move_to(ad2_box.get_center() + UP * 1)
        ad2_text.move_to(ad2_box.get_center() + UP * 0.3)
        ad2_phone.move_to(ad2_box.get_center() + DOWN * 0.4)
        ad2_img1.move_to(ad2_box.get_center() + DOWN * 1.2)
        
        # Show ad2 box and label
        self.play(
            Create(ad2_box),
            Write(ad2_label)
        )
        
        # Show ad2 content
        self.play(
            Write(ad2_title),
            Write(ad2_text),
            Write(ad2_phone),
            Create(ad2_img1),
            run_time=2
        )
        
        self.ad2_elements = [ad2_title, ad2_text, ad2_phone, ad2_img1]
        self.ad2_box = ad2_box
        self.ad2_label = ad2_label
        
        # Define node positions for second graph
        center2 = ad2_box.get_center()
        radius = 1.5
        angles = np.linspace(0, 2 * np.pi, len(self.ad2_elements), endpoint=False)
        positions = [center2 + radius * np.array([np.cos(angle), np.sin(angle), 0]) for angle in angles]
        
        # Create nodes
        nodes2 = []
        node_labels2 = []
        
        for i in range(len(self.ad2_elements)):
            if i == 0:  # Title node
                node = Circle(radius=0.4, color=self.text_node_color, fill_opacity=0.7)
                label = Text("Title", font_size=16)
            elif i == 1:  # Description
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text("Text", font_size=16)
            elif i == 2:  # Phone (matching node)
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text("Phone", font_size=16)
            else:  # Images
                node = Circle(radius=0.4, color=self.node_color, fill_opacity=0.7)
                label = Text(f"Img{i-2}", font_size=16)
            
            node.move_to(positions[i])
            label.move_to(node.get_center())
            nodes2.append(node)
            node_labels2.append(label)
        
        # First fade out the box and label for a cleaner transition
        self.play(
            FadeOut(ad2_box),
            FadeOut(ad2_label),
            run_time=0.5
        )
        
        # FIX 1: Transform all elements simultaneously
        transforms2 = [ReplacementTransform(element, node) for element, node in zip(self.ad2_elements, nodes2)]
        self.play(*transforms2, run_time=1)
        self.ad2_elements = nodes2
        
        # FIX 2: Write all labels simultaneously
        self.play(*[Write(label) for label in node_labels2], run_time=1)
        
        # Connect second graph nodes
        title_node2 = self.ad2_elements[0]
        title_pos2 = center2
        
        self.play(
            title_node2.animate.move_to(title_pos2),
            node_labels2[0].animate.move_to(title_pos2),
            run_time=1
        )
        
        # Create edges for graph 2
        edges2 = []
        for i in range(1, len(self.ad2_elements)):
            edge = Line(
                title_node2.get_center(),
                self.ad2_elements[i].get_center(),
                color=WHITE
            )
            edges2.append(edge)
        
        # FIX 5: Show all edges simultaneously
        self.play(*[Create(edge) for edge in edges2], run_time=1)
        
        self.nodes2 = nodes2
        self.node_labels2 = node_labels2
        self.edges2 = edges2
        
        # Group into graph 2
        self.graph2_elements = VGroup(*[elem for elem in self.ad2_elements], *node_labels2, *edges2)
        
        self.wait(0.5)
    
    def highlight_matching_nodes(self):
        # Ensure the previous text is fully faded out before the new one appears
        step5_text = Text("These two ads have the same phone number.").scale(0.8).to_edge(UP)
        self.play(
            FadeOut(self.step4_text, run_time=0.5),
        )
        self.play(
            Write(step5_text)
        )
        self.step5_text = step5_text
        
        # Identify the matching nodes (phone numbers)
        phone_node1 = self.ad1_elements[2]
        phone_node2 = self.ad2_elements[2]
        
        # Highlight matching nodes with a pulse animation
        self.play(
            phone_node1.animate.set_color(self.highlight_color),
            phone_node2.animate.set_color(self.highlight_color),
            run_time=1
        )
        
        # Add equals sign between the nodes with a fade in
        equals_sign = Text("=", font_size=36, color=self.highlight_color)
        equals_sign.move_to((phone_node1.get_center() + phone_node2.get_center()) / 2)
        
        self.play(FadeIn(equals_sign))
        self.equals_sign = equals_sign
        
        self.wait(0.5)
    
    def merge_graphs(self):
        # FIX 3: Position the step6_text to avoid overlap with final label
        step6_text = Text("This allows us to connect these two ads \ntogether into a single graph.").scale(0.8).to_edge(UP)
        self.play(
            FadeOut(self.step5_text, run_time=0.5),
        )
        self.play(
            Write(step6_text)
        )
        self.step6_text = step6_text
        
        # Get positions
        phone_node1 = self.ad1_elements[2]
        phone_node2 = self.ad2_elements[2]
        phone_label1 = self.node_labels1[2]
        phone_label2 = self.node_labels2[2]
        
        # Find the title nodes and edges (needed for the line update)
        title_node1 = self.ad1_elements[0]
        title_node2 = self.ad2_elements[0]
        
        # Find edges connected to phone nodes
        phone_edges1 = []
        phone_edges2 = []
        
        for edge in self.edges1:
            if np.allclose(edge.get_end(), phone_node1.get_center(), atol=0.1):
                phone_edges1.append(edge)
                
        for edge in self.edges2:
            if np.allclose(edge.get_end(), phone_node2.get_center(), atol=0.1):
                phone_edges2.append(edge)
        
        # Target position for merged node (midway)
        merged_pos = (phone_node1.get_center() + phone_node2.get_center()) / 2
        
        # Create merged node
        merged_node = Circle(radius=0.5, color=self.highlight_color, fill_opacity=0.9)
        merged_node.move_to(merged_pos)
        merged_label = Text("Phone", font_size=16).move_to(merged_pos)
        
        # First fade out equals sign
        self.play(
            FadeOut(self.equals_sign),
            run_time=0.5
        )
        
        # FIX 4: Create Always updaters for the edges BEFORE starting the merge animation
        # This makes the lines follow the nodes as they move
        for edge in phone_edges1:
            edge.add_updater(lambda e, tn=title_node1, pn=phone_node1: 
                             e.put_start_and_end_on(tn.get_center(), pn.get_center()))
        
        for edge in phone_edges2:
            edge.add_updater(lambda e, tn=title_node2, pn=phone_node2: 
                             e.put_start_and_end_on(tn.get_center(), pn.get_center()))
        
        # Merge the phone nodes - the edges will follow due to the updaters
        self.play(
            Transform(phone_node1, merged_node),
            Transform(phone_node2, merged_node.copy()),
            Transform(phone_label1, merged_label),
            Transform(phone_label2, merged_label.copy()),
            run_time=1.5
        )
        
        # Remove the updaters after the animation completes
        for edge in phone_edges1 + phone_edges2:
            edge.clear_updaters()
        
        # Create box around the merged graph
        merged_graph_elements = VGroup(
            *[elem for elem in self.ad1_elements if elem != phone_node2],
            *[elem for elem in self.ad2_elements if elem != phone_node1],
            *[label for label in self.node_labels1 if label != phone_label2],
            *[label for label in self.node_labels2 if label != phone_label1],
            *self.edges1, *self.edges2
        )
        
        merged_box = SurroundingRectangle(merged_graph_elements, color=WHITE, buff=0.5)
        
        # FIX 3 (cont): Position the "New Connected Component" label below the step text
        # to avoid overlapping with the step6_text
        
        
        self.play(
            Create(merged_box),
            run_time=1
        )
        self.play(
            Write(merged_label),
            run_time=1
        )
        
        # Final message
        final_text = Text("Our new connected component is linkable to a potential individual.", 
                         color=WHITE, font_size=28).to_edge(DOWN, buff=0.5)
        self.play(Write(final_text))
        
        self.wait(2)


# To render this animation:
if __name__ == "__main__":
    scene = AdLinkingVisualization()
    scene.render()