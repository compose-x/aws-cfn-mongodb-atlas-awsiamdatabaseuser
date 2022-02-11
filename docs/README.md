# MongoDb::Atlas::AwsIamDatabaseUser

CRUD for AWS IAM MongoDB users in a project for your clusters/databases.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "MongoDb::Atlas::AwsIamDatabaseUser",
    "Properties" : {
        "<a href="#awsiamresource" title="AwsIamResource">AwsIamResource</a>" : <i>String</i>,
        "<a href="#apikeys" title="ApiKeys">ApiKeys</a>" : <i><a href="apikeydefinition.md">apiKeyDefinition</a></i>,
        "<a href="#projectid" title="ProjectId">ProjectId</a>" : <i>String</i>,
        "<a href="#databaseaccess" title="DatabaseAccess">DatabaseAccess</a>" : <i><a href="databaseaccess.md">DatabaseAccess</a></i>,
        "<a href="#scopes" title="Scopes">Scopes</a>" : <i><a href="scopes.md">Scopes</a></i>,
    }
}
</pre>

### YAML

<pre>
Type: MongoDb::Atlas::AwsIamDatabaseUser
Properties:
    <a href="#awsiamresource" title="AwsIamResource">AwsIamResource</a>: <i>String</i>
    <a href="#apikeys" title="ApiKeys">ApiKeys</a>: <i><a href="apikeydefinition.md">apiKeyDefinition</a></i>
    <a href="#projectid" title="ProjectId">ProjectId</a>: <i>String</i>
    <a href="#databaseaccess" title="DatabaseAccess">DatabaseAccess</a>: <i><a href="databaseaccess.md">DatabaseAccess</a></i>
    <a href="#scopes" title="Scopes">Scopes</a>: <i><a href="scopes.md">Scopes</a></i>
</pre>

## Properties

#### AwsIamResource

The AWS IAM user or role ARN used as the database username.

_Required_: Yes

_Type_: String

_Pattern_: <code>^arn:aws(?:-[a-z-]+)?:iam::[0-9]{12}:(role|user)/[\S]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ApiKeys

_Required_: Yes

_Type_: <a href="apikeydefinition.md">apiKeyDefinition</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ProjectId

Unique identifier of the Atlas project to which the user belongs.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### DatabaseAccess

_Required_: Yes

_Type_: <a href="databaseaccess.md">DatabaseAccess</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Scopes

_Required_: No

_Type_: <a href="scopes.md">Scopes</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the MongoDbUsername.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### MongoDbUsername

MongoDB username for the AWS IAM resource.
