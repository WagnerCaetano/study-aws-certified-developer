from solution import get_user_with_cache, save_user_with_cache, cache, _mock_db

def setup():
    _mock_db.clear()
    cache._store.clear()
    cache._ttl.clear()

def test_lazy_loading():
    setup()
    _mock_db['user-1'] = {'id': 'user-1', 'name': 'Alice'}
    
    # First call - cache miss, reads from DB
    result = get_user_with_cache('user-1')
    assert result['name'] == 'Alice'
    
    # Second call - cache hit
    result2 = get_user_with_cache('user-1')
    assert result2['name'] == 'Alice'

def test_write_through():
    setup()
    save_user_with_cache('user-2', {'id': 'user-2', 'name': 'Bob'})
    
    # Should be in cache
    cached = cache.get('user:user-2')
    assert cached['name'] == 'Bob'
    
    # Should be in DB
    db_result = _mock_db.get('user-2')
    assert db_result['name'] == 'Bob'

def test_cache_miss_returns_none():
    setup()
    result = get_user_with_cache('nonexistent')
    assert result is None
