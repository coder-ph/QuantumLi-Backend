from src.Models.billing import Billing
from src.startup.database import db
from src.utils.logger import logger
from typing import Optional, List

class BillingRepository:
    def create(self, data: dict) -> Optional[Billing]:
        """
        Create a new billing record.
        """
        try:
            billing = Billing(**data)
            db.session.add(billing)
            db.session.commit()
            logger.info(f"Billing created: {billing.invoice_id}")
            return billing
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating billing: {str(e)}")
            return None

    def get_all(self) -> List[Billing]:
        """
        Retrieve all non-deleted billing records.
        """
        try:
            return Billing.query.filter_by(is_deleted=False).all()
        except Exception as e:
            logger.error(f"Error fetching all billing records: {str(e)}")
            return []

    def get_by_id(self, invoice_id: str) -> Optional[Billing]:
        """
        Get a billing record by invoice ID.
        """
        try:
            return Billing.query.filter_by(invoice_id=invoice_id, is_deleted=False).first()
        except Exception as e:
            logger.error(f"Error fetching billing by ID {invoice_id}: {str(e)}")
            return None

    def update(self, billing: Billing, data: dict) -> Optional[Billing]:
        """
        Update a billing record with provided data.
        """
        try:
            for key, value in data.items():
                setattr(billing, key, value)
            db.session.commit()
            logger.info(f"Billing {billing.invoice_id} updated successfully.")
            return billing
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating billing {billing.invoice_id}: {str(e)}")
            return None

    def delete(self, billing: Billing) -> Optional[Billing]:
        """
        Soft delete a billing record.
        """
        try:
            billing.is_deleted = True
            db.session.commit()
            logger.info(f"Billing {billing.invoice_id} soft deleted.")
            return billing
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting billing {billing.invoice_id}: {str(e)}")
            return None

    def restore(self, billing: Billing) -> Optional[Billing]:
        """
        Restore a soft-deleted billing record.
        """
        try:
            billing.is_deleted = False
            db.session.commit()
            logger.info(f"Billing {billing.invoice_id} restored.")
            return billing
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error restoring billing {billing.invoice_id}: {str(e)}")
            return None
