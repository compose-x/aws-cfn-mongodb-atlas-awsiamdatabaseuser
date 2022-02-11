# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]
    typeConfiguration: Optional["TypeConfigurationModel"]


@dataclass
class ResourceModel(BaseModel):
    AwsIamResource: Optional[str]
    ApiKeys: Optional["_ApiKeyDefinition"]
    ProjectId: Optional[str]
    DatabaseAccess: Optional[MutableMapping[str, "_DatabaseAccessDefinition"]]
    Scopes: Optional[MutableMapping[str, str]]
    MongoDbUsername: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            AwsIamResource=json_data.get("AwsIamResource"),
            ApiKeys=ApiKeyDefinition._deserialize(json_data.get("ApiKeys")),
            ProjectId=json_data.get("ProjectId"),
            DatabaseAccess=json_data.get("DatabaseAccess"),
            Scopes=json_data.get("Scopes"),
            MongoDbUsername=json_data.get("MongoDbUsername"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class ApiKeyDefinition(BaseModel):
    PrivateKey: Optional[str]
    PublicKey: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_ApiKeyDefinition"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ApiKeyDefinition"]:
        if not json_data:
            return None
        return cls(
            PrivateKey=json_data.get("PrivateKey"),
            PublicKey=json_data.get("PublicKey"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ApiKeyDefinition = ApiKeyDefinition


@dataclass
class DatabaseAccessDefinition(BaseModel):
    RoleName: Optional[str]
    CollectionName: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_DatabaseAccessDefinition"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_DatabaseAccessDefinition"]:
        if not json_data:
            return None
        return cls(
            RoleName=json_data.get("RoleName"),
            CollectionName=json_data.get("CollectionName"),
        )


# work around possible type aliasing issues when variable has same name as a model
_DatabaseAccessDefinition = DatabaseAccessDefinition


@dataclass
class TypeConfigurationModel(BaseModel):
    @classmethod
    def _deserialize(
        cls: Type["_TypeConfigurationModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TypeConfigurationModel"]:
        if not json_data:
            return None
        return cls()


# work around possible type aliasing issues when variable has same name as a model
_TypeConfigurationModel = TypeConfigurationModel
