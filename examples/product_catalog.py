"""
Product Catalog Search Example

Enable natural language product search with accurate specifications
and availability using similarity search and intent patterns.

Key Principle: Understand what customers mean, not just what they say.
Match intent to products even with imprecise queries.

This example demonstrates:
1. Creating product concepts with rich attributes
2. Intent patterns for natural language queries
3. Similarity search for finding matching products
4. Faceted filtering with attribute matching

Use Cases:
- E-commerce product search
- Inventory lookup systems
- Customer service product queries
- Catalog management
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import IntentEncoder, IntentPattern

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Product Concepts
# =============================================================================

def create_product(
    sku: str,
    name: str,
    # Classification
    category: str,
    subcategory: str,
    brand: str,
    # Attributes
    color: str = None,
    size: str = None,
    material: str = None,
    # Specifications
    price: float = 0,
    weight_kg: float = None,
    dimensions: str = None,
    # Inventory
    in_stock: bool = True,
    stock_quantity: int = 0,
    # Metadata
    description: str = "",
    tags: list = None,
    rating: float = 0,
    review_count: int = 0,
):
    """Create a product concept for catalog search."""
    return Concept(
        name=f"product_{sku}",
        attributes={
            "sku": sku,
            "name": name,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "color": color,
            "size": size,
            "material": material,
            "price": price,
            "weight_kg": weight_kg,
            "dimensions": dimensions,
            "in_stock": in_stock,
            "stock_quantity": stock_quantity,
            "description": description,
            "tags": tags or [],
            "rating": rating,
            "review_count": review_count,
            # For cortex similarity
            "layer": category,
            "role": subcategory,
        }
    )

# =============================================================================
# Create Product Catalog
# =============================================================================

print("Creating product catalog...")

products = [
    # Electronics
    create_product(
        "ELEC-001", "Pro Wireless Headphones",
        category="Electronics", subcategory="Audio", brand="SoundMax",
        color="Black", material="Plastic/Metal",
        price=199.99, weight_kg=0.25,
        in_stock=True, stock_quantity=150,
        description="Premium wireless headphones with noise cancellation",
        tags=["wireless", "noise-cancelling", "bluetooth", "premium"],
        rating=4.7, review_count=1250
    ),
    create_product(
        "ELEC-002", "Compact Bluetooth Speaker",
        category="Electronics", subcategory="Audio", brand="SoundMax",
        color="Blue", material="Fabric/Plastic",
        price=79.99, weight_kg=0.5,
        in_stock=True, stock_quantity=300,
        description="Portable waterproof bluetooth speaker",
        tags=["portable", "waterproof", "bluetooth", "outdoor"],
        rating=4.5, review_count=890
    ),
    create_product(
        "ELEC-003", "4K Smart TV 55 inch",
        category="Electronics", subcategory="TV", brand="ViewTech",
        color="Black", size="55 inch",
        price=699.99, weight_kg=15.5, dimensions="123x71x8 cm",
        in_stock=True, stock_quantity=45,
        description="55 inch 4K UHD Smart TV with streaming apps",
        tags=["4k", "smart-tv", "streaming", "large-screen"],
        rating=4.6, review_count=567
    ),
    # Clothing
    create_product(
        "CLTH-001", "Classic Cotton T-Shirt",
        category="Clothing", subcategory="Tops", brand="BasicWear",
        color="White", size="M", material="100% Cotton",
        price=24.99, weight_kg=0.2,
        in_stock=True, stock_quantity=500,
        description="Comfortable everyday cotton t-shirt",
        tags=["casual", "cotton", "basic", "everyday"],
        rating=4.3, review_count=2100
    ),
    create_product(
        "CLTH-002", "Slim Fit Jeans",
        category="Clothing", subcategory="Bottoms", brand="DenimCo",
        color="Dark Blue", size="32x32", material="98% Cotton, 2% Elastane",
        price=59.99, weight_kg=0.6,
        in_stock=True, stock_quantity=200,
        description="Classic slim fit jeans with stretch",
        tags=["jeans", "slim-fit", "stretch", "casual"],
        rating=4.4, review_count=1560
    ),
    create_product(
        "CLTH-003", "Winter Parka Jacket",
        category="Clothing", subcategory="Outerwear", brand="NorthStyle",
        color="Navy", size="L", material="Polyester/Down",
        price=189.99, weight_kg=1.2,
        in_stock=True, stock_quantity=75,
        description="Warm winter parka with hood and down insulation",
        tags=["winter", "warm", "parka", "hooded", "down"],
        rating=4.8, review_count=430
    ),
    # Home & Kitchen
    create_product(
        "HOME-001", "Stainless Steel Cookware Set",
        category="Home", subcategory="Kitchen", brand="ChefPro",
        color="Silver", material="Stainless Steel",
        price=149.99, weight_kg=8.5,
        in_stock=True, stock_quantity=60,
        description="10-piece stainless steel cookware set",
        tags=["cookware", "stainless-steel", "kitchen", "cooking"],
        rating=4.6, review_count=780
    ),
    create_product(
        "HOME-002", "Robot Vacuum Cleaner",
        category="Home", subcategory="Appliances", brand="CleanBot",
        color="White", material="Plastic",
        price=299.99, weight_kg=3.2,
        in_stock=False, stock_quantity=0,
        description="Smart robot vacuum with app control and mapping",
        tags=["vacuum", "robot", "smart-home", "cleaning", "automated"],
        rating=4.4, review_count=1120
    ),
    # Sports
    create_product(
        "SPRT-001", "Running Shoes",
        category="Sports", subcategory="Footwear", brand="SpeedRun",
        color="Red/Black", size="10", material="Mesh/Rubber",
        price=129.99, weight_kg=0.3,
        in_stock=True, stock_quantity=180,
        description="Lightweight running shoes with cushioned sole",
        tags=["running", "athletic", "lightweight", "cushioned"],
        rating=4.7, review_count=2340
    ),
    create_product(
        "SPRT-002", "Yoga Mat Premium",
        category="Sports", subcategory="Fitness", brand="ZenFit",
        color="Purple", size="183x61 cm", material="TPE",
        price=39.99, weight_kg=1.0,
        in_stock=True, stock_quantity=250,
        description="Non-slip premium yoga mat with carrying strap",
        tags=["yoga", "fitness", "non-slip", "exercise"],
        rating=4.5, review_count=890
    ),
]

for product in products:
    glyph = model.encode(product)
    print(f"  ✓ {product.attributes['sku']}: {product.attributes['name']}")

# =============================================================================
# Set up Intent Patterns
# =============================================================================

intent_encoder = IntentEncoder(config)

intent_encoder.add_pattern(IntentPattern(
    intent_type="product_search",
    example_phrases=[
        "looking for",
        "I need",
        "show me",
        "find",
        "search for",
        "do you have",
    ],
    query_template={
        "operation": "similarity_search",
        "entity_type": "product",
        "top_k": 10
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="price_filter",
    example_phrases=[
        "under $",
        "less than",
        "cheaper than",
        "budget",
        "affordable",
        "on sale",
    ],
    query_template={
        "operation": "similarity_search",
        "filter_type": "price",
        "top_k": 10
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="availability_check",
    example_phrases=[
        "in stock",
        "available",
        "can I get",
        "do you have",
        "is there",
    ],
    query_template={
        "operation": "similarity_search",
        "filter": {"in_stock": True},
        "top_k": 10
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="recommendation",
    example_phrases=[
        "recommend",
        "suggest",
        "best",
        "top rated",
        "popular",
        "what should I get",
    ],
    query_template={
        "operation": "similarity_search",
        "sort_by": "rating",
        "top_k": 5
    }
))

model.intent_encoder = intent_encoder

# =============================================================================
# Product Search Functions
# =============================================================================

def search_products(query: str, filters: dict = None, top_k: int = 5):
    """
    Search products using natural language query.
    
    Returns matching products with relevance scores.
    """
    print(f"\n{'='*60}")
    print(f"PRODUCT SEARCH")
    print(f"Query: {query}")
    print('='*60)
    
    # Match intent
    intent_match = model.intent_encoder.match_intent(query)
    print(f"\nIntent: {intent_match.intent_type} ({intent_match.confidence:.2f})")
    
    # Search products
    results = model.similarity_search(query, top_k=top_k)
    
    # Apply filters if provided
    if filters:
        filtered_results = []
        for result in results:
            attrs = result.attributes
            match = True
            
            if "max_price" in filters and attrs.get("price", 0) > filters["max_price"]:
                match = False
            if "category" in filters and attrs.get("category") != filters["category"]:
                match = False
            if "in_stock" in filters and attrs.get("in_stock") != filters["in_stock"]:
                match = False
            
            if match:
                filtered_results.append(result)
        
        results = filtered_results
    
    print(f"\nResults ({len(results)}):")
    for i, result in enumerate(results, 1):
        attrs = result.attributes
        stock_status = "✓ In Stock" if attrs.get("in_stock") else "✗ Out of Stock"
        print(f"\n  {i}. {attrs['name']}")
        print(f"     SKU: {attrs['sku']} | Brand: {attrs['brand']}")
        print(f"     Price: ${attrs['price']:.2f} | {stock_status}")
        print(f"     Rating: {'★' * int(attrs.get('rating', 0))} ({attrs.get('rating', 0)}/5)")
        print(f"     Relevance: {result.score:.2f}")
    
    return results


def get_product_details(sku: str):
    """
    Get detailed information about a specific product.
    """
    results = model.similarity_search(sku, top_k=1)
    
    if not results:
        return None
    
    product = results[0]
    attrs = product.attributes
    
    print(f"\n{'='*60}")
    print(f"PRODUCT DETAILS: {attrs['name']}")
    print('='*60)
    print(f"SKU: {attrs['sku']}")
    print(f"Brand: {attrs['brand']}")
    print(f"Category: {attrs['category']} > {attrs['subcategory']}")
    print(f"\nPrice: ${attrs['price']:.2f}")
    print(f"Rating: {'★' * int(attrs.get('rating', 0))} ({attrs.get('rating', 0)}/5 from {attrs.get('review_count', 0)} reviews)")
    print(f"\nDescription: {attrs['description']}")
    print(f"\nSpecifications:")
    if attrs.get('color'):
        print(f"  • Color: {attrs['color']}")
    if attrs.get('size'):
        print(f"  • Size: {attrs['size']}")
    if attrs.get('material'):
        print(f"  • Material: {attrs['material']}")
    if attrs.get('weight_kg'):
        print(f"  • Weight: {attrs['weight_kg']} kg")
    
    print(f"\nAvailability: {'In Stock ({} units)'.format(attrs.get('stock_quantity', 0)) if attrs.get('in_stock') else 'Out of Stock'}")
    
    return attrs


def find_similar_products(sku: str, top_k: int = 3):
    """
    Find products similar to a given product.
    """
    # Get the product
    results = model.similarity_search(sku, top_k=1)
    
    if not results:
        return []
    
    product = results[0]
    
    # Find similar products
    similar = model.similarity_search(product, top_k=top_k + 1)
    
    # Exclude the original product
    similar = [s for s in similar if s.attributes.get("sku") != sku]
    
    print(f"\n{'='*60}")
    print(f"SIMILAR PRODUCTS TO: {product.attributes['name']}")
    print('='*60)
    
    for s in similar[:top_k]:
        attrs = s.attributes
        print(f"\n  • {attrs['name']}")
        print(f"    ${attrs['price']:.2f} | {attrs['brand']}")
        print(f"    Similarity: {s.score:.2f}")
    
    return similar[:top_k]

# =============================================================================
# Test Product Search
# =============================================================================

print("\n" + "="*60)
print("TESTING PRODUCT SEARCH")
print("="*60)

# Natural language searches
test_queries = [
    "I need wireless headphones",
    "looking for a warm winter jacket",
    "show me running shoes",
    "do you have any smart TVs",
    "recommend a good yoga mat",
]

for query in test_queries:
    search_products(query, top_k=3)

# Filtered search
print("\n" + "="*60)
print("FILTERED SEARCH")
print("="*60)

search_products("headphones", filters={"max_price": 100, "in_stock": True})

# Product details
print("\n" + "="*60)
print("PRODUCT DETAILS")
print("="*60)

get_product_details("ELEC-001")

# Similar products
find_similar_products("ELEC-001")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("product-catalog.glyphh")
print("✓ Model exported to product-catalog.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @product-catalog.glyphh")

print("\nSearch products via API:")
print('  curl -X POST http://localhost:8000/api/v1/product-catalog/search \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"query": "wireless headphones", "filters": {"max_price": 200}}\'')
