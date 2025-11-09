"""TinyNote Azure Functions HTTP Triggers
Endpoints:
  POST /api/notes - Create a new note
  GET /api/notes/{id} - Retrieve a note
"""

import azure.functions as func
import json
import os
import uuid
from datetime import datetime
from .notes_service import save_note, get_note

app = func.FunctionApp()


@app.function_name("CreateNote")
@app.route("notes", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def create_note(req: func.HttpRequest) -> func.HttpResponse:
    """POST /api/notes - Create and save a note."""
    try:
        req_body = req.get_json()
        text = req_body.get("text", "").strip()

        if not text:
            return func.HttpResponse(
                json.dumps({"error": "text field is required"}),
                status_code=400,
                mimetype="application/json",
            )

        note_id = str(uuid.uuid4())
        note = {
            "id": note_id,
            "text": text,
            "created_at": datetime.utcnow().isoformat(),
        }

        conn_string = os.environ.get("NOTES_STORAGE_CONNECTION")
        container_name = os.environ.get("NOTES_CONTAINER", "notes")

        if not conn_string:
            return func.HttpResponse(
                json.dumps({"error": "Storage connection not configured"}),
                status_code=500,
                mimetype="application/json",
            )

        save_note(conn_string, container_name, note_id, json.dumps(note))

        return func.HttpResponse(
            json.dumps({"id": note_id, "created_at": note["created_at"]}),
            status_code=201,
            mimetype="application/json",
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json",
        )


@app.function_name("GetNote")
@app.route("notes/{id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_note_handler(req: func.HttpRequest) -> func.HttpResponse:
    """GET /api/notes/{id} - Retrieve note by ID."""
    try:
        note_id = req.route_params.get("id")

        if not note_id:
            return func.HttpResponse(
                json.dumps({"error": "Note ID required"}),
                status_code=400,
                mimetype="application/json",
            )

        conn_string = os.environ.get("NOTES_STORAGE_CONNECTION")
        container_name = os.environ.get("NOTES_CONTAINER", "notes")

        if not conn_string:
            return func.HttpResponse(
                json.dumps({"error": "Storage not configured"}),
                status_code=500,
                mimetype="application/json",
            )

        note_data = get_note(conn_string, container_name, note_id)

        if note_data is None:
            return func.HttpResponse(
                json.dumps({"error": "Note not found"}),
                status_code=404,
                mimetype="application/json",
            )

        return func.HttpResponse(
            note_data,
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json",
        )


@app.function_name("Health")
@app.route("health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """GET /api/health - Health check endpoint."""
    return func.HttpResponse(
        json.dumps({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}),
        status_code=200,
        mimetype="application/json",
    )
