import sys
import logging
from src.reader import read_sales_csv
from src.transformer import transform_records
from src.validator import validate_transformed_records
from src.reporter import generate_summary

logger = logging.getLogger(__name__)

def run_pipeline(file_path: str = "data/sales.csv", execution_id: str = "EXEC-001") -> dict:
    logger.info("Executing pipeline for %s (execution_id=%s)", file_path, execution_id)
    raw = read_sales_csv(file_path)
    transformed = transform_records(raw)
    valid = validate_transformed_records(transformed)
    report = generate_summary(valid, execution_id)
    return report

if __name__ == "__main__":
    rep = run_pipeline()
    print("Pipeline Execution Complete:", rep)
