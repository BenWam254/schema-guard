import os
import shutil
import polars as pl
from src.validator import load_contract, validate_parquet_dataset


def test_contract_validation_pass_and_fail():
    tmp_parquet = "tests/tmp_guard.parquet"
    if os.path.exists(tmp_parquet):
        os.remove(tmp_parquet)

    # 1. Create a valid dummy Parquet dataset
    valid_df = pl.DataFrame(
        {
            "scraper_name": ["bot_a", "bot_b"],
            "url": ["https://example.com/1", "https://example.com/2"],
            "status_code": [200, 200],
            "response_time_ms": [100.0, 150.0],
            "raw_content": ["# Hello", "# World"],
            "timestamp": [1700000000.0, 1700000001.0],
        }
    )
    valid_df.write_parquet(tmp_parquet)

    contract = load_contract("contracts/default_contract.yaml")
    result = validate_parquet_dataset(tmp_parquet, contract)

    assert result["valid"] is True
    assert result["rows_inspected"] == 2
    assert len(result["errors"]) == 0

    # 2. Create an invalid dummy Parquet dataset (missing status_code)
    invalid_df = pl.DataFrame(
        {
            "scraper_name": ["bot_a"],
            "url": ["https://example.com/1"],
            "response_time_ms": [100.0],
            "raw_content": ["# Hello"],
            "timestamp": [1700000000.0],
        }
    )
    invalid_df.write_parquet(tmp_parquet)

    invalid_result = validate_parquet_dataset(tmp_parquet, contract)
    assert invalid_result["valid"] is False
    assert any("Missing Column" in err for err in invalid_result["errors"])

    # Cleanup
    if os.path.exists(tmp_parquet):
        os.remove(tmp_parquet)