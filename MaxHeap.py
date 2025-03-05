class MaxHeap:
    def __init__(self):
        self.heaplist = []  # Initialize with an empty list
        self.currsize = 0  # Initialize the current size to 0
    # Time Complexity: O(1) for initialization

    def push(self, item):
        """
        Insert a new item into the heap.
        
        :param item: The item to be inserted.
        """
        self.heaplist.append(item)  # Add the item to the end of the list
        self.currsize += 1  # Increment the current size
        self._upheap(self.currsize - 1)  # Maintain the heap property going up
    # Time Complexity: O(log n)
    # Explanation: Inserting an item involves appending to the list (O(1)) and maintaining the heap property (O(log n)).

    def pop(self):
        """
        Remove and return the largest item from the heap.
        
        :return: The largest item from the heap.
        """
        if self.currsize == 0:
            return None  # Return None if the heap is empty
        root = self.heaplist[0]  # Get the max item (root of the heap)
        self.heaplist[0] = self.heaplist[-1]  # Move the last item to the root
        self.heaplist.pop()  # Remove the last item
        self.currsize -= 1  # Decrement the current size
        self._downheap(0)  # Maintain the heap property going down
        return root
    # Time Complexity: O(log n)
    # Explanation: Removing the max item involves removing the root (O(1)) and maintaining the heap property (O(log n)).

    def _upheap(self, index):
        """
        Maintain the heap property going up.
        
        :param index: The index of the item to be moved up.
        """
        while index > 0:
            parent_index = (index - 1) // 2  # Calculate the parent index
            if self.heaplist[index][0] > self.heaplist[parent_index][0]:  # Compare the item with its parent
                self.heaplist[index], self.heaplist[parent_index] = self.heaplist[parent_index], self.heaplist[index]  # Swap if the item is greater
                index = parent_index  # Move to the parent index
            else:
                break
    # Time Complexity: O(log n)
    # Explanation: Maintaining the heap property going up involves comparing and potentially swapping items up the tree, which takes O(log n) time.

    def _downheap(self, index):
        """
        Maintain the heap property going down.
        
        :param index: The index of the item to be moved down.
        """
        while (index * 2) + 1 < self.currsize:
            max_child_index = self._max_child(index)  # Get the index of the maximum child
            if self.heaplist[index][0] < self.heaplist[max_child_index][0]:  # Compare the item with its maximum child
                self.heaplist[index], self.heaplist[max_child_index] = self.heaplist[max_child_index], self.heaplist[index]  # Swap if the item is less
                index = max_child_index  # Move to the maximum child index
            else:
                break
    # Time Complexity: O(log n)
    # Explanation: Maintaining the heap property going down involves comparing and potentially swapping items down the tree, which takes O(log n) time.

    def _max_child(self, index):
        """
        Return the index of the maximum child.
        
        :param index: The index of the parent item.
        :return: The index of the maximum child.
        """
        if (index * 2) + 2 >= self.currsize:  # If there is no right child
            return (index * 2) + 1  # Return the left child index
        if self.heaplist[(index * 2) + 1][0] > self.heaplist[(index * 2) + 2][0]:  # Compare the left and right children
            return (index * 2) + 1  # Return the left child index if it is greater
        else:
            return (index * 2) + 2  # Return the right child index if it is greater
    # Time Complexity: O(1)
    # Explanation: Finding the maximum child involves comparing two children, which takes constant time.

    def is_empty(self):
        """
        Check if the heap is empty.
        
        :return: True if the heap is empty, False otherwise.
        """
        return self.currsize == 0
    # Time Complexity: O(1)
    # Explanation: Checking if the heap is empty involves comparing the current size to 0, which takes constant time.
