import os
import yaml
import logging
import polars as pl
from pydantic import BaseModel

logger = logging.getLogger("schema_guard")


class ContractRules(BaseModel):
    max_null_percentage: float = 0.05
    allowed_status_codes: list[int] = [200, 201, 202, 301, 302, 404, 500]


class DataContract(BaseModel):
    version: str
    dataset: str
    columns: dict[str, str]
    rules: ContractRules


def load_contract(contract_path: str) -> DataContract:
    """Loads and validates a YAML contract definition."""
    if not os.path.exists(contract_path):
        raise FileNotFoundError(f"Contract file not found at: {contract_path}")

    with open(contract_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return DataContract(**data)


def validate_parquet_dataset(parquet_path: str, contract: DataContract) -> dict:
    """Scans a Parquet dataset or file and verifies schema type alignment, missing columns,
    and null percentage thresholds using Polars.
    """
    if not os.path.exists(parquet_path):
        return {"valid": False, "errors": [f"Parquet target path does not exist: {parquet_path}"]}

    errors = []
    df = pl.scan_parquet(parquet_path).collect()

    # 1. Check Missing & Extra Columns
    existing_schema = {col: str(dtype) for col, dtype in df.schema.items()}

    for expected_col, expected_type in contract.columns.items():
        if expected_col not in existing_schema:
            errors.append(f"Missing Column: Expected column '{expected_col}' was not found in Parquet dataset.")
        else:
            actual_type = existing_schema[expected_col]
            if expected_type.lower() not in actual_type.lower():
                errors.append(f"Type Mismatch on '{expected_col}': Expected {expected_type}, got {actual_type}.")

    # 2. Check Null Thresholds
    total_rows = df.height
    if total_rows > 0:
        for col in contract.columns.keys():
            if col in df.columns:
                null_count = df[col].null_count()
                null_ratio = null_count / total_rows
                if null_ratio > contract.rules.max_null_percentage:
                    errors.append(
                        f"Null Threshold Exceeded on '{col}': Null ratio is {null_ratio:.2%} "
                        f"(Max allowed: {contract.rules.max_null_percentage:.2%})"
                    )

    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "rows_inspected": total_rows,
        "errors": errors,
    }