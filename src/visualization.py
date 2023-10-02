from pyvis.network import Network


class Visualization:
    """Generates a graph visualization of a topic and its related papers."""

    # Only visualize first N authors
    AUTHORS_TO_SHOW = 2

    def __init__(self, title, papers):
        """Creates a graph visualization."""
        self.net = Network(bgcolor="#222222", font_color="white")
        self.net.add_node(-1, title)
        self.title = title
        self.papers = papers
        # Uncomment to show configuration buttons
        self.net.show_buttons(filter_=["physics"])

        # Generate paper nodes and edges
        for i, paper in enumerate(self.papers):
            self.net.add_node(i, paper.title, title=paper.summary)
            self.net.add_edge(-1, i, physics=False)

        # Generate author data structure for generating edges
        authors = {}
        for i, paper in enumerate(self.papers):
            # Only show first n authors
            author_count = min(self.AUTHORS_TO_SHOW, len(paper.authors))
            for author in paper.authors[:author_count]:
                if author not in authors:
                    authors[author] = set()
                authors[author].add(i)

        # Add author nodes and edges
        for author in authors:
            # Don't display unknown authors
            if author == "Unknown author":
                continue

            # Add node and edges for author
            self.net.add_node(author, color="red")
            for pid in authors[author]:
                self.net.add_edge(author, pid, physics=False)

    def generate(self, vis_name: str):
        """Ouput visualization as html file."""
        self.net.show(f"{vis_name}.html", notebook=False)
