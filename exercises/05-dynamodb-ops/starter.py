"""DynamoDB CRUD helpers — fix the bugs so tests pass against LocalStack."""

from boto3.dynamodb.conditions import Key


def put_item(table, item):
    """Put an item; fail if pk already exists."""
    # BUG: missing ConditionExpression — overwrites silently
    table.put_item(Item=item)


def get_item(table, key):
    """Return the item for ``key``, or None if missing."""
    # BUG: returns whole response instead of Item
    return table.get_item(Key=key)


def query_by_pk(table, pk_name, pk_value):
    """Query all items with the given partition key."""
    # BUG: wrong KeyConditionExpression (string, not Key condition)
    resp = table.query(KeyConditionExpression=f"{pk_name} = {pk_value}")
    return resp.get("Items", [])


def update_item(table, key, updates):
    """SET each attribute in ``updates`` on the item identified by ``key``."""
    # BUG: builds invalid UpdateExpression without placeholders
    table.update_item(
        Key=key,
        UpdateExpression="SET " + ", ".join(updates.keys()),
    )


def delete_item(table, key):
    """Delete the item; fail if pk does not exist."""
    # BUG: missing ConditionExpression
    table.delete_item(Key=key)
