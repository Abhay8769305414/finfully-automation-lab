import os
import json
import logging
from src.worker.celery_app import celery_app
from src.repositories.factory import get_execution_repository, get_ledger_repository
from src.services.reconciliation_service import ReconciliationService

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="src.worker.tasks.process_invoice_batch_task")
def process_invoice_batch_task(self, file_path: str, execution_id: str):
    logger.info("Starting background invoice processing task (execution_id=%s)", execution_id)
    
    exec_repo = get_execution_repository()
    exec_repo.update_job_status(execution_id, "running")
    
    try:
        service = ReconciliationService()
        report = service.run_reconciliation(file_path=file_path, execution_id=execution_id)
        
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"reconciliation_{execution_id}.json")
        with open(report_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
            
        exec_repo.update_job_status(execution_id, "completed", result_summary=report.get("summary"), report_path=report_path)
        logger.info("Task completed successfully (execution_id=%s)", execution_id)
        return report
    except Exception as exc:
        logger.error("Task failed (execution_id=%s): %s", execution_id, exc)
        exec_repo.update_job_status(execution_id, "failed", error_message=str(exc))
        raise exc
