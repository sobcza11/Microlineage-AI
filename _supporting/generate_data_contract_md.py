# _supporting/generate_data_contract_md.py

from __future__ import annotations

import sys
from pathlib import Path

import pandera as pa

# Path to repo root: one level up from _supporting/
ROOT = Path(__file__).resolve().parents[1]

# Ensure repo root is on sys.path so `import microlineage` works
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Local import (same folder as this script)
from schema_contract import schema_to_contract_df  # noqa: E402

# Now safe to import your schema
from microlineage.schemas import RetailSchema  # noqa: E402


def main() -> None:
    schema: pa.DataFrameSchema = RetailSchema
    contract_df = schema_to_contract_df(schema)
    md = contract_df.to_markdown(index=False)

    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)

    output_path = docs_dir / "data_contract_retail.md"

    with output_path.open("w", encoding="utf-8") as f:
        f.write("# Data Contract: Retail Forecast Input\n\n")
        f.write(
            "This table describes the expected input structure enforced by Pandera "
            "for the core forecasting pipeline.\n\n"
        )
        f.write(md)
        f.write("\n")

    print(f"Data contract markdown written to {output_path}")


if __name__ == "__main__":
    main()
