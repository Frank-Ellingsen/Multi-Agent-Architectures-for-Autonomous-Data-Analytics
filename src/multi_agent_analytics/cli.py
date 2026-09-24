from __future__ import annotations

import argparse

from .analytics import compute_key_metrics
from .relationships import validate_relationships
from .reporting import build_markdown_report
from .schema import summarize_schema
from .workflow import build_workflow


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-agent analytics workflow runner")
    parser.add_argument("--start", type=int, default=1, help="Starting skill index")
    parser.add_argument("--end", type=int, default=None, help="Ending skill index")
    parser.add_argument("--data-dir", type=str, default='test_data', help="Path to the analytics CSV data directory")
    parser.add_argument("--report", action='store_true', help="Generate a markdown report for the dataset")
    args = parser.parse_args()

    if args.report:
        print(build_markdown_report(args.data_dir))
        return 0

    workflow = build_workflow(args.start, args.end)
    print("Workflow steps:")
    for i, skill in enumerate(workflow, start=1):
        print(f"{i}. {skill.title} ({skill.id})")

    if args.data_dir:
        print("\nDataset validation:")
        print(f"schema={list(summarize_schema(args.data_dir).keys())[:3]}")
        print(f"relationships={validate_relationships(args.data_dir)['valid']}")
        print(f"kpis={compute_key_metrics(args.data_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
