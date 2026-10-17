import json
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONFIG = {
    'table_name': 'default',
    'max_retries': 1,
    'timeout': 28
}


def process_item(item):
    """Process a single item with error handling."""
    return {'id': item.get('id'), 'processed': True, 'timestamp': int(time.time())}


def handler(event, context):
    remaining_ms = context.get_remaining_time_in_millis() if context else 30000

    logger.info(f"Processing event, time remaining: {remaining_ms}ms")

    try:
        items = event.get('items', [])
        processed = []
        for item in items:
            if context and context.get_remaining_time_in_millis() < 5000:
                logger.warning("Approaching timeout, returning partial results")
                break
            processed.append(process_item(item))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed': len(processed),
                'total': len(items),
                'table': CONFIG['table_name']
            })
        }
    except Exception as e:
        logger.error(f"Error processing: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
