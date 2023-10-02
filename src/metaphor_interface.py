from metaphor_python import Metaphor
from paper import Paper
import os


class MetaphorInterface:
    """Interface for interacting with the metaphor API.

    Additionally handles result parsing.
    """

    def __init__(self):
        metaphor_key = os.getenv("METAPHOR_API_KEY")
        self.metaphor = Metaphor(metaphor_key)

    def search_papers(self, prompt: str, num_results=3) -> list[Paper]:
        """Searches for papers on arxiv.org."""
        domains = ["arxiv.org"]
        response = self.metaphor.search(
            prompt,
            include_domains=domains,
            num_results=num_results,
            use_autoprompt=True,
        )

        # Look up all fetched paper abstracts
        ids_for_lookup = []
        for result in response.results:
            ids_for_lookup.append(result.id)
        abstracts = self._get_paper_abstracts(ids_for_lookup)

        # Build final paper list
        papers = []
        for result, abstract in zip(response.results, abstracts):
            papers.append(self._parse_paper_output(result, abstract))

        return papers

    def _parse_paper_output(self, result, abstract) -> Paper:
        """Converts metaphor result to internal Paper object."""
        # TODO: author parsing may break if author contains more than firstname
        #       + lastname
        # Parse authors
        if result.author is None:
            parsed_authors = ["Unknown author"]
        else:
            authors = result.author.split(";")
            parsed_authors = [
                b.strip() + " " + a.strip()
                for a, b in zip(authors[0::2], authors[1::2])
            ]

        return Paper(
            result.title,
            result.url,
            result.id,
            result.published_date,
            parsed_authors,
            abstract,
        )

    def _parse_paper_abstract(self, result):
        """Grabs the abstract/summary from an arxiv paper result."""
        # TODO: add more robust parsing
        # For now, just return html summary from arxiv
        html = result.extract
        return html

    def _get_paper_abstracts(self, ids: list[str]):
        """Returns a list of abstracts/descriptions for the given paper ids."""
        response = self.metaphor.get_contents(ids)
        abstracts = []
        for result in response.contents:
            abstracts.append(self._parse_paper_abstract(result))
        return abstracts

    def search(self, prompt: str):
        """Standard metaphor search endpoint."""
        response = self.metaphor.search(
            prompt,
            num_results=5,
            use_autoprompt=True,
        )
        return response

    def find_similar(self, url):
        """Metaphor 'find similar' search endpoint."""
        response = self.metaphor.find_similar(
            url,
            num_results=10,
        )
        return response

    def get_content(self, ids):
        """Metaphor 'get content' endpoint."""
        response = self.metaphor.get_contents(ids)
        return response
