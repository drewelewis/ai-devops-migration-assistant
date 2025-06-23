import os

from dotenv import load_dotenv
from typing import List, Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, field_validator

from operations.harness_operations import HarnessOperations

load_dotenv(override=True)

class HarnessGetPipelineListInputModel(BaseModel):
    account_identifier: str = Field(description="Account Identifier for the Entity.")
    org_identifier: str = Field(description="Organization Identifier for the Entity.")
    project_identifier: str = Field(description="Project Identifier for the Entity.")
    body: Optional[object] = Field(default=None, description="PipelineFilterProperties object for filter properties when listing pipelines.")
    page: Optional[int] = Field(default=0, description="Page Index of the results to fetch. Default: 0")
    size: Optional[int] = Field(default=25, description="Results per page. Default: 25")
    sort: Optional[List[str]] = Field(default=None, description="Sort criteria for the elements.")
    search_term: Optional[str] = Field(default=None, description="Search term to filter pipelines by name, identifier, or tags.")
    module: Optional[str] = Field(default=None, description="Module")
    filter_identifier: Optional[str] = Field(default=None, description="Filter identifier.")
    branch: Optional[str] = Field(default=None, description="Name of the branch.")
    repo_identifier: Optional[str] = Field(default=None, description="Git Sync Config Id.")
    get_default_from_other_repo: Optional[bool] = Field(default=None, description="If true, return all the default entities.")
    get_distinct_from_branches: Optional[bool] = Field(default=None, description="Boolean flag to get distinct pipelines from all branches.")

    @field_validator("account_identifier")
    def validate_account_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineListTool error: account_identifier parameter is required")
        return v.strip()
    
    @field_validator("org_identifier")
    def validate_org_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineListTool error: org_identifier parameter is required")
        return v.strip()
    
    @field_validator("project_identifier")
    def validate_project_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineListTool error: project_identifier parameter is required")
        return v.strip()


class HarnessCreatePipelineInputModel(BaseModel):
    account_identifier: str = Field(description="Account Identifier for the Entity.")
    org_identifier: str = Field(description="Organization Identifier for the Entity.")
    project_identifier: str = Field(description="Project Identifier for the Entity.")
    body: Optional[object] = Field(default=None, description="PipelineFilterProperties object for filter properties when listing pipelines.")
    branch: Optional[str] = Field(default=None, description="Name of the branch.")
    repo_identifier: Optional[str] = Field(default=None, description="Git Sync Config Id.")    
    root_folder: Optional[str] = Field(default=None, description="Path to the root folder of the Entity.")
    file_path: Optional[str] = Field(default=None, description="File Path of the Entity.")
    commit_msg: Optional[str] = Field(default=None, description="Commit message for the Entity.")
    is_new_branch: bool = Field(default=False, description="Checks the new branch (default: false).")
    base_branch: Optional[str] = Field(default=None, description="Name of the default branch.")
    connector_ref: Optional[str] = Field(default=None, description="Identifier of Connector needed for CRUD operations on the respective Entity.")
    store_type: Optional[str] = Field(default=None, description="Tells whether the Entity is to be saved on Git or not.")
    repo_name: Optional[str] = Field(default=None, description="Name of the repository.")
    
    @field_validator("account_identifier")
    def validate_account_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessCreatePipelineTool error: account_identifier parameter is required")
        return v.strip()
    
    @field_validator("org_identifier")
    def validate_org_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessCreatePipelineTool error: org_identifier parameter is required")
        return v.strip()
    
    @field_validator("project_identifier")
    def validate_project_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessCreatePipelineTool error: project_identifier parameter is required")
        return v.strip()
    
    @field_validator("body")
    def validate_body(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessCreatePipelineTool error: body parameter is required")
        return v.strip()

class HarnessGetPipelineInputModel(BaseModel):
    account_identifier: str = Field(description="Account Identifier for the Entity.")
    org_identifier: str = Field(description="Organization Identifier for the Entity.")
    project_identifier: str = Field(description="Project Identifier for the Entity.")
    pipeline_identifier: str = Field(description="Pipeline Identifier for the Entity.")    
    branch: Optional[str] = Field(default=None, description="Name of the branch.")
    repo_identifier: Optional[str] = Field(default=None, description="Git Sync Config Id.")    
    get_default_from_other_repo: bool = Field(default=True, description="If true, return all the default entities.")
    get_templates_resolved_pipeline: bool = Field(default=False, description="If true, returns Templates resolved Pipeline YAML in the response else returns null.")
    load_from_fallback_branch: bool = Field(default=False, description="If true, loads the pipeline from the fallback branch.")
    load_from_cache: str = Field(default='false', description="If true, loads the pipeline from cache.")
    validate_async: bool = Field(default=False, description="If true, validates the pipeline asynchronously.")        
    
    @field_validator("account_identifier")
    def validate_account_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineTool error: account_identifier parameter is required")
        return v.strip()
    
    @field_validator("org_identifier")
    def validate_org_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineTool error: org_identifier parameter is required")
        return v.strip()
    
    @field_validator("project_identifier")
    def validate_project_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineTool error: project_identifier parameter is required")
        return v.strip()
    
    @field_validator("pipeline_identifier")
    def validate_pipeline_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("HarnessGetPipelineTool error: pipeline_identifier parameter is required")
        return v.strip()


class HarnessGetPipelineListTool(BaseTool):
    name: str = "HarnessGetPipelineListTool"
    description: str = """
        Useful for when you need to get a list of pipelines from a Harness project.
        Requires account_identifier, org_identifier, and project_identifier.
    """.strip()
    return_direct: bool = False
    args_schema: Optional[ArgsSchema] = HarnessGetPipelineListInputModel    
    harness_operations: HarnessOperations = Field(exclude=True)    
    
    def __init__(self, harness_operations: HarnessOperations):
        super().__init__(harness_operations=harness_operations)
    
    def _run(
        self,
        account_identifier: str,
        org_identifier: str,
        project_identifier: str,
        body: Optional[object] = None,
        page: Optional[int] = 0,
        size: Optional[int] = 25
    ) -> str:
        try:
            pipelines = self.harness_operations.get_pipeline_list(
                account_identifier=account_identifier,
                org_identifier=org_identifier,
                project_identifier=project_identifier,
                body=body,                
                page=page,
                size=size                
            )
            return str(pipelines)
        except Exception as e:
            return f"Error retrieving pipeline list: {str(e)}"


class HarnessCreatePipelineTool(BaseTool):
    name: str = "HarnessCreatePipelineTool"
    description: str = """
        Useful for when you need to create a new pipeline in a Harness project.
        Requires account_identifier, org_identifier, project_identifier, and body with pipeline YAML.
    """.strip()
    return_direct: bool = False
    args_schema: Optional[ArgsSchema] = HarnessCreatePipelineInputModel
    harness_operations: HarnessOperations = Field(exclude=True)    
    
    def __init__(self, harness_operations: HarnessOperations):
        super().__init__(harness_operations=harness_operations)
    
    def _run(
        self,
        account_identifier: str,
        org_identifier: str,
        project_identifier: str,
        body: str,
    ) -> str:
        try:
            pipeline = self.harness_operations.create_pipeline(
                body=body,
                account_identifier=account_identifier,
                org_identifier=org_identifier,
                project_identifier=project_identifier                
            )
            return str(pipeline)
        except Exception as e:
            return f"Error creating pipeline: {str(e)}"
        
class HarnessGetPipelineTool(BaseTool):
    name: str = "HarnessGetPipelineTool"
    description: str = """
        Useful for when you need to get a specific pipeline from a Harness project.
        Requires account_identifier, org_identifier, project_identifier, and pipeline_identifier.    
    """.strip()
    return_direct: bool = False
    args_schema: Optional[ArgsSchema] = HarnessGetPipelineInputModel
    harness_operations: HarnessOperations = Field(exclude=True)    
    
    def __init__(self, harness_operations: HarnessOperations):
        super().__init__(harness_operations=harness_operations)
    
    def _run(
        self,
        account_identifier: str,
        org_identifier: str,
        project_identifier: str,
        pipeline_identifier: str
    ) -> str:
        try:
            pipeline = self.harness_operations.get_pipeline(
                account_identifier=account_identifier,
                org_identifier=org_identifier,
                project_identifier=project_identifier,
                pipeline_identifier=pipeline_identifier
            )
            return str(pipeline)
        except Exception as e:
            return f"Error retrieving pipeline: {str(e)}"


class HarnessTools:
    """Container class for Harness tools."""
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        # Initialize Harness operations with API key from environment or parameter
        self.harness_api_key = api_key or os.getenv("HARNESS_API_KEY")
        if not self.harness_api_key:
            raise ValueError("HARNESS_API_KEY environment variable is required or must be provided as parameter")
        
        self.harness_operations = HarnessOperations(api_key=self.harness_api_key)
        
        self.tools = [
            HarnessGetPipelineListTool(self.harness_operations),            
            HarnessGetPipelineTool(self.harness_operations),
            HarnessCreatePipelineTool(self.harness_operations),
        ]

    def get_tools(self) -> List[BaseTool]:
        """Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)."""
        return self.tools
    