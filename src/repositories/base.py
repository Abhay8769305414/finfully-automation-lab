from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class LedgerRepositoryInterface(ABC):
    @abstractmethod
    def create_invoice(self, invoice_id: str, customer_id: str, total_amount: float) -> Dict[str, Any]: pass
    @abstractmethod
    def claim_invoice(self, invoice_id: str, execution_id: str) -> bool: pass
    @abstractmethod
    def get_by_id(self, invoice_id: str) -> Optional[Dict[str, Any]]: pass

class ExecutionRepositoryInterface(ABC):
    @abstractmethod
    def create_job(self, execution_id: str, file_path: str, source: str = "manual") -> Dict[str, Any]: pass
    @abstractmethod
    def update_job_status(self, execution_id: str, status: str, result_summary: Optional[Dict[str, Any]] = None, report_path: Optional[str] = None, error_message: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def get_job(self, execution_id: str) -> Optional[Dict[str, Any]]: pass

class ReviewRepositoryInterface(ABC):
    @abstractmethod
    def create_review_item(self, customer_id: str, customer_name: str, raw_note: str, flag_reason: Dict[str, Any]) -> Dict[str, Any]: pass
    @abstractmethod
    def approve_item(self, item_id: int, reviewed_by: str) -> Dict[str, Any]: pass

class AIIdempotencyRepositoryInterface(ABC):
    @abstractmethod
    def save(self, idempotency_key: str, customer_id: str, raw_note: str, classification_json: Dict[str, Any]) -> Dict[str, Any]: pass
    @abstractmethod
    def get(self, idempotency_key: str) -> Optional[Dict[str, Any]]: pass
