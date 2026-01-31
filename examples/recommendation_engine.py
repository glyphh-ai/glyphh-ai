"""
Product Recommendation Engine Example

Generate personalized product recommendations based on user preferences,
purchase history, and behavioral patterns using similarity search.

Key Principle: Recommendations emerge from similarity to user preferences
and successful past purchases, not hardcoded rules.

This example demonstrates:
1. Creating user preference profiles
2. Temporal patterns for purchase history
3. Similarity search for finding relevant products
4. Collaborative filtering through user similarity

Use Cases:
- E-commerce product recommendations
- Content personalization
- Cross-sell and upsell suggestions
- "Customers also bought" features
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define User Preference Profiles
# =============================================================================

def create_user_profile(
    user_id: str,
    # Preferences
    preferred_categories: list,
    preferred_brands: list,
    price_sensitivity: str,  # "budget", "mid-range", "premium"
    # Behavioral signals
    avg_order_value: float,
    purchase_frequency: str,  # "rare", "occasional", "frequent"
    # Demographics (optional)
    age_group: str = None,
    location: str = None,
):
    """Create a user preference profile."""
    return Concept(
        name=f"user_{user_id}",
        attributes={
            "user_id": user_id,
            "preferred_categories": preferred_categories,
            "preferred_brands": preferred_brands,
            "price_sensitivity": price_sensitivity,
            "avg_order_value": avg_order_value,
            "purchase_frequency": purchase_frequency,
            "age_group": age_group,
            "location": location,
            # For cortex similarity
            "layer": price_sensitivity,
            "role": purchase_frequency,
        }
    )

# =============================================================================
# Define Products
# =============================================================================

def create_product(
    product_id: str,
    name: str,
    category: str,
    brand: str,
    price: float,
    tags: list,
    rating: float = 0,
    purchase_count: int = 0,
):
    """Create a product concept."""
    return Concept(
        name=f"product_{product_id}",
        attributes={
            "product_id": product_id,
            "name": name,
            "category": category,
            "brand": brand,
            "price": price,
            "tags": tags,
            "rating": rating,
            "purchase_count": purchase_count,
            "layer": category,
        }
    )

# =============================================================================
# Define Purchase Events
# =============================================================================

def create_purchase(
    user_id: str,
    product_id: str,
    timestamp: str,
    quantity: int = 1,
    rating_given: float = None,
):
    """Create a purchase event concept."""
    return Concept(
        name=f"purchase_{user_id}_{product_id}_{timestamp}",
        attributes={
            "user_id": user_id,
            "product_id": product_id,
            "timestamp": timestamp,
            "quantity": quantity,
            "rating_given": rating_given,
        }
    )

# =============================================================================
# Create Sample Data
# =============================================================================

print("Creating user profiles...")

users = [
    create_user_profile(
        "U001",
        preferred_categories=["Electronics", "Gaming"],
        preferred_brands=["TechPro", "GameMax"],
        price_sensitivity="mid-range",
        avg_order_value=150,
        purchase_frequency="frequent",
        age_group="25-34"
    ),
    create_user_profile(
        "U002",
        preferred_categories=["Fashion", "Beauty"],
        preferred_brands=["StyleCo", "GlamBrand"],
        price_sensitivity="premium",
        avg_order_value=250,
        purchase_frequency="frequent",
        age_group="25-34"
    ),
    create_user_profile(
        "U003",
        preferred_categories=["Home", "Kitchen"],
        preferred_brands=["HomePlus", "ChefPro"],
        price_sensitivity="budget",
        avg_order_value=75,
        purchase_frequency="occasional",
        age_group="35-44"
    ),
    create_user_profile(
        "U004",
        preferred_categories=["Electronics", "Home"],
        preferred_brands=["TechPro", "SmartHome"],
        price_sensitivity="premium",
        avg_order_value=300,
        purchase_frequency="occasional",
        age_group="35-44"
    ),
]

for user in users:
    glyph = model.encode(user)
    print(f"  ✓ {user.attributes['user_id']}: {user.attributes['preferred_categories']}")

print("\nCreating products...")

products = [
    # Electronics
    create_product("P001", "Wireless Gaming Headset", "Electronics", "GameMax", 129.99,
                   ["gaming", "wireless", "headset"], rating=4.7, purchase_count=1500),
    create_product("P002", "4K Gaming Monitor", "Electronics", "TechPro", 399.99,
                   ["gaming", "monitor", "4k"], rating=4.8, purchase_count=800),
    create_product("P003", "Mechanical Keyboard", "Electronics", "GameMax", 89.99,
                   ["gaming", "keyboard", "mechanical"], rating=4.6, purchase_count=2000),
    create_product("P004", "Smart Speaker", "Electronics", "TechPro", 79.99,
                   ["smart-home", "speaker", "voice"], rating=4.5, purchase_count=3000),
    # Fashion
    create_product("P005", "Designer Handbag", "Fashion", "StyleCo", 299.99,
                   ["luxury", "handbag", "designer"], rating=4.9, purchase_count=500),
    create_product("P006", "Premium Sunglasses", "Fashion", "GlamBrand", 199.99,
                   ["sunglasses", "premium", "fashion"], rating=4.7, purchase_count=750),
    create_product("P007", "Silk Scarf", "Fashion", "StyleCo", 89.99,
                   ["scarf", "silk", "accessory"], rating=4.6, purchase_count=600),
    # Home
    create_product("P008", "Robot Vacuum", "Home", "SmartHome", 349.99,
                   ["vacuum", "robot", "smart-home"], rating=4.6, purchase_count=1200),
    create_product("P009", "Air Purifier", "Home", "HomePlus", 149.99,
                   ["air-purifier", "health", "home"], rating=4.5, purchase_count=900),
    create_product("P010", "Coffee Maker", "Kitchen", "ChefPro", 79.99,
                   ["coffee", "kitchen", "appliance"], rating=4.4, purchase_count=2500),
]

for product in products:
    glyph = model.encode(product)
    print(f"  ✓ {product.attributes['product_id']}: {product.attributes['name']}")

print("\nCreating purchase history...")

purchases = [
    # User 1 purchases (Electronics/Gaming)
    create_purchase("U001", "P001", "2025-01-15", rating_given=5),
    create_purchase("U001", "P003", "2025-01-20", rating_given=4),
    # User 2 purchases (Fashion)
    create_purchase("U002", "P005", "2025-01-10", rating_given=5),
    create_purchase("U002", "P006", "2025-01-18", rating_given=5),
    # User 3 purchases (Home/Kitchen)
    create_purchase("U003", "P009", "2025-01-12", rating_given=4),
    create_purchase("U003", "P010", "2025-01-22", rating_given=4),
    # User 4 purchases (Electronics/Home)
    create_purchase("U004", "P004", "2025-01-08", rating_given=5),
    create_purchase("U004", "P008", "2025-01-25", rating_given=4),
]

for purchase in purchases:
    glyph = model.encode(purchase)
    print(f"  ✓ {purchase.attributes['user_id']} → {purchase.attributes['product_id']}")

# =============================================================================
# Create Temporal Edges for Purchase Sequences
# =============================================================================

print("\nCreating temporal edges...")

temporal_encoder = TemporalEncoder(config)

# Group purchases by user and create sequences
user_purchases = {}
for purchase in purchases:
    uid = purchase.attributes["user_id"]
    if uid not in user_purchases:
        user_purchases[uid] = []
    user_purchases[uid].append(purchase)

for uid, user_purch in user_purchases.items():
    # Sort by timestamp
    user_purch.sort(key=lambda x: x.attributes["timestamp"])
    
    for i in range(len(user_purch) - 1):
        edge = temporal_encoder.create_edge(
            from_concept=user_purch[i],
            to_concept=user_purch[i + 1],
            edge_type="purchase_sequence"
        )
        print(f"  ✓ {uid}: {user_purch[i].attributes['product_id']} → {user_purch[i+1].attributes['product_id']}")

# =============================================================================
# Recommendation Functions
# =============================================================================

def get_recommendations_for_user(user_id: str, top_k: int = 5):
    """
    Get personalized recommendations for a user based on their profile
    and purchase history.
    """
    print(f"\n{'='*60}")
    print(f"RECOMMENDATIONS FOR: {user_id}")
    print('='*60)
    
    # Find user profile
    user_results = model.similarity_search(user_id, top_k=1)
    
    if not user_results:
        print("User not found")
        return []
    
    user = user_results[0]
    user_attrs = user.attributes
    
    print(f"\nUser Profile:")
    print(f"  Categories: {user_attrs.get('preferred_categories', [])}")
    print(f"  Brands: {user_attrs.get('preferred_brands', [])}")
    print(f"  Price Sensitivity: {user_attrs.get('price_sensitivity')}")
    
    # Find products similar to user preferences
    results = model.similarity_search(user, top_k=top_k + 5)
    
    # Filter to products only and exclude already purchased
    purchased_products = set()
    for purchase in purchases:
        if purchase.attributes["user_id"] == user_id:
            purchased_products.add(purchase.attributes["product_id"])
    
    recommendations = []
    for result in results:
        if "product_id" in result.attributes:
            pid = result.attributes["product_id"]
            if pid not in purchased_products:
                recommendations.append({
                    "product_id": pid,
                    "name": result.attributes["name"],
                    "category": result.attributes["category"],
                    "price": result.attributes["price"],
                    "relevance": result.score,
                    "reason": "Matches your preferences"
                })
    
    print(f"\nRecommended Products:")
    for i, rec in enumerate(recommendations[:top_k], 1):
        print(f"\n  {i}. {rec['name']}")
        print(f"     ${rec['price']:.2f} | {rec['category']}")
        print(f"     Relevance: {rec['relevance']:.2f}")
        print(f"     Reason: {rec['reason']}")
    
    return recommendations[:top_k]


def get_similar_products(product_id: str, top_k: int = 3):
    """
    Get products similar to a given product ("You might also like").
    """
    print(f"\n{'='*60}")
    print(f"SIMILAR TO: {product_id}")
    print('='*60)
    
    # Find the product
    product_results = model.similarity_search(product_id, top_k=1)
    
    if not product_results:
        return []
    
    product = product_results[0]
    
    # Find similar products
    results = model.similarity_search(product, top_k=top_k + 1)
    
    similar = []
    for result in results:
        if "product_id" in result.attributes and result.attributes["product_id"] != product_id:
            similar.append({
                "product_id": result.attributes["product_id"],
                "name": result.attributes["name"],
                "price": result.attributes["price"],
                "similarity": result.score
            })
    
    print(f"\nProduct: {product.attributes['name']}")
    print(f"\nSimilar Products:")
    for s in similar[:top_k]:
        print(f"  • {s['name']} (${s['price']:.2f}) - {s['similarity']:.2f}")
    
    return similar[:top_k]


def get_frequently_bought_together(product_id: str):
    """
    Find products frequently purchased together.
    """
    print(f"\n{'='*60}")
    print(f"FREQUENTLY BOUGHT WITH: {product_id}")
    print('='*60)
    
    # Find users who bought this product
    buyers = set()
    for purchase in purchases:
        if purchase.attributes["product_id"] == product_id:
            buyers.add(purchase.attributes["user_id"])
    
    # Find other products these users bought
    co_purchased = {}
    for purchase in purchases:
        if purchase.attributes["user_id"] in buyers:
            pid = purchase.attributes["product_id"]
            if pid != product_id:
                co_purchased[pid] = co_purchased.get(pid, 0) + 1
    
    # Sort by frequency
    sorted_products = sorted(co_purchased.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nCustomers also bought:")
    for pid, count in sorted_products[:3]:
        # Get product details
        for product in products:
            if product.attributes["product_id"] == pid:
                print(f"  • {product.attributes['name']} ({count} co-purchases)")
                break
    
    return sorted_products[:3]


def find_similar_users(user_id: str, top_k: int = 3):
    """
    Find users with similar preferences for collaborative filtering.
    """
    print(f"\n{'='*60}")
    print(f"SIMILAR USERS TO: {user_id}")
    print('='*60)
    
    # Find user
    user_results = model.similarity_search(user_id, top_k=1)
    
    if not user_results:
        return []
    
    user = user_results[0]
    
    # Find similar users
    results = model.similarity_search(user, top_k=top_k + 1)
    
    similar = []
    for result in results:
        if "user_id" in result.attributes and result.attributes["user_id"] != user_id:
            similar.append({
                "user_id": result.attributes["user_id"],
                "similarity": result.score,
                "categories": result.attributes.get("preferred_categories", [])
            })
    
    print(f"\nSimilar Users:")
    for s in similar[:top_k]:
        print(f"  • {s['user_id']}: {s['similarity']:.2f}")
        print(f"    Categories: {s['categories']}")
    
    return similar[:top_k]

# =============================================================================
# Test Recommendations
# =============================================================================

print("\n" + "="*60)
print("TESTING RECOMMENDATION ENGINE")
print("="*60)

# Get recommendations for each user
for user in users:
    get_recommendations_for_user(user.attributes["user_id"])

# Similar products
get_similar_products("P001")

# Frequently bought together
get_frequently_bought_together("P001")

# Similar users
find_similar_users("U001")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("recommendation-engine.glyphh")
print("✓ Model exported to recommendation-engine.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @recommendation-engine.glyphh")

print("\nGet recommendations via API:")
print('  curl -X POST http://localhost:8000/api/v1/recommendation-engine/recommend \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"user_id": "U001", "top_k": 5}\'')

print("\n" + "="*60)
print("KEY CAPABILITIES")
print("="*60)
print("""
1. PERSONALIZED RECOMMENDATIONS
   - Based on user preferences and history
   - Similarity-driven, not rule-based
   
2. COLLABORATIVE FILTERING
   - Find similar users
   - Recommend what similar users liked
   
3. PRODUCT SIMILARITY
   - "You might also like" suggestions
   - Based on product attributes
   
4. PURCHASE PATTERNS
   - Frequently bought together
   - Temporal purchase sequences
""")
