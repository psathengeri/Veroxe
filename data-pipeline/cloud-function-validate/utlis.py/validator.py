import csv
import json
import io
from google.cloud import storage
from jsonschema import validate, ValidationError


# Config
SCHEMA_BUCKET_NAME = "ml-dataset-veroxe"
SCHEMA_FOLDER = "schemas/"


def load_schema(client_name: str) -> dict:
    """Loads the JSON schema for a specific client."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(SCHEMA_BUCKET_NAME)
    schema_blob = bucket.blob(f"{SCHEMA_FOLDER}{client_name}.schema.json")
    if not schema_blob.exists():
        raise FileNotFoundError(f"Schema for client '{client_name}' not found.")
    schema_data = schema_blob.download_as_text()
    return json.loads(schema_data)


def parse_csv_and_validate(file_contents: str, schema: dict):
    """Validates each row in the CSV against the schema."""
    reader = csv.DictReader(io.StringIO(file_contents))
    errors = []
    for i, row in enumerate(reader, start=1):
        try:
            validate(instance=row, schema=schema)
        except ValidationError as e:
            errors.append(f"Row {i}: {str(e.message)}")
    return errors


def validate_gcs_file(bucket_name: str, blob_name: str) -> tuple[bool, list[str]]:
    """Main validation routine."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if not blob_name.endswith(".csv"):
        return False, ["Invalid file format. Only CSV is supported."]

    # Assume client name is first folder in uploads path: uploads/pending/client1/filename.csv
    try:
        client_name = blob_name.split("/")[2]
    except IndexError:
        return False, ["Invalid file path structure. Expected uploads/pending/{client}/filename.csv"]

    try:
        schema = load_schema(client_name)
    except FileNotFoundError as e:
        return False, [str(e)]

    csv_data = blob.download_as_text()
    errors = parse_csv_and_validate(csv_data, schema)
    return len(errors) == 0, errors
