
from Trienode import TrieNode


class Trie:
    def __init__(self):
        self.root = TrieNode()  # Initialize the root node of the Trie
    # Time Complexity: O(1) for initialization

    def insert(self, product_name, product_id):
        """
        Inserts a product name and its associated product ID into the Trie.
        
        :param product_name: The name of the product to be inserted.
        :param product_id: The ID of the product to be inserted.
        """
        node = self.root
        for char in product_name:
            if char not in node.children:
                node.children[char] = TrieNode()  # Create a new TrieNode if the character is not already a child
            node = node.children[char]  # Move to the child node
            node.product_ids.add(product_id)  # Add the product ID to the current node's product_ids set
        node.is_end_of_word = True  # Mark the last node as the end of a word
    # Time Complexity: O(m), where m is the length of the product_name
    # Explanation: The method iterates over each character in the product_name, performing constant-time operations for each character.

    def search(self, prefix):
        """
        Searches for a prefix in the Trie and returns the list of product IDs associated with the prefix.
        
        :param prefix: The prefix to be searched in the Trie.
        :return: A list of product IDs associated with the prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Return an empty list if the prefix is not found
            node = node.children[char]  # Move to the child node
        return list(node.product_ids)  # Return the list of product IDs associated with the last node of the prefix
    # Time Complexity: O(m), where m is the length of the prefix
    # Explanation: The method iterates over each character in the prefix, performing constant-time operations for each character.