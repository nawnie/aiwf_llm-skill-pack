from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any


MONEY = Decimal("0.01")


def money(value: Any, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{label} must be a finite non-negative number")
    return result.quantize(MONEY, rounding=ROUND_HALF_UP)


def number(value: Decimal) -> float:
    return float(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    starting_cash = money(payload.get("starting_cash"), "starting_cash")
    currency = str(payload.get("currency", "USD")).strip().upper()
    scenarios = payload.get("scenarios")
    if not currency or len(currency) > 8:
        raise ValueError("currency must be a short currency code")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios must be a non-empty list")

    seen_names: set[str] = set()
    results: list[dict[str, Any]] = []
    for scenario_index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise ValueError(f"scenarios[{scenario_index}] must be an object")
        name = str(scenario.get("name", "")).strip()
        if not name or name in seen_names:
            raise ValueError("each scenario needs a unique non-empty name")
        seen_names.add(name)
        months = scenario.get("months")
        if not isinstance(months, list) or not 1 <= len(months) <= 120:
            raise ValueError(f"scenario {name!r} must contain 1-120 months")

        cash = starting_cash
        funded_months = 0
        depletion_month: str | None = None
        rows: list[dict[str, Any]] = []
        total_inflows = Decimal("0")
        total_outflows = Decimal("0")
        seen_months: set[str] = set()
        for month_index, month in enumerate(months):
            if not isinstance(month, dict):
                raise ValueError(f"scenario {name!r} month {month_index} must be an object")
            label = str(month.get("month", "")).strip()
            if not label or label in seen_months:
                raise ValueError(f"scenario {name!r} has a missing or duplicate month label")
            seen_months.add(label)
            inflows = money(month.get("inflows", 0), f"{name}.{label}.inflows")
            outflows = money(month.get("outflows", 0), f"{name}.{label}.outflows")
            opening = cash
            net_change = inflows - outflows
            cash += net_change
            total_inflows += inflows
            total_outflows += outflows
            if cash >= 0 and depletion_month is None:
                funded_months += 1
            elif depletion_month is None:
                depletion_month = label
            rows.append(
                {
                    "month": label,
                    "opening_cash": number(opening),
                    "inflows": number(inflows),
                    "outflows": number(outflows),
                    "net_burn": number(outflows - inflows),
                    "closing_cash": number(cash),
                }
            )

        results.append(
            {
                "name": name,
                "funded_months_in_horizon": funded_months,
                "depletion_month": depletion_month,
                "ending_cash": number(cash),
                "average_monthly_inflows": number(total_inflows / len(months)),
                "average_monthly_outflows": number(total_outflows / len(months)),
                "average_monthly_net_burn": number((total_outflows - total_inflows) / len(months)),
                "months": rows,
            }
        )

    return {
        "schema_version": 1,
        "currency": currency,
        "starting_cash": number(starting_cash),
        "scenario_results": results,
        "notes": [
            "Runway covers only the supplied monthly horizon.",
            "Pipeline and uncommitted financing should not be entered as contracted inflows.",
            "This operating model is not legal, tax, accounting, valuation, or investment advice.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate explicit startup cash-runway scenarios.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("input must be a JSON object")
        result = calculate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
