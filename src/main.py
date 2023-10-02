import argparse
from metaphor_interface import MetaphorInterface
from visualization import Visualization


def main():
    """Entrypoint for Metaphor reserach visualizer."""

    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Project with Metaphor API",
        epilog="Oh yeah...",
    )
    parser.add_argument("topic", help="Topic to retrieve research about.")
    parser.add_argument(
        "-n",
        "--num-papers",
        type=int,
        default=3,
        help="Number of papers to retrieve in initial pass.",
    )
    args = parser.parse_args()

    # Fetch papers with Metaphor
    m = MetaphorInterface()
    paper_list = m.search_papers(args.topic, args.num_papers)

    # Generate visualization
    vis = Visualization(args.topic, paper_list)
    vis.generate("output")


if __name__ == "__main__":
    main()
