import json
import time

class SimpleCache:
    """Simple in-memory cache simulating ElastiCache."""
    
    def __init__(self):
        self._store = {}
        self._ttl = {}
    
    def get(self, key):
        if key in self._store:
            if self._ttl.get(key, float('inf')) > time.time():
                return self._store[key]
            else:
                del self._store[key]
                self._ttl.pop(key, None)
        return None
    
    def set(self, key, value, ttl_seconds=3600):
        self._store[key] = value
        self._ttl[key] = time.time() + ttl_seconds
    
    def delete(self, key):
        self._store.pop(key, None)
        self._ttl.pop(key, None)

# Simulated database
_mock_db = {}

def mock_db_get(user_id):
    """Simulate a database read."""
    return _mock_db.get(user_id)

def mock_db_set(user_id, data):
    """Simulate a database write."""
    _mock_db[user_id] = data

cache = SimpleCache()

def get_user_with_cache(user_id):
    """Lazy loading pattern: check cache first, then DB."""
    # Fix: Check cache first
    cached = cache.get(f'user:{user_id}')
    if cached:
        return cached
    
    # Cache miss - get from DB
    user = mock_db_get(user_id)
    if user:
        cache.set(f'user:{user_id}', user, ttl_seconds=3600)
    return user

def save_user_with_cache(user_id, data):
    """Write-through pattern: update both cache and DB."""
    # Fix: Write to both cache and DB
    mock_db_set(user_id, data)
    cache.set(f'user:{user_id}', data, ttl_seconds=3600)
    return data
