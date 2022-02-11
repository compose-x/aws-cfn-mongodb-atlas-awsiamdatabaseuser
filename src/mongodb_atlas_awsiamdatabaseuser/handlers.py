import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)
from mongodb_atlas_api_sdk.atlas_api_sdk import setup_logging
from mongodb_atlas_api_sdk.errors import (
    DatabaseUserConflict,
    DatabaseUserDuplicateDatabaseRole,
    DatabaseUserInvalidAttribute,
    DatabaseUserMissingAttribute,
    DatabaseUserNotFound,
    GenericForbidden,
    GenericNotFound,
    GenericUnauthorized,
    IpAddressNotOnAccessList,
)

from .models import ResourceHandlerRequest, ResourceModel
from .user_mgmt import create_update_user, initialize_database_user

# Use this logger to forward log messages to CloudWatch Logs.
LOG = setup_logging()
# LOG.setLevel(logging.INFO)

TYPE_NAME = "MongoDb::Atlas::AwsIamDatabaseUser"
resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    print("Action.CREATE")
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    progress.status = OperationStatus.FAILED
    try:
        user = initialize_database_user(model)
        create_update_user(user, model, Action.CREATE)
        primary_identifier = user.username
        model.MongoDbUsername = user.username
        progress.status = OperationStatus.SUCCESS
        progress.message = f"Action.CREATE - SUCCESS"
        return progress
    except DatabaseUserConflict as error:
        print(error)
        progress.errorCode = HandlerErrorCode.AlreadyExists
        progress.message = f"Action.CREATE - Resource already exists"
        return progress
    except (IpAddressNotOnAccessList, GenericForbidden, GenericUnauthorized) as error:
        print(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.CREATE {error}"
        return progress
    except (
        DatabaseUserInvalidAttribute,
        DatabaseUserDuplicateDatabaseRole,
        ValueError,
        AttributeError,
    ) as error:
        print(f"Action.CREATE {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.CREATE - {error}"
        return progress
    except Exception as error:
        print(f"Action.CREATE {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.CREATE - Unmanaged error - {error}"
        return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    print("Action.READ")
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.FAILED,
        resourceModel=model,
    )
    try:
        user = initialize_database_user(model)
        user.set_from_api_describe(**user.read())
        progress.status = OperationStatus.SUCCESS
        progress.message = "Action.READ SUCCESS"
        progress.resourceModel = model
        return progress
    except (DatabaseUserNotFound, GenericNotFound) as error:
        print(f"Action.READ {error}")
        progress.status = OperationStatus.FAILED
        progress.errorCode = HandlerErrorCode.NotFound
        return progress
    except (IpAddressNotOnAccessList, GenericForbidden) as error:
        print(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.READ {error}"
        return progress
    except Exception as error:
        print(f"Action.CREATE {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.CREATE - Unmanaged error - {error}"
        return progress


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    print("Action.UPDATE")
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    progress.status = OperationStatus.FAILED
    try:
        user = initialize_database_user(model)
        create_update_user(user, model, Action.UPDATE)
        progress.status = OperationStatus.SUCCESS
        return ProgressEvent(
            status=progress.status,
            message=f"Action.UPDATE {user} Updated successfully",
            resourceModel=model,
        )
    except (DatabaseUserNotFound, GenericNotFound) as error:
        print(f"Action.UPDATE {error}")
        progress.errorCode = HandlerErrorCode.NotFound
        progress.message = f"Action.UPDATE {error}"
        return progress
    except DatabaseUserConflict as error:
        print(f"Action.UPDATE {error}")
        progress.message = f"Action.UPDATE {error}"
        progress.errorCode = HandlerErrorCode.AlreadyExists
        return progress
    except (IpAddressNotOnAccessList, GenericForbidden) as error:
        print(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.CREATE {error}"
        return progress
    except (
        DatabaseUserInvalidAttribute,
        DatabaseUserMissingAttribute,
        DatabaseUserDuplicateDatabaseRole,
        GenericUnauthorized,
        ValueError,
        AttributeError,
    ) as error:
        print(f"Action.UPDATE - {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.UPDATE - {error}"
        return progress
    except Exception as error:
        print(f"Action.CREATE {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.UPDATE - Unmanaged error - {error}"
        return progress


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    print("Action.DELETE")
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )
    progress.status = OperationStatus.FAILED
    try:
        user = initialize_database_user(model)
        user.delete()
        progress.status = OperationStatus.SUCCESS
        progress.message = f"Action.DELETE SUCCESS"
        return progress
    except (DatabaseUserNotFound, GenericNotFound) as error:
        progress.errorCode = HandlerErrorCode.NotFound
        progress.message = f"Action.DELETE {error}"
        print(f"Action.DELETE {error}")
        return progress
    except (IpAddressNotOnAccessList, GenericForbidden) as error:
        print(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.CREATE {error}"
        return progress
    except GenericUnauthorized as error:
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.DELETE {error}"
        print(f"Action.DELETE {error}")
        return progress
    except Exception as error:
        print(f"Action.DELETE - Unmanaged error - {error}")
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.DELETE - Unmanaged error - {error}"
        return progress


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    print("Action.LIST")
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )
