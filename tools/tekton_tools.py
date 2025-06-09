import os
from typing import List, Optional, Type
from langchain_core.callbacks import  CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, field_validator

from dotenv import load_dotenv
load_dotenv(override=True)

from operations.tekton_operations import TektonOperations

teckton_Operations=TektonOperations()

class TektonTools():
    class TektonGetNamespacesTool(BaseTool):
        name: str = "TektonGetNamespacesTool"
        description: str = """Usefull when you want to get all the namespaces from tekton.
    """.strip()
        return_direct: bool = True

        def _run(self) -> str:
            namespaces=teckton_Operations.get_namespaces()
            return str(namespaces)
    
    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.TektonGetNamespacesTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools

