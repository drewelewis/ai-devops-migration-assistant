import harness_python_sdk
import logging

from harness_python_sdk.rest import ApiException

# Harness operations class to interact with the Harness API.
class HarnessOperations:
    def __init__(self, api_key, api_key_prefix=None):
        """
        Initializes the Harness operations class with the provided API key and optional API key prefix.
        Args:
            api_key (str): The API key used for authentication with the Harness API.
            api_key_prefix (str, optional): An optional prefix for the API key (e.g., 'Bearer'). Defaults to None.
        Attributes:
            api_client (harness_python_sdk.ApiClient): The API client configured with the provided credentials.
            pipeline_api (harness_python_sdk.PipelineApi): The Pipeline API interface for interacting with Harness pipelines.
            logger (logging.Logger): Logger instance for this class.
        """
        # Configure API key authorization: x-api-key
        configuration = harness_python_sdk.Configuration()
        configuration.api_key['x-api-key'] = api_key
        # Setup prefix (e.g. Bearer) for API key, if needed        
        if api_key_prefix:
            configuration.api_key_prefix['x-api-key'] = api_key_prefix

        self.api_client = harness_python_sdk.ApiClient(configuration)
        self.pipeline_api = harness_python_sdk.PipelineApi(self.api_client)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")  
    
    def get_pipeline_list(
        self,
        account_identifier,
        org_identifier,
        project_identifier,
        body=None,
        page=0,
        size=25
    ):
        """
        List pipelines using the harness_python_sdk PipelineApi.
        All parameters except the first three are optional.
        """
        try:
            api_response = self.pipeline_api.get_pipeline_list(
                account_identifier,
                org_identifier,
                project_identifier,
                body=body,
                page=page,
                size=size                
            )
            return api_response
        except ApiException as e:            
            self.logger.error(f"Exception getting pipeline list: {e}")
            