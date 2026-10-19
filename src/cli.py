import sys
import typer
from rich import print
from src.validator import load_contract, validate_parquet_dataset

app = typer.Typer(name="schema-guard", help="Data enforcer and schema drift detector.")

@app.command()
def validate(
    data_path: str = typer.Option(..., "--data-path", "-d", help="Path to Parquet file or partitioned directory"),
    contract_path: str = typer.Option("contracts/default_contract.yaml", "--contract", "-c", help="Path to YAML contract"),
):
    """Executes schema contract checks agaist target Parquet datasets."""
    print(f"[bold blue]INFO:[/bold blue] Loading data contract: [yellow]{contract_path}[/yellow]")

    try:
        contract = load_contract(contract_path)
    except Exception as err:
        print(f"[bold red]ERROR:[/bold red] Failed to load contract: {err}")
        sys.exit(1)

    print(f"[bold blue]INFO:[/bold blue] Inspecting Parquet dataset at: [yellow]{data_path}[/yellow]")
    result = validate_parquet_dataset(data_path, contract)

    if result["valid"]:
        print(f"[bold green]SUCCESS:[/bold green] Contract validation passed! ({result['rows_inspected']} rows checked)")
        sys.exit(0)
    else:
        print(f"[bold red]CONTRACT VIOLATION:[/bold red] Found {len(result['errors'])} drift errors")
        for err in result["errors"]:
            print(f"  - [red]{err}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    app()
