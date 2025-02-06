from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


class VertexAIPredictor:
    
    """Handles interaction with Google Cloud's Vertex AI prediction service."""

    def __init__(self, project_id: str, endpoint_id: str, location: str, api_endpoint: str):
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.location = location
        self.api_endpoint = api_endpoint

        # Initialize the Prediction Service Client
        client_options = {"api_endpoint": self.api_endpoint}
        self.client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    def predict(self, instances: list) -> list:
        
        """
        Sends prediction request to the Vertex AI model.

        :param instances: List of input data dictionaries for prediction.
        :return: List of model predictions.
        """
        formatted_instances = [
            json_format.ParseDict(instance, Value()) for instance in instances
        ]

        endpoint = self.client.endpoint_path(
            project=self.project_id, location=self.location, endpoint=self.endpoint_id
        )

        response = self.client.predict(endpoint=endpoint, instances=formatted_instances)
        return response.predictions
