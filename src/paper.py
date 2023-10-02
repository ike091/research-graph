class Paper:
    """Data model representing a paper."""

    def __init__(
        self,
        title: str,
        url: str,
        id: str,
        publish_date: str,
        authors: list[str],
        summary: str,  # html string from arxiv
    ):
        """Initialize a paper object."""
        self.title = title
        self.url = url
        self.id = id
        self.publish_date = publish_date
        self.authors = authors
        self.summary = summary
