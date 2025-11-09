"""TinyNote Blob Storage Service - Azure Blob read/write operations."""

from azure.storage.blob import BlobServiceClient
import logging

logger = logging.getLogger(__name__)


def save_note(connection_string: str, container_name: str, note_id: str, note_data: str) -> bool:
    """Save note to Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = f"{note_id}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(note_data, overwrite=True)
        logger.info(f"Note {note_id} saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving note {note_id}: {str(e)}")
        return False


def get_note(connection_string: str, container_name: str, note_id: str) -> str or None:
    """Retrieve note from Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = f"{note_id}.json"
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()
        note_data = download_stream.readall().decode("utf-8")
        logger.info(f"Note {note_id} retrieved successfully")
        return note_data
    except Exception as e:
        if "BlobNotFound" in str(type(e).__name__) or "404" in str(e):
            logger.info(f"Note {note_id} not found")
            return None
        logger.error(f"Error retrieving note {note_id}: {str(e)}")
        return None


def delete_note(connection_string: str, container_name: str, note_id: str) -> bool:
    """Delete note from Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = f"{note_id}.json"
        container_client.delete_blob(blob_name)
        logger.info(f"Note {note_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Error deleting note {note_id}: {str(e)}")
        return False
