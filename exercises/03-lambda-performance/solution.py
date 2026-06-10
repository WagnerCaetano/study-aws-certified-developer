import json
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Fix: Initialize clients OUTSIDE the handler for connection reuse
# This avoids cold-start re-initialization
CONFIG = {
    'table_name': os.environ.get('TABLE_NAME', 'default'),
    'max_retries': 3,
    'timeout': 28  # Stay under Lambda timeout
}

def process_item(item):
    """Process a single item with error handling."""
    if not item or 'id' not in item:
        raise ValueError("Item must have an 'id' field")
    return {'id': item['id'], 'processed': True, 'timestamp': int(time.time())}

def handler(event, context):
    # Fix: Check remaining time to avoid timeout
    remaining_ms = context.get_remaining_time_in_millis() if context else 30000
    
    logger.info(f"Processing event, time remaining: {remaining_ms}ms")
    
    try:
        items = event.get('items', [])
        if not items:
            # Fix: Return early for empty batches
            return {'statusCode': 200, 'body': json.dumps({'processed': 0})}
        
        processed = []
        for item in items:
            # Fix: Check if we're running out of time
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
