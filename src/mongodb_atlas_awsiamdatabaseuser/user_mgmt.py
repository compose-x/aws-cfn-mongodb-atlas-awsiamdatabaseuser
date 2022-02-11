"""
Module to manage a new MongoDB Username
"""
import re

from cloudformation_cli_python_lib import Action
from mongodb_atlas_api_sdk.atlas_api_sdk import Atlas
from mongodb_atlas_api_sdk.atlas_project import AtlasProject
from mongodb_atlas_api_sdk.database_user import DatabaseUser

from .models import ResourceModel


def initialize_atlas_connection(user_model: ResourceModel) -> Atlas:
    """
    Defines the Atlas API client interface based on the CFN Resource model properties
    :param ResourceModel user_model:
    :rtype: Atlas
    """
    return Atlas(user_model.ApiKeys.PublicKey, user_model.ApiKeys.PrivateKey)


def initialize_atlas_project(atlas: Atlas, project_id: str) -> AtlasProject:
    """
    Defines the AtlasProject based on the CFN Resource model properties

    :param Atlas atlas:
    :param str project_id:
    :return: The Project manager
    :rtype: AtlasProject
    """
    return AtlasProject(atlas, project_id)


def initialize_database_user(user_model: ResourceModel) -> DatabaseUser:
    """
    Helper to define the DatabaseUser from the ResourceModel properties
    """
    atlas_conn = initialize_atlas_connection(user_model)
    atlas_project = initialize_atlas_project(atlas_conn, user_model.ProjectId)
    valid_username = re.compile(
        r"^arn:aws(?:-[a-z]+)?:iam::[0-9]{12}:(?P<type>role|user)/[\S]+$"
    )
    parts = valid_username.match(user_model.AwsIamResource)
    if not parts:
        raise ValueError(
            f"Username value {user_model.AwsIamResource} is not a valid IAM Role or IAM User ARN. Must match",
            valid_username.pattern,
        )
    user = DatabaseUser(
        atlas_conn,
        atlas_project,
        username=user_model.AwsIamResource,
        database=r"$external",
    )
    if user.exists:
        user.set_from_api_describe(**user.read())
    return user


def create_update_user(user: DatabaseUser, user_model: ResourceModel, action: Action):
    """
    Create a new DB User
    """
    for _db_name, _access_definition in user_model.DatabaseAccess.items():
        user.add_role(
            name=_access_definition.RoleName,
            database=_db_name,
            collection=_access_definition.CollectionName
            if _access_definition.CollectionName
            else None,
        )
    if user_model.Scopes:
        for _scope_db, _scope_type in user_model.Scopes.items():
            user.add_scope(_scope_db, _scope_type)
    if action == Action.CREATE:
        user.create()
    elif action == Action.UPDATE:
        user.update()


def list_users(user_model: ResourceModel):
    """
    Return the list of all users from the given Atlas Project
    """
    atlas_conn = initialize_atlas_connection(user_model)
    atlas_project = initialize_atlas_project(atlas_conn, user_model.ProjectId)
    return atlas_project.users.values()
