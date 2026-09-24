from __future__ import annotations

import argparse

from .workflow import build_workflow, get_skill_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-agent analytics workflow runner")
    parser.add_argument("--start", type=int, default=1, help="Starting skill index")
    parser.add_argument("--end", type=int, default=None, help="Ending skill index")
    args = parser.parse_args()

    workflow = build_workflow(args.start, args.end)
    print("Workflow steps:")
    for i, skill in enumerate(workflow, start=1):
        print(f"{i}. {skill.title} ({skill.id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
