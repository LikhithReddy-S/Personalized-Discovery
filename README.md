# Recommendation System

## Overview
This project implements a **Recommendation System** using various data structures such as **HashMap, Trie, and MaxHeap**. The system allows users to:

- Add products to the recommendation system.
- Record user interactions with products (e.g., views, purchases, likes).
- Get product recommendations based on user interactions.
- Search for products by name or category.
- Display all user-product interactions.

## Project Structure
```
Personalized-Discovery/
│── README.md  # Project documentation
│── problem.txt #problem statement
│── hashmap.py  # HashMap implementation
│── trie.py  # Trie implementation
│── trieNode.py  # Trienode implementation
│── maxheap.py  # MaxHeap implementation
│── recommendation.py  # Core recommendation logic
```

## Installation & Usage
1. **Clone the Repository**
   ```sh
   git clone https://github.com/LikhithReddy-S/Personalized-Discovery.git
   cd Personalized-Discovery
   ```

2. **Run the Application**
   ```sh
   python main.py
   ```

## Features
- **Efficient Product Search**: Uses Trie for fast product name lookups.
- **User-Product Interaction Tracking**: Stores user interactions using HashMap.
- **Recommendation Engine**: Uses similarity scores and MaxHeap to suggest products.

## Example Usage
```python
system = RecommendationSystem()
system.add_product("p1", "Laptop", "Electronics")
system.add_interaction("user1", "p1", 5)
recommendations = system.get_recommendations("user1", 3)
print(recommendations)
```

## Contributors
- Likhith Reddy
- Team Members (Add Names)

## License
This project is open-source. You may use and modify it as needed.

