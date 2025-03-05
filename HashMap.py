import time
class HashMap:
    def __init__(self, size=100):
        """
        Initializes the HashMap with a specified size.
        
        :param size: The number of buckets in the hash map.
        """
        self.size = size
        self.buckets = [[] for _ in range(size)]  # Create a list of empty lists (buckets)
    # Time Complexity: O(n), where n is the size of the hash map
    # Explanation: Initializing the hash map involves creating a list of empty lists, which takes O(n) time.

    def _hash(self, key):
        """
        Computes the hash value for a given key.
        
        :param key: The key to be hashed.
        :return: The hash value of the key.
        """
        return hash(key) % self.size
    # Time Complexity: O(1)
    # Explanation: Hashing a key and computing the index takes constant time.

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash map.
        
        :param key: The key to be inserted.
        :param value: The value to be associated with the key.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                self.buckets[index][i] = (key, value)  # Update if key exists
                return
        self.buckets[index].append((key, value))  # Insert new key-value pair
    # Time Complexity: O(1) on average, O(n) in the worst case
    # Explanation: Inserting a key-value pair involves computing the hash value and appending to the bucket, which takes O(1) time on average. In the worst case, all keys hash to the same bucket, making it O(n).

    def get(self, key):
        """
        Retrieves the value associated with a given key.
        
        :param key: The key to be searched.
        :return: The value associated with the key, or None if the key is not found.
        """
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return None  # Key not found
    # Time Complexity: O(1) on average, O(n) in the worst case
    # Explanation: Retrieving a value involves computing the hash value and searching the bucket, which takes O(1) time on average. In the worst case, all keys hash to the same bucket, making it O(n).

    def remove(self, key):
        """
        Removes a key-value pair from the hash map.
        
        :param key: The key to be removed.
        :return: None
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                del self.buckets[index][i]
                return
        return None  # Key not found
    # Time Complexity: O(1) on average, O(n) in the worst case
    # Explanation: Removing a key-value pair involves computing the hash value and searching the bucket, which takes O(1) time on average. In the worst case, all keys hash to the same bucket, making it O(n).

    def contains(self, key):
        """
        Checks if a key exists in the hash map.
        
        :param key: The key to be checked.
        :return: True if the key exists, False otherwise.
        """
        return self.get(key) is not None
    # Time Complexity: O(1) on average, O(n) in the worst case
    # Explanation: Checking if a key exists involves retrieving the value associated with the key, which takes O(1) time on average. In the worst case, all keys hash to the same bucket, making it O(n).