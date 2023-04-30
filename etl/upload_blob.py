from azure.storage.blob import BlobServiceClient
import config

def uploadToBlobStorage(file_path, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(config.connection_string)
    blob_client = blob_service_client.get_blob_client(container=config.container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_name}")




