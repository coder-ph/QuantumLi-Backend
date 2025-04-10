from src.Models.incidents import Incidents
from src.startup.database import db
from uuid import uuid4
import logging
from src.utils.logger import logger



class IncidentRepository:

    def create(self, data, user):
        
        try:
            data['reported_by'] = user.email  
            incident = Incidents(**data)
            db.session.add(incident)
            db.session.commit()
            logger.info(f"Incident created by {user.email}, ID: {incident.incident_id}")
            return incident
        except Exception as e:
            logger.error(f"Error creating incident: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to create incident: {str(e)}")

    def get_all(self):
      
        try:
            incidents = Incidents.query.filter_by(is_deleted=False).all()
            logger.info(f"Retrieved {len(incidents)} incidents.")
            return incidents
        except Exception as e:
            logger.error(f"Error retrieving incidents: {str(e)}")
            raise Exception(f"Failed to retrieve incidents: {str(e)}")

    def get_by_id(self, incident_id):
       
        try:
            incident = Incidents.query.get(incident_id)
            if not incident or incident.is_deleted:
                logger.warning(f"Incident with ID {incident_id} not found or already deleted.")
                return None
            logger.info(f"Retrieved incident with ID {incident_id}.")
            return incident
        except Exception as e:
            logger.error(f"Error retrieving incident with ID {incident_id}: {str(e)}")
            raise Exception(f"Failed to retrieve incident with ID {incident_id}: {str(e)}")

    def delete(self, incident):
      
        try:
            incident.is_deleted = True
            db.session.commit()
            logger.info(f"Incident {incident.incident_id} has been soft deleted.")
        except Exception as e:
            logger.error(f"Error deleting incident {incident.incident_id}: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to delete incident: {str(e)}")

    def update(self, incident, data):
       
        try:
            for key, value in data.items():
                if hasattr(incident, key):
                    setattr(incident, key, value)
            db.session.commit()
            logger.info(f"Incident {incident.incident_id} updated with new data.")
            return incident
        except Exception as e:
            logger.error(f"Error updating incident {incident.incident_id}: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to update incident: {str(e)}")

    def restore(self, incident):
        
        try:
            incident.is_deleted = False
            db.session.commit()
            logger.info(f"Incident {incident.incident_id} has been restored.")
        except Exception as e:
            logger.error(f"Error restoring incident {incident.incident_id}: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to restore incident: {str(e)}")
