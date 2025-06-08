import os
from typing import List, Optional, Type
from langchain_core.callbacks import  CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, field_validator

from dotenv import load_dotenv
load_dotenv(override=True)

from operations.team_city_operations import TeamcityOperations

teamcity_Operations=TeamcityOperations()

class GithubTools():
    
    class TeamCityGetProjectsTool(BaseTool):
        name: str = "TeamCityGetProjectsTool"
        description: str = "useful for when you need get a list of projects from a TeamCity server"
        return_direct: bool = True
               
        def _run(self) -> str:
            repos=teamcity_Operations.get_projects()
            return str(repos)

    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.TeamCityGetProjectsTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools