"""hebrew-toolbench CLI: `run` queries a model, `report` scores every cached model."""

from __future__ import annotations

import argparse
from pathlib import Path

from hebrew_toolbench import report, runner
from hebrew_toolbench.dataset import DEFAULT_DATASET, load_items


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="hebrew-toolbench")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATASET)
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="query a model on the dataset (resumable)")
    run_p.add_argument("--model", required=True)
    run_p.add_argument("--env-file", type=Path, help="file with TAINTWALL_BASE_URL / TAINTWALL_API_KEY")
    run_p.add_argument("--rpm", type=float, default=10.0, help="request rate cap (free tiers are ~10-20)")
    run_p.add_argument("--limit", type=int, help="only the first N items")
    sub.add_parser("report", help="score all cached raw outputs and print tables")
    args = parser.parse_args(argv)

    items = load_items(args.data)
    if args.command == "run":
        if args.env_file:
            runner.load_env_file(args.env_file.expanduser())
        new, failed = runner.run(items[: args.limit], args.model, args.rpm)
        print(f"{args.model}: {new} new, {failed} failed -> {runner.raw_path(args.model)}")
        return
    results = [report.score_raw(items, p) for p in sorted((runner.RESULTS_DIR / "raw").glob("*.jsonl"))]
    print(report.results_table(items, results), "\n")
    print(report.error_table(results), "\n")
    print(report.tag_table(items, results))


if __name__ == "__main__":
    main()
