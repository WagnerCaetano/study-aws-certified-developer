"""Live DynamoDB tests against LocalStack (create / exercise / teardown)."""

from __future__ import annotations

import importlib
import os
import uuid
from contextlib import contextmanager

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
put_item = _mod.put_item
get_item = _mod.get_item
query_by_pk = _mod.query_by_pk
update_item = _mod.update_item
delete_item = _mod.delete_item

from common.aws_client import get_resource, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


@contextmanager
def temp_table():
    _require_localstack()
    ddb = get_resource("dynamodb")
    name = f"ex05-{uuid.uuid4().hex[:10]}"
    table = ddb.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    try:
        yield table
    finally:
        try:
            table.delete()
        except ClientError:
            pass


def test_put_and_get():
    with temp_table() as table:
        put_item(table, {"pk": "USER#1", "name": "Alice"})
        item = get_item(table, {"pk": "USER#1"})
        assert item is not None
        assert item["name"] == "Alice"
        assert item["pk"] == "USER#1"


def test_put_condition_rejects_duplicate():
    with temp_table() as table:
        put_item(table, {"pk": "USER#1", "name": "Alice"})
        raised = False
        try:
            put_item(table, {"pk": "USER#1", "name": "Bob"})
        except ClientError as e:
            raised = True
            assert e.response["Error"]["Code"] in (
                "ConditionalCheckFailedException",
                "TransactionCanceledException",
            )
        assert raised, "duplicate put should raise ConditionalCheckFailedException"


def test_query_by_pk():
    with temp_table() as table:
        put_item(table, {"pk": "USER#42", "name": "Zed"})
        items = query_by_pk(table, "pk", "USER#42")
        assert len(items) == 1
        assert items[0]["name"] == "Zed"


def test_update_item():
    with temp_table() as table:
        put_item(table, {"pk": "USER#1", "name": "Alice"})
        update_item(table, {"pk": "USER#1"}, {"name": "Bob", "age": 30})
        item = get_item(table, {"pk": "USER#1"})
        assert item["name"] == "Bob"
        assert int(item["age"]) == 30


def test_delete_item():
    with temp_table() as table:
        put_item(table, {"pk": "USER#1", "name": "Alice"})
        delete_item(table, {"pk": "USER#1"})
        assert get_item(table, {"pk": "USER#1"}) is None


def test_delete_missing_fails():
    with temp_table() as table:
        raised = False
        try:
            delete_item(table, {"pk": "MISSING"})
        except ClientError:
            raised = True
        assert raised, "delete of missing pk should fail condition"
