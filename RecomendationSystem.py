
import time
import HashMap
import MaxHeap
import Trie


class RecommendationSystem:
    def __init__(self):
        """
        Initializes the RecommendationSystem with various data structures.
        """
        self.user_to_product = HashMap()  # Maps user IDs to products they have interacted with
        self.product_to_user = HashMap()  # Maps product IDs to users who have interacted with them
        self.trie = Trie()  # Trie for efficient product name search
        self.product_details = HashMap()  # Maps product IDs to product details (name, category)
        self.category_to_products = HashMap()  # Maps categories to sets of product IDs
    # Time Complexity: O(1) for initialization
    # Explanation: Initializing the RecommendationSystem involves creating instances of HashMap and Trie, which are constant-time operations.

    def add_product(self, product_id, product_name, category):
        """
        Adds a product to the recommendation system.
        
        :param product_id: The ID of the product to be added.
        :param product_name: The name of the product to be added.
        :param category: The category of the product to be added.
        """
        self.product_details.insert(product_id, (product_name, category))  # Insert product details into the HashMap
        self.trie.insert(product_name, product_id)  # Insert product name into the Trie
        if not self.category_to_products.contains(category):
            self.category_to_products.insert(category, set())  # Insert category if it doesn't exist
        self.category_to_products.get(category).add(product_id)  # Add product ID to the category set
    # Time Complexity: O(m + n), where m is the length of the product_name and n is the number of products in the category
    # Explanation: Inserting into the HashMap and Trie takes O(m) time, and checking/inserting into the category HashMap takes O(1) on average. Adding to the set takes O(1) on average.

    def add_interaction(self, user_id, product_id, score, interaction_type):
        """
        Adds an interaction between a user and a product.
        
        :param user_id: The ID of the user.
        :param product_id: The ID of the product.
        :param score: The score of the interaction.
        :param interaction_type: The type of interaction (e.g., view, purchase).
        """
        timestamp = time.time()  # Get the current timestamp
        if not self.user_to_product.contains(user_id):
            self.user_to_product.insert(user_id, HashMap())  # Insert user ID if it doesn't exist
        self.user_to_product.get(user_id).insert(product_id, (score, interaction_type, timestamp))  # Insert interaction details

        if not self.product_to_user.contains(product_id):
            self.product_to_user.insert(product_id, HashMap())  # Insert product ID if it doesn't exist
        self.product_to_user.get(product_id).insert(user_id, (score, interaction_type, timestamp))  # Insert interaction details
    # Time Complexity: O(1) on average, O(n) in the worst case
    # Explanation: Inserting and retrieving from the HashMap takes O(1) time on average. In the worst case, all keys hash to the same bucket, making it O(n).

   
    def compute_similarity(self, user1, user2):
        """
        Computes the similarity score between two users based on their common product interactions.
        
        :param user1: The ID of the first user.
        :param user2: The ID of the second user.
        :return: The similarity score between the two users.
        """
        user1_products = set()
        for bucket in self.user_to_product.get(user1).buckets:
            for product, _ in bucket:
                user1_products.add(product)

        user2_products = set()
        for bucket in self.user_to_product.get(user2).buckets:
            for product, _ in bucket:
                user2_products.add(product)

        common_products = user1_products & user2_products
        if not common_products:
            return 0  # No common products

        similarity = sum((self.user_to_product.get(user1).get(p)[0] + self.user_to_product.get(user2).get(p)[0]) / 2 for p in common_products)
        return similarity / len(common_products) if common_products else 0  # Return average similarity, handle case with no common products
    # Time Complexity: O(n + m), where n is the number of products user1 has interacted with and m is the number of products user2 has interacted with
    # Explanation: The method iterates over the products of both users to create sets and then computes the intersection and similarity score.

    def _get_user_interacted_products(self, user_id):
        """
        Helper function to get all products interacted with by a user.
        
        :param user_id: The ID of the user.
        :return: A set of product IDs interacted with by the user.
        """
        user_interacted_products = set()
        if self.user_to_product.contains(user_id):
            for bucket in self.user_to_product.get(user_id).buckets:
                for product, _ in bucket:
                    user_interacted_products.add(product)
        return user_interacted_products
    # Time Complexity: O(n), where n is the number of products the user has interacted with
    # Explanation: The method iterates over the products of the user to create a set of interacted products.

    def _calculate_weighted_score(self, score, time_diff, decay_factor):
        """
        Calculates the weighted score based on time decay.
        
        :param score: The original score.
        :param time_diff: The time difference since the interaction.
        :param decay_factor: The decay factor for the score.
        :return: The weighted score.
        """
        return score * (decay_factor ** (time_diff / (60 * 60 * 24)))
    # Time Complexity: O(1)
    # Explanation: The method performs a constant-time calculation to compute the weighted score.

    def _populate_similar_products(self, user_id, user_interacted_products, decay_factor, similar_products):
        """
        Helper function to populate similar products based on interactions.
        
        :param user_id: The ID of the user.
        :param user_interacted_products: A set of products the user has interacted with.
        :param decay_factor: The decay factor for the score.
        :param similar_products: A dictionary to store similar products and their scores.
        """
        for bucket in self.user_to_product.buckets:
            for other_user, products in bucket:
                if other_user != user_id:
                    similarity_score = self.compute_similarity(user_id, other_user)

                    for other_product, (other_score, _, other_timestamp) in sum(products.buckets, []):
                        if other_product not in user_interacted_products:
                            time_diff = time.time() - other_timestamp
                            weighted_score = self._calculate_weighted_score(other_score, time_diff, decay_factor)
                            if other_product not in similar_products:
                                similar_products[other_product] = 0
                            similar_products[other_product] += weighted_score * similarity_score
    # Time Complexity: O(u * p), where u is the number of users and p is the average number of products per user
    # Explanation: The method iterates over all users and their products to compute similarity scores and populate similar products.

                            
    def get_recommendations(self, user_id, k, decay_factor=0.95):
        """
        Get top-k recommendations for a user based on weighted scores from other users' interactions.
        
        :param user_id: The ID of the user.
        :param k: The number of recommendations to return.
        :param decay_factor: The decay factor for the score.
        :return: A list of top-k recommended product IDs and their scores.
        """
        if not self.user_to_product.contains(user_id):
            return []  # Return empty list if user has no interactions

        user_interacted_products = self._get_user_interacted_products(user_id)
        similar_products = {}
        
        # Populate similar products with weighted scores
        self._populate_similar_products(user_id, user_interacted_products, decay_factor, similar_products)

        # Initialize max heap and push all similar products with their scores
        max_heap = MaxHeap()
        for product_id, score in similar_products.items():
            max_heap.push((score, product_id))

        # Extract top-k recommendations from the max heap
        recommendations = []
        for _ in range(min(k, max_heap.currsize)):
            score, product_id = max_heap.pop()
            recommendations.append((product_id, score))

        return recommendations
    # Time Complexity: O(u * p + k log p), where u is the number of users, p is the average number of products per user, and k is the number of recommendations
    # Explanation: The method involves populating similar products (O(u * p)), pushing items into the max heap (O(p log p)), and extracting top-k recommendations (O(k log p)).

    def search_products(self, query, search_by="name"):
        """
        Searches for products by name or category.
        
        :param query: The search query.
        :param search_by: The search criterion ("name" or "category").
        :return: A list of tuples containing product IDs and their names.
        """
        if search_by == "name":
            matched_product_ids = self.trie.search(query)
        elif search_by == "category":
            if self.category_to_products.contains(query):
                matched_product_ids = self.category_to_products.get(query)
            else:
                matched_product_ids = []
        else:
            return []

        return [(product_id, self.product_details.get(product_id)[0]) for product_id in matched_product_ids]
    # Time Complexity: O(m + n), where m is the length of the query and n is the number of matched products
    # Explanation: Searching by name involves querying the Trie (O(m)). Searching by category involves checking the HashMap (O(1) on average) and retrieving the product IDs (O(n)). Retrieving product details takes O(n) time.

    def display_interactions(self):
        """
        Displays all user-to-product and product-to-user interactions.
        """
        print("User to Product Interactions:")
        for bucket in self.user_to_product.buckets:
            for user, products in bucket:
                product_interactions = []
                for product_bucket in products.buckets:
                    for product, details in product_bucket:
                        product_interactions.append((product, details))
                print(f"{user}: {product_interactions}")

        print("\nProduct to User Interactions:")
        for bucket in self.product_to_user.buckets:
            for product, users in bucket:
                user_interactions = []
                for user_bucket in users.buckets:
                    for user, details in user_bucket:
                        user_interactions.append((user, details))
                print(f"{product}: {user_interactions}")
    # Time Complexity: O(u * p), where u is the number of users and p is the average number of products per user
    # Explanation: The method iterates over all users and their products to display interactions, resulting in O(u * p) time complexity.
    # Driver code
if __name__ == "__main__":
    system = RecommendationSystem()

    system.add_product("p1", "laptop", "electronics")
    system.add_product("p2", "smartphone", "electronics")
    system.add_product("p3", "smartwatch", "wearables")
    system.add_product("p4", "laptop cover", "accessories")
    system.add_product("p5", "tablet", "electronics")
    system.add_product("p6", "headphones", "accessories")
    system.add_product("p7", "fitness tracker", "wearables")
    system.add_product("p8", "camera", "electronics")

    # Add interactions
    system.add_interaction("user1", "p1", 5, "purchase")
    system.add_interaction("user1", "p2", 3, "view")
    system.add_interaction("user2", "p1", 4, "purchase")
    system.add_interaction("user2", "p3", 2, "view")
    system.add_interaction("user3", "p2", 5, "like")
    system.add_interaction("user4", "p1", 5, "purchase")
    system.add_interaction("user5", "p1", 1, "view")
    system.add_interaction("user6", "p5", 4, "purchase")
    system.add_interaction("user7", "p6", 5, "view")
    system.add_interaction("user8", "p7", 5, "like")
    system.add_interaction("user9", "p8", 4, "purchase")
    system.add_interaction("user3", "p5", 5, "view")
    system.add_interaction("user9", "p2", 4, "purchase")
    system.add_interaction("user9", "p1", 4, "purchase")
while True:
    print("\nMenu:")
    print("1. Get Recommendations")
    print("2. Search Products")
    print("3. Display All Interactions")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        user_id = input("Enter user ID: ")
        k = input("Enter the number of recommendations: ")
        try:
            k = int(k)
            if k <= 0:
                raise ValueError("k must be a positive integer.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        recommendations = system.get_recommendations(user_id, k)
        print(f"\nRecommendations for user {user_id}:")
        for product_id, score in recommendations:
            product_name = system.product_details.get(product_id)[0]
            print(f"Product ID: {product_id}, Product Name: {product_name}, Weighted Score: {score:.2f}")

    elif choice == '2':
        search_by = input("Search by name (n) or category (c)? ").strip().lower()
        query = input("Enter search query: ")
        if search_by == 'n':
            results = system.search_products(query, search_by="name")
        elif search_by == 'c':
            results = system.search_products(query, search_by="category")
        else:
            print("Invalid choice")
            continue
        print(f"\nProducts matching '{query}':")
        for product_id, product_name in results:
            print(f"Product ID: {product_id}, Product Name: {product_name}")

    elif choice == '3':
        system.display_interactions()

    elif choice == '4':
        print("Thank you...!!!")
        break

    else:
        print("Invalid choice")