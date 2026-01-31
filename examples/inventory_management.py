"""
Inventory Management Example

Track inventory levels, predict stockouts, and optimize reorder points
using temporal patterns and fact trees for supply chain visibility.

Key Principle: Use temporal patterns to predict inventory needs
before stockouts occur, not just react to low stock.

This example demonstrates:
1. Creating inventory item concepts with stock levels
2. Temporal edges for tracking stock changes over time
3. Fact trees for warehouse/location hierarchy
4. Predictive reordering based on consumption patterns

Use Cases:
- Warehouse inventory tracking
- Stockout prediction
- Reorder point optimization
- Multi-location inventory visibility
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import TemporalEncoder

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Inventory Item Concepts
# =============================================================================

def create_inventory_item(
    sku: str,
    name: str,
    # Classification
    category: str,
    subcategory: str,
    # Stock levels
    quantity_on_hand: int,
    quantity_reserved: int,
    quantity_available: int,
    # Thresholds
    reorder_point: int,
    safety_stock: int,
    max_stock: int,
    # Location
    warehouse: str,
    zone: str,
    bin_location: str,
    # Metrics
    avg_daily_demand: float,
    lead_time_days: int,
    unit_cost: float,
):
    """Create an inventory item concept."""
    return Concept(
        name=f"inv_{sku}_{warehouse}",
        attributes={
            "sku": sku,
            "name": name,
            "category": category,
            "subcategory": subcategory,
            "quantity_on_hand": quantity_on_hand,
            "quantity_reserved": quantity_reserved,
            "quantity_available": quantity_available,
            "reorder_point": reorder_point,
            "safety_stock": safety_stock,
            "max_stock": max_stock,
            "warehouse": warehouse,
            "zone": zone,
            "bin_location": bin_location,
            "avg_daily_demand": avg_daily_demand,
            "lead_time_days": lead_time_days,
            "unit_cost": unit_cost,
            # Computed
            "days_of_stock": quantity_available / avg_daily_demand if avg_daily_demand > 0 else 999,
            "stock_status": "critical" if quantity_available <= safety_stock else "low" if quantity_available <= reorder_point else "healthy",
            # For cortex similarity
            "layer": category,
            "role": warehouse,
        }
    )

# =============================================================================
# Define Stock Movement Events
# =============================================================================

def create_stock_movement(
    sku: str,
    warehouse: str,
    timestamp: str,
    movement_type: str,  # "receipt", "sale", "transfer", "adjustment"
    quantity: int,
    quantity_after: int,
    reference: str = None,
):
    """Create a stock movement event."""
    return Concept(
        name=f"move_{sku}_{warehouse}_{timestamp}",
        attributes={
            "sku": sku,
            "warehouse": warehouse,
            "timestamp": timestamp,
            "movement_type": movement_type,
            "quantity": quantity,
            "quantity_after": quantity_after,
            "reference": reference,
        }
    )

# =============================================================================
# Define Warehouse Hierarchy
# =============================================================================

warehouses = [
    Concept(
        name="warehouse_east",
        attributes={
            "warehouse_id": "WH-EAST",
            "name": "East Coast Distribution Center",
            "location": "New Jersey",
            "region": "East",
            "capacity_units": 50000,
            "zones": ["A", "B", "C", "D"],
            "type": "distribution"
        }
    ),
    Concept(
        name="warehouse_west",
        attributes={
            "warehouse_id": "WH-WEST",
            "name": "West Coast Distribution Center",
            "location": "California",
            "region": "West",
            "capacity_units": 40000,
            "zones": ["A", "B", "C"],
            "type": "distribution"
        }
    ),
    Concept(
        name="warehouse_central",
        attributes={
            "warehouse_id": "WH-CENTRAL",
            "name": "Central Fulfillment Center",
            "location": "Texas",
            "region": "Central",
            "capacity_units": 60000,
            "zones": ["A", "B", "C", "D", "E"],
            "type": "fulfillment"
        }
    ),
]

print("Encoding warehouses...")
for wh in warehouses:
    glyph = model.encode(wh)
    print(f"  ✓ {wh.attributes['warehouse_id']}: {wh.attributes['name']}")

# =============================================================================
# Create Inventory Data
# =============================================================================

print("\nCreating inventory items...")

inventory_items = [
    # East warehouse
    create_inventory_item(
        "SKU-001", "Widget A", "Components", "Widgets",
        quantity_on_hand=500, quantity_reserved=50, quantity_available=450,
        reorder_point=200, safety_stock=100, max_stock=1000,
        warehouse="WH-EAST", zone="A", bin_location="A-01-01",
        avg_daily_demand=25, lead_time_days=7, unit_cost=5.00
    ),
    create_inventory_item(
        "SKU-002", "Gadget B", "Components", "Gadgets",
        quantity_on_hand=150, quantity_reserved=30, quantity_available=120,
        reorder_point=150, safety_stock=75, max_stock=500,
        warehouse="WH-EAST", zone="B", bin_location="B-02-03",
        avg_daily_demand=15, lead_time_days=10, unit_cost=12.00
    ),
    create_inventory_item(
        "SKU-003", "Assembly C", "Finished Goods", "Assemblies",
        quantity_on_hand=80, quantity_reserved=20, quantity_available=60,
        reorder_point=100, safety_stock=50, max_stock=300,
        warehouse="WH-EAST", zone="C", bin_location="C-01-02",
        avg_daily_demand=8, lead_time_days=14, unit_cost=45.00
    ),
    # West warehouse
    create_inventory_item(
        "SKU-001", "Widget A", "Components", "Widgets",
        quantity_on_hand=300, quantity_reserved=25, quantity_available=275,
        reorder_point=200, safety_stock=100, max_stock=800,
        warehouse="WH-WEST", zone="A", bin_location="A-02-01",
        avg_daily_demand=20, lead_time_days=7, unit_cost=5.00
    ),
    create_inventory_item(
        "SKU-004", "Part D", "Raw Materials", "Parts",
        quantity_on_hand=50, quantity_reserved=10, quantity_available=40,
        reorder_point=100, safety_stock=50, max_stock=400,
        warehouse="WH-WEST", zone="B", bin_location="B-01-01",
        avg_daily_demand=12, lead_time_days=5, unit_cost=3.00
    ),
    # Central warehouse
    create_inventory_item(
        "SKU-001", "Widget A", "Components", "Widgets",
        quantity_on_hand=800, quantity_reserved=100, quantity_available=700,
        reorder_point=300, safety_stock=150, max_stock=1500,
        warehouse="WH-CENTRAL", zone="A", bin_location="A-01-01",
        avg_daily_demand=40, lead_time_days=7, unit_cost=5.00
    ),
]

for item in inventory_items:
    glyph = model.encode(item)
    status = item.attributes["stock_status"]
    status_icon = "🔴" if status == "critical" else "🟡" if status == "low" else "🟢"
    print(f"  {status_icon} {item.attributes['sku']} @ {item.attributes['warehouse']}: {item.attributes['quantity_available']} units")

# =============================================================================
# Create Stock Movement History
# =============================================================================

print("\nCreating stock movements...")

movements = [
    # SKU-001 at East - declining stock
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-25", "sale", -30, 530, "ORD-1001"),
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-26", "sale", -25, 505, "ORD-1002"),
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-27", "sale", -28, 477, "ORD-1003"),
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-28", "receipt", 100, 577, "PO-2001"),
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-29", "sale", -35, 542, "ORD-1004"),
    create_stock_movement("SKU-001", "WH-EAST", "2025-01-30", "sale", -42, 500, "ORD-1005"),
    # SKU-004 at West - critical stock
    create_stock_movement("SKU-004", "WH-WEST", "2025-01-28", "sale", -15, 65, "ORD-2001"),
    create_stock_movement("SKU-004", "WH-WEST", "2025-01-29", "sale", -10, 55, "ORD-2002"),
    create_stock_movement("SKU-004", "WH-WEST", "2025-01-30", "sale", -5, 50, "ORD-2003"),
]

for move in movements:
    glyph = model.encode(move)
    direction = "↓" if move.attributes["quantity"] < 0 else "↑"
    print(f"  {direction} {move.attributes['sku']} @ {move.attributes['warehouse']}: {move.attributes['quantity']} → {move.attributes['quantity_after']}")

# =============================================================================
# Create Temporal Edges
# =============================================================================

print("\nCreating temporal edges...")

temporal_encoder = TemporalEncoder(config)

# Group movements by SKU/warehouse
movement_groups = {}
for move in movements:
    key = f"{move.attributes['sku']}_{move.attributes['warehouse']}"
    if key not in movement_groups:
        movement_groups[key] = []
    movement_groups[key].append(move)

for key, group in movement_groups.items():
    group.sort(key=lambda x: x.attributes["timestamp"])
    for i in range(len(group) - 1):
        edge = temporal_encoder.create_edge(
            from_concept=group[i],
            to_concept=group[i + 1],
            edge_type="stock_transition"
        )
    print(f"  ✓ {key}: {len(group)} movements linked")

# =============================================================================
# Inventory Analysis Functions
# =============================================================================

def check_stock_status(sku: str = None, warehouse: str = None):
    """
    Check stock status across locations.
    """
    print(f"\n{'='*60}")
    print(f"STOCK STATUS CHECK")
    if sku:
        print(f"SKU: {sku}")
    if warehouse:
        print(f"Warehouse: {warehouse}")
    print('='*60)
    
    results = []
    for item in inventory_items:
        attrs = item.attributes
        
        # Apply filters
        if sku and attrs["sku"] != sku:
            continue
        if warehouse and attrs["warehouse"] != warehouse:
            continue
        
        results.append({
            "sku": attrs["sku"],
            "name": attrs["name"],
            "warehouse": attrs["warehouse"],
            "available": attrs["quantity_available"],
            "status": attrs["stock_status"],
            "days_of_stock": attrs["days_of_stock"],
            "reorder_point": attrs["reorder_point"]
        })
    
    print(f"\nItems Found: {len(results)}")
    for r in results:
        status_icon = "🔴" if r["status"] == "critical" else "🟡" if r["status"] == "low" else "🟢"
        print(f"\n  {status_icon} {r['sku']} - {r['name']}")
        print(f"     Location: {r['warehouse']}")
        print(f"     Available: {r['available']} units")
        print(f"     Days of Stock: {r['days_of_stock']:.1f}")
        print(f"     Status: {r['status'].upper()}")
    
    return results


def predict_stockout(sku: str, warehouse: str):
    """
    Predict when stockout will occur based on consumption patterns.
    """
    print(f"\n{'='*60}")
    print(f"STOCKOUT PREDICTION: {sku} @ {warehouse}")
    print('='*60)
    
    # Find the inventory item
    item = None
    for inv in inventory_items:
        if inv.attributes["sku"] == sku and inv.attributes["warehouse"] == warehouse:
            item = inv
            break
    
    if not item:
        print("Item not found")
        return None
    
    attrs = item.attributes
    
    # Calculate days until stockout
    days_until_stockout = attrs["quantity_available"] / attrs["avg_daily_demand"]
    days_until_reorder = (attrs["quantity_available"] - attrs["reorder_point"]) / attrs["avg_daily_demand"]
    
    print(f"\nCurrent Stock: {attrs['quantity_available']} units")
    print(f"Avg Daily Demand: {attrs['avg_daily_demand']} units")
    print(f"Lead Time: {attrs['lead_time_days']} days")
    print(f"\nPredictions:")
    print(f"  Days until stockout: {days_until_stockout:.1f}")
    print(f"  Days until reorder point: {max(0, days_until_reorder):.1f}")
    
    # Recommendation
    if days_until_reorder <= 0:
        print(f"\n⚠️  REORDER NOW - Below reorder point!")
        reorder_qty = attrs["max_stock"] - attrs["quantity_on_hand"]
        print(f"  Recommended order quantity: {reorder_qty} units")
    elif days_until_reorder <= attrs["lead_time_days"]:
        print(f"\n⚡ REORDER SOON - Will hit reorder point before lead time")
    else:
        print(f"\n✓ Stock healthy - {days_until_reorder:.0f} days until reorder needed")
    
    return {
        "days_until_stockout": days_until_stockout,
        "days_until_reorder": days_until_reorder,
        "needs_reorder": days_until_reorder <= attrs["lead_time_days"]
    }


def get_reorder_recommendations():
    """
    Get list of items that need to be reordered.
    """
    print(f"\n{'='*60}")
    print(f"REORDER RECOMMENDATIONS")
    print('='*60)
    
    recommendations = []
    
    for item in inventory_items:
        attrs = item.attributes
        days_until_reorder = (attrs["quantity_available"] - attrs["reorder_point"]) / attrs["avg_daily_demand"]
        
        if days_until_reorder <= attrs["lead_time_days"]:
            reorder_qty = attrs["max_stock"] - attrs["quantity_on_hand"]
            recommendations.append({
                "sku": attrs["sku"],
                "name": attrs["name"],
                "warehouse": attrs["warehouse"],
                "current_stock": attrs["quantity_available"],
                "reorder_qty": reorder_qty,
                "urgency": "critical" if attrs["stock_status"] == "critical" else "high" if days_until_reorder <= 0 else "medium",
                "estimated_cost": reorder_qty * attrs["unit_cost"]
            })
    
    # Sort by urgency
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    recommendations.sort(key=lambda x: urgency_order.get(x["urgency"], 3))
    
    print(f"\nItems Needing Reorder: {len(recommendations)}")
    
    total_cost = 0
    for rec in recommendations:
        urgency_icon = "🔴" if rec["urgency"] == "critical" else "🟡" if rec["urgency"] == "high" else "🟢"
        print(f"\n  {urgency_icon} {rec['sku']} - {rec['name']}")
        print(f"     Warehouse: {rec['warehouse']}")
        print(f"     Current: {rec['current_stock']} → Order: {rec['reorder_qty']}")
        print(f"     Est. Cost: ${rec['estimated_cost']:.2f}")
        total_cost += rec["estimated_cost"]
    
    print(f"\n{'='*60}")
    print(f"Total Estimated Reorder Cost: ${total_cost:.2f}")
    
    return recommendations


def get_inventory_by_warehouse(warehouse: str):
    """
    Get inventory summary for a specific warehouse.
    """
    print(f"\n{'='*60}")
    print(f"WAREHOUSE INVENTORY: {warehouse}")
    print('='*60)
    
    # Find warehouse details
    wh_details = None
    for wh in warehouses:
        if wh.attributes["warehouse_id"] == warehouse:
            wh_details = wh.attributes
            break
    
    if wh_details:
        print(f"\n{wh_details['name']}")
        print(f"Location: {wh_details['location']}")
        print(f"Type: {wh_details['type']}")
    
    # Get items in this warehouse
    items = [i for i in inventory_items if i.attributes["warehouse"] == warehouse]
    
    total_units = sum(i.attributes["quantity_on_hand"] for i in items)
    total_value = sum(i.attributes["quantity_on_hand"] * i.attributes["unit_cost"] for i in items)
    
    print(f"\nSummary:")
    print(f"  Total SKUs: {len(items)}")
    print(f"  Total Units: {total_units}")
    print(f"  Total Value: ${total_value:.2f}")
    
    # Status breakdown
    critical = len([i for i in items if i.attributes["stock_status"] == "critical"])
    low = len([i for i in items if i.attributes["stock_status"] == "low"])
    healthy = len([i for i in items if i.attributes["stock_status"] == "healthy"])
    
    print(f"\nStock Status:")
    print(f"  🔴 Critical: {critical}")
    print(f"  🟡 Low: {low}")
    print(f"  🟢 Healthy: {healthy}")
    
    return items

# =============================================================================
# Test Inventory Management
# =============================================================================

print("\n" + "="*60)
print("TESTING INVENTORY MANAGEMENT")
print("="*60)

# Check overall stock status
check_stock_status()

# Check specific SKU across warehouses
check_stock_status(sku="SKU-001")

# Predict stockout
predict_stockout("SKU-004", "WH-WEST")

# Get reorder recommendations
get_reorder_recommendations()

# Warehouse summary
get_inventory_by_warehouse("WH-EAST")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("inventory-management.glyphh")
print("✓ Model exported to inventory-management.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @inventory-management.glyphh")

print("\nCheck stock via API:")
print('  curl -X POST http://localhost:8000/api/v1/inventory-management/check \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"sku": "SKU-001", "warehouse": "WH-EAST"}\'')

print("\n" + "="*60)
print("KEY CAPABILITIES")
print("="*60)
print("""
1. MULTI-LOCATION VISIBILITY
   - Track stock across warehouses
   - Aggregate or drill-down views
   
2. PREDICTIVE REORDERING
   - Forecast stockouts before they happen
   - Lead time-aware recommendations
   
3. TEMPORAL TRACKING
   - Stock movement history
   - Consumption pattern analysis
   
4. AUTOMATED ALERTS
   - Critical/low stock identification
   - Prioritized reorder lists
""")
