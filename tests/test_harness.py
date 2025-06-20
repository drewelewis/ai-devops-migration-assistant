import os
import sys
import logging
import harness_python_sdk

from dotenv import load_dotenv
from harness_python_sdk.rest import ApiException
from pprint import pprint

from tools.harness_tools import HarnessTools, HarnessGetPipelineListInputModel

load_dotenv(override=True)
logger = logging.getLogger(__name__)

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


def test_pipeline_list_tool():
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


def interactive_test():
    """Interactive test mode"""
    print("\nInteractive Test Mode")
    print("=" * 50)

    try:
        harness_tools = HarnessTools()
        pipeline_tool = harness_tools.tools[0]

        print("Enter test parameters (press Enter for defaults):")
        account_id = input("Account Identifier (required): ").strip()
        if not account_id:
            print("Account identifier is required for testing")
            return

        org_id = input("Organization Identifier (required): ").strip()
        if not org_id:
            print("Organization identifier is required for testing")
            return

        project_id = input("Project Identifier (required): ").strip()
        if not project_id:
            print("Project identifier is required for testing")
            return

        search_term = input("Search term (optional): ").strip() or None

        print(f"\nExecuting pipeline list query...")
        result = pipeline_tool._run(
            account_identifier=account_id,
            org_identifier=org_id,
            project_identifier=project_id,
            body = harness_python_sdk.PipelineFilterProperties(filter_type="PipelineSetup"),
            page = 0,
            size = 25
        )

        print(f"Result: {result}")

    except Exception as e:
        print(f"Error during interactive test: {e}")


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
            

def main():
    # Main execution
    print("Harness Tools Test Suite")
    print("=" * 50)

    # Check if we have any command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "interactive":
            interactive_test()
        elif command == "pipeline":
            test_pipeline_list_tool()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: interactive, pipeline")
    else:
        # Run basic tests
        if test_harness_tools():
            get_pipeline_list()
            test_pipeline_list_tool()

        print("\n" + "=" * 50)
        print("Test complete!")
        print("\nUsage examples:")
        print(f"  python {__file__} interactive  # Interactive testing")
        print(f"  python {__file__} pipeline     # Test pipeline tool only")
        print(f"  python {__file__}              # Run all basic tests")
        
if __name__ == "__main__":    
    main()