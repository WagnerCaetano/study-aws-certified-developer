"""DynamoDB CRUD helpers against a LocalStack Table resource."""

from boto3.dynamodb.conditions import Key


def put_item(table, item):
    """Put an item; fail if pk already exists."""
    table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(pk)",
    )


def get_item(table, key):
    """Return the item for ``key``, or None if missing."""
    resp = table.get_item(Key=key)
    return resp.get("Item")


def query_by_pk(table, pk_name, pk_value):
    """Query all items with the given partition key."""
    resp = table.query(KeyConditionExpression=Key(pk_name).eq(pk_value))
    return resp.get("Items", [])


def update_item(table, key, updates):
    """SET each attribute in ``updates`` on the item identified by ``key``."""
    set_parts = []
    values = {}
    names = {}
    for i, (attr, value) in enumerate(updates.items()):
        name_key = f"#a{i}"
        val_key = f":v{i}"
        names[name_key] = attr
        values[val_key] = value
        set_parts.append(f"{name_key} = {val_key}")

    table.update_item(
        Key=key,
        UpdateExpression="SET " + ", ".join(set_parts),
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
    )


def delete_item(table, key):
    """Delete the item; fail if pk does not exist."""
    table.delete_item(
        Key=key,
        ConditionExpression="attribute_exists(pk)",
    )
