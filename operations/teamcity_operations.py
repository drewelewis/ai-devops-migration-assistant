import os
from typing import List, Optional
from pydantic import BaseModel, Field

from dohq_teamcity import TeamCity
from dotenv import load_dotenv
load_dotenv(override=True)

TEAMCITY_URL=os.getenv('TEAMCITY_URL')
TEAMCITY_ADMIN=os.getenv('TEAMCITY_ADMIN')
TEAMCITY_ADMIN_PASSWORD=os.getenv('TEAMCITY_ADMIN_PASSWORD')


class TeamcityOperations():
    def get_projects(self) -> str:
        try:
            tc = TeamCity(TEAMCITY_URL, auth=(TEAMCITY_ADMIN, TEAMCITY_ADMIN_PASSWORD))
            # connect to TeamCity server
            projects = tc.projects.get_projects()
            return projects
        except Exception as e:
            print(f"An error occurred with TeamcityOperations.get_projects: {e}")
            return []
        finally:
            pass

    def get_all_builds(self) -> str:
        try:
            tc = TeamCity(TEAMCITY_URL, auth=(TEAMCITY_ADMIN, TEAMCITY_ADMIN_PASSWORD))
            # connect to TeamCity server
            builds = tc.builds.get_all_builds()
            return builds
        except Exception as e:
            print(f"An error occurred with TeamcityOperations.ge_builds: {e}")
            return []
        finally:
            pass
    # get all builds by project
    def get_builds_by_project(self, project_id: str) -> str:
        try:
            tc = TeamCity(TEAMCITY_URL, auth=(TEAMCITY_ADMIN, TEAMCITY_ADMIN_PASSWORD))
            # connect to TeamCity server
            builds = tc.builds.get_builds(project=project_id)
            return builds
        except Exception as e:
            print(f"An error occurred with TeamcityOperations.get_builds_by_project: {e}")
            return []
        finally:
            pass

    # get build definitions by project
    def get_build_definitions_by_build_config_id(self, build_config_id: str) -> str:
        try:
            tc = TeamCity(TEAMCITY_URL, auth=(TEAMCITY_ADMIN, TEAMCITY_ADMIN_PASSWORD))
            # connect to TeamCity server
            build_definitions = tc.build_types.get_by_id(build_config_id) 
            return build_definitions
        except Exception as e:
            print(f"An error occurred with TeamcityOperations.get_build_definitions_by_project: {e}")
            return []
        finally:
            pass

    

