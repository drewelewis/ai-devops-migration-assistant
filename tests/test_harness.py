import os
import sys
import logging
import harness_python_sdk
import yaml

from dotenv import load_dotenv
from harness_python_sdk.rest import ApiException
from pprint import pprint

from tools.harness_tools import HarnessTools, HarnessGetPipelineListInputModel

load_dotenv(override=True)
logger = logging.getLogger(__name__)

pipeline = """
pipeline:
    name: Sample Pipeline
    identifier: Sample_Pipeline
    allowStageExecutions: false
    projectIdentifier: Temp
    orgIdentifier: default
    tags: {}
    stages:
        - stage:
              name: Sample Stage
              identifier: Sample_Stage
              description: ""
              type: Approval
              spec:
                  execution:
                      steps:
                          - step:
                                name: Approval Step
                                identifier: Approval_Step
                                type: HarnessApproval
                                timeout: 1d
                                spec:
                                    approvalMessage: |-
                                        Please review the following information
                                        and approve the pipeline progression
                                    includePipelineExecutionHistory: true
                                    approvers:
                                        minimumCount: 1
                                        disallowPipelineExecutor: false
                                        userGroups: <+input>
                                    approverInputs: []
                          - step:
                                type: ShellScript
                                name: ShellScript Step
                                identifier: ShellScript_Step
                                spec:
                                    shell: Bash
                                    onDelegate: true
                                    source:
                                        type: Inline
                                        spec:
                                            script: <+input>
                                    environmentVariables: []
                                    outputVariables: []
                                    executionTarget: {}
                                timeout: 10m
              tags: {}
        - stage:
              name: Sample Deploy Stage
              identifier: Sample_Deploy_Stage
              description: ""
              type: Deployment
              spec:
                  serviceConfig:
                      serviceRef: <+input>
                      serviceDefinition:
                          spec:
                              variables: []
                          type: Kubernetes
                  infrastructure:
                      environmentRef: <+input>
                      infrastructureDefinition:
                          type: KubernetesDirect
                          spec:
                              connectorRef: <+input>
                              namespace: <+input>
                              releaseName: release-<+INFRA_KEY>
                      allowSimultaneousDeployments: false
                  execution:
                      steps:
                          - step:
                                name: Rollout Deployment
                                identifier: rolloutDeployment
                                type: K8sRollingDeploy
                                timeout: 10m
                                spec:
                                    skipDryRun: false
                      rollbackSteps:
                          - step:
                                name: Rollback Rollout Deployment
                                identifier: rollbackRolloutDeployment
                                type: K8sRollingRollback
                                timeout: 10m
                                spec: {}
              tags: {}
              failureStrategies:
                  - onFailure:
                        errors:
                            - AllErrors
                        action:
                            type: StageRollback
    """    

def test_harness_tools():
    """Test function for Harness tools"""
    print("Testing Harness Tools...")
    print("=" * 50)

    try:
        # Initialize Harness tools
        # You can either set HARNESS_API_KEY in environment or pass it directly
        harness_tools = HarnessTools()
        print("HarnessTools initialized successfully")

        # Get available tools
        tools = harness_tools.get_tools()
        print(f"Available tools: {len(tools)}")

        for i, tool in enumerate(tools):
            print(f"  {i+1}. {tool.name}: {tool.description.strip()}")

    except ValueError as e:
        print(f"Error initializing HarnessTools: {e}")
        print("\nTo test this file, you need to:")
        print("1. Set the HARNESS_API_KEY environment variable, or")
        print("2. Create a .env file with HARNESS_API_KEY=your_api_key")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

    return True


def test_get_pipeline_list_tool():
    """Test the pipeline list tool with sample data"""
    print("\nTesting HarnessGetPipelineListTool...")
    print("=" * 50)

    try:
        harness_tools = HarnessTools()
        pipeline_tool = harness_tools.tools[0]  # HarnessGetPipelineListTool

        # Test input validation
        print("Testing input validation...")
        try:
            # This should raise a validation error due to empty account_identifier
            HarnessGetPipelineListInputModel(
                account_identifier="",
                org_identifier="test_org",
                project_identifier="test_project"
            )
            print("Validation should have failed for empty account_identifier")
        except ValueError as e:
            print(f"Input validation working: {e}")

        # Test with valid input structure (but may fail API call without real credentials)
        print("\nTesting tool execution structure...")         
        result = pipeline_tool._run(
            account_identifier=os.getenv("HARNESS_ACCOUNT_ID"),
            org_identifier=os.getenv("HARNESS_ORG_ID"),
            project_identifier=os.getenv("HARNESS_PROJECT_ID"),
            body = harness_python_sdk.PipelineFilterProperties(filter_type="PipelineSetup"),
            page = 0,
            size = 25
        )

        print(f"Tool execution result: {result}")

    except Exception as e:
        print(f"Error during pipeline tool test: {e}")
        
        
def test_get_pipeline_tool():
    """Test the get pipeline tool with sample data"""
    print("\nTesting HarnessGetPipelineTool...")
    print("=" * 50)

    try:
        harness_tools = HarnessTools()
        pipeline_tool = harness_tools.tools[1]  # HarnessGetPipelineTool

        # Test with valid input structure
        print("\nTesting tool execution structure...")         
        result = pipeline_tool._run(
            account_identifier=os.getenv("HARNESS_ACCOUNT_ID"),
            org_identifier=os.getenv("HARNESS_ORG_ID"),
            project_identifier=os.getenv("HARNESS_PROJECT_ID"),
            pipeline_identifier = "CIPythonExample"
        )

        print(f"Tool execution result: {result}")

    except Exception as e:
        print(f"Error during pipeline tool test: {e}")


def test_create_pipeline_tool():
    """Test the create pipeline tool with sample data"""
    print("\nTesting HarnessGetPipelineTool...")
    print("=" * 50)

    try:
        harness_tools = HarnessTools()
        pipeline_tool = harness_tools.tools[2]  # HarnessCreatePipelineTool

        # Test with valid input structure
        print("\nTesting tool execution structure...")         
        result = pipeline_tool._run(
            account_identifier=os.getenv("HARNESS_ACCOUNT_ID"),
            org_identifier=os.getenv("HARNESS_ORG_ID"),
            project_identifier=os.getenv("HARNESS_PROJECT_ID"),
            body=yaml.safe_load(pipeline)
        )

        print(f"Tool execution result: {result}")

    except Exception as e:
        print(f"Error during pipeline tool test: {e}")

# https://apidocs.harness.io/tag/Pipeline#operation/getPipelineList
def get_pipeline_list():
    # Configure API key authorization: x-api-key
    configuration = harness_python_sdk.Configuration()
    configuration.api_key['x-api-key'] = os.getenv('HARNESS_API_KEY')

    # create an instance of the API class
    api_instance = harness_python_sdk.PipelineApi(harness_python_sdk.ApiClient(configuration))
    account_identifier = os.getenv("HARNESS_ACCOUNT_ID")
    org_identifier = os.getenv("HARNESS_ORG_ID")
    project_identifier = os.getenv("HARNESS_PROJECT_ID")
    body = harness_python_sdk.PipelineFilterProperties(filter_type="PipelineSetup")
    page = 0
    size = 25
    
    try:
        # List Pipelines
        api_response = api_instance.get_pipeline_list(account_identifier, org_identifier, project_identifier, body=body, page=page, size=size)
        pprint(api_response)
    except ApiException as e:
        print(f"Error calling PipelineApi->get_pipeline_list: {e}")
        
        
# https://apidocs.harness.io/tag/Pipeline#operation/getPipeline 
def get_pipeline():
    # Configure API key authorization: x-api-key
    configuration = harness_python_sdk.Configuration()
    configuration.api_key['x-api-key'] = os.getenv('HARNESS_API_KEY')

    # create an instance of the API class
    api_instance = harness_python_sdk.PipelineApi(harness_python_sdk.ApiClient(configuration))
    account_identifier = os.getenv("HARNESS_ACCOUNT_ID")
    org_identifier = os.getenv("HARNESS_ORG_ID")
    project_identifier = os.getenv("HARNESS_PROJECT_ID")
    pipeline_identifier = "CIPythonExample"
    page = 0
    size = 25
    
    try:
        # Get Pipeline
        api_response = api_instance.get_pipeline(account_identifier, org_identifier, project_identifier, pipeline_identifier)
        pprint(api_response)
    except ApiException as e:
        print(f"Error calling PipelineApi->get_pipeline: {e}")


# https://apidocs.harness.io/tag/Pipeline#operation/postPipelineV2
def create_pipeline():
     # Configure API key authorization: x-api-key
    configuration = harness_python_sdk.Configuration()
    configuration.api_key['x-api-key'] = os.getenv('HARNESS_API_KEY')

    # create an instance of the API class
    api_instance = harness_python_sdk.PipelineApi(harness_python_sdk.ApiClient(configuration))
    account_identifier = os.getenv("HARNESS_ACCOUNT_ID")
    org_identifier = os.getenv("HARNESS_ORG_ID")
    project_identifier = os.getenv("HARNESS_PROJECT_ID")
    body = yaml.safe_load(pipeline)

    try:
        # Create Pipeline
        api_response = api_instance.post_pipeline(body, account_identifier, org_identifier, project_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Error calling PipelineApi->post_pipeline: %s\n" % e)
                
def test_get_pipeline_list():
    print("\nRunning test: get_pipeline_list")
    get_pipeline_list()

def test_get_pipeline():
    print("\nRunning test: get_pipeline")
    get_pipeline()

def test_create_pipeline():
    print("\nRunning test: create_pipeline")
    create_pipeline()


def main():
    print("Harness Tools Test Suite")
    print("=" * 50)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "get-pipeline-list-tool":
            test_harness_tools()
            test_get_pipeline_list_tool()
        elif command == "get-pipeline-tool":
            test_harness_tools()
            test_get_pipeline_tool()
        elif command == "create-pipeline-tool":
            test_harness_tools()
            test_create_pipeline_tool()
        elif command == "list":
            test_get_pipeline_list()
        elif command == "get":
            test_get_pipeline()
        elif command == "create":
            test_create_pipeline()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: get-pipeline-list-tool, get-pipeline-tool, create-pipeline-tool, list, get, create")

    print("\n" + "=" * 50)
    print("Test complete!")
    print("\nUsage examples:")    
    print(f"  python {__file__} get-pipeline-list-tool # Test get-pipeline-list tool only")
    print(f"  python {__file__} get-pipeline-tool      # Test get-pipeline tool only")
    print(f"  python {__file__} create-pipeline-tool   # Test create-pipeline tool only")    
    print(f"  python {__file__} list                   # Test get_pipeline_list only")
    print(f"  python {__file__} get                    # Test get_pipeline only")
    print(f"  python {__file__} create                 # Test create_pipeline only")

if __name__ == "__main__":
    main()
