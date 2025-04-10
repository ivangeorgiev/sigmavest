import os
import time
import pytest
from sigmavest.cache.file_cache import FileCache, NotInCacheError


class TestFileCache:
    def test_put_and_get(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=3600)
        key = "test_key"
        data = {"value": 42}

        # Store data in the cache
        cache.put(key, data)
        # Retrieve data from the cache
        retrieved_data = cache.get(key)

        assert retrieved_data == data

    def test_cache_expiration(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=1)  # 1-second TTL
        key = "test_key"
        data = {"value": 42}

        # Store data in the cache
        cache.put(key, data)
        # Simulate expiration for one of the cache files
        cache_path = cache._get_cache_path(key)
        os.utime(cache_path, (time.time() - 4000, time.time() - 4000))

        # Attempt to retrieve expired data
        with pytest.raises(NotInCacheError):
            cache.get(key)

    def test_not_in_cache_exception(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=3600)
        key = "nonexistent_key"

        # Attempt to retrieve non-existent data
        with pytest.raises(NotInCacheError):
            cache.get(key)

    def test_sanitize_filename(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=3600)
        sanitized = cache._sanitize_filename("invalid/filename?*")
        assert sanitized == "invalid_filename__"

    def test_is_cache_valid(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=3600)
        key = "test_key"
        data = {"value": 42}

        # Store data in the cache
        cache.put(key, data)
        cache_path = cache._get_cache_path(key)

        # Check if the cache is valid
        assert cache._is_cache_valid(cache_path)

        # Simulate expiration
        os.utime(cache_path, (time.time() - 4000, time.time() - 4000))
        assert not cache._is_cache_valid(cache_path)

    def test_get_with_not_found_callback(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=3600)
        key = "missing_key"

        # Define a callback to provide data if the key is not found
        def not_found_callback():
            return {"value": 99}

        # Retrieve data using the callback
        retrieved_data = cache.get(key, not_found_callback=not_found_callback)

        # Verify the data was retrieved and stored in the cache
        assert retrieved_data == {"value": 99}
        assert cache.get(key) == {"value": 99}

    def test_vacuum(self, tmpdir):
        cache_dir = tmpdir.mkdir("cache")
        cache = FileCache(cache_dir=str(cache_dir), ttl=1)  # 1-second TTL
        key1 = "key1"
        key2 = "key2"
        data1 = {"value": 1}
        data2 = {"value": 2}

        # Store data in the cache
        cache.put(key1, data1)
        cache.put(key2, data2)

        # Ensure both files exist
        cache_path1 = cache._get_cache_path(key1)
        cache_path2 = cache._get_cache_path(key2)
        assert os.path.exists(cache_path1)
        assert os.path.exists(cache_path2)

        # Simulate expiration for one of the cache files
        os.utime(cache_path1, (time.time() - 4000, time.time() - 4000))

        # Run the vacuum method
        cache.vacuum()

        # Verify that the expired file is removed and the valid file remains
        assert not os.path.exists(cache_path1)
        assert os.path.exists(cache_path2)

