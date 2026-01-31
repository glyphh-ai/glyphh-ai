"""
Medical Protocols Example

Provide accurate medical protocol information with proper citations,
disclaimers, and evidence levels using fact trees and similarity search.

Key Principle: Every medical recommendation must be traceable to
an authoritative source with clear evidence levels.

This example demonstrates:
1. Creating medical protocol concepts with citations
2. Fact trees for protocol hierarchies and relationships
3. Similarity search for finding relevant protocols
4. Evidence-based recommendations with disclaimers

Use Cases:
- Clinical decision support
- Medical reference systems
- Protocol compliance checking
- Healthcare staff training

DISCLAIMER: This is a demonstration model only. Not for actual medical use.
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Medical Protocol Concepts
# =============================================================================

def create_protocol(
    protocol_id: str,
    name: str,
    # Classification
    category: str,  # "treatment", "diagnostic", "preventive", "emergency"
    specialty: str,
    condition: str,
    # Content
    description: str,
    steps: list,
    contraindications: list = None,
    # Evidence
    evidence_level: str,  # "A", "B", "C", "D" (A=highest)
    source: str,
    last_reviewed: str,
    # Metadata
    keywords: list = None,
):
    """Create a medical protocol concept."""
    return Concept(
        name=f"protocol_{protocol_id}",
        attributes={
            "protocol_id": protocol_id,
            "name": name,
            "category": category,
            "specialty": specialty,
            "condition": condition,
            "description": description,
            "steps": steps,
            "contraindications": contraindications or [],
            "evidence_level": evidence_level,
            "source": source,
            "last_reviewed": last_reviewed,
            "keywords": keywords or [],
            # For cortex similarity
            "layer": specialty,
            "role": category,
        }
    )

# =============================================================================
# Create Medical Protocols
# =============================================================================

print("Creating medical protocols...")

protocols = [
    # Emergency protocols
    create_protocol(
        "EM-001", "Basic Life Support (BLS)",
        category="emergency", specialty="Emergency Medicine", condition="Cardiac Arrest",
        description="Standard protocol for basic life support in cardiac arrest situations",
        steps=[
            "1. Ensure scene safety",
            "2. Check responsiveness",
            "3. Call for help / activate EMS",
            "4. Check pulse (10 seconds max)",
            "5. Begin chest compressions (100-120/min, 2 inches depth)",
            "6. Open airway (head-tilt chin-lift)",
            "7. Give rescue breaths (30:2 ratio)",
            "8. Continue until AED arrives or EMS takes over"
        ],
        contraindications=["DNR order in place", "Obvious signs of death"],
        evidence_level="A",
        source="American Heart Association Guidelines 2025",
        last_reviewed="2025-01-15",
        keywords=["CPR", "cardiac arrest", "resuscitation", "emergency"]
    ),
    create_protocol(
        "EM-002", "Anaphylaxis Management",
        category="emergency", specialty="Emergency Medicine", condition="Anaphylaxis",
        description="Emergency protocol for severe allergic reactions",
        steps=[
            "1. Remove allergen if possible",
            "2. Administer epinephrine IM (0.3-0.5mg adult, anterolateral thigh)",
            "3. Call emergency services",
            "4. Position patient (supine, legs elevated unless breathing difficulty)",
            "5. Administer oxygen if available",
            "6. Establish IV access",
            "7. Monitor vital signs continuously",
            "8. Repeat epinephrine every 5-15 min if needed"
        ],
        contraindications=[],
        evidence_level="A",
        source="World Allergy Organization Guidelines 2024",
        last_reviewed="2024-12-01",
        keywords=["allergy", "epinephrine", "anaphylaxis", "emergency"]
    ),
    # Treatment protocols
    create_protocol(
        "TX-001", "Type 2 Diabetes Initial Management",
        category="treatment", specialty="Endocrinology", condition="Type 2 Diabetes",
        description="Initial treatment protocol for newly diagnosed Type 2 Diabetes",
        steps=[
            "1. Confirm diagnosis (HbA1c ≥6.5% or FPG ≥126 mg/dL)",
            "2. Assess cardiovascular risk factors",
            "3. Initiate lifestyle modifications (diet, exercise)",
            "4. Start metformin if no contraindications (500mg BID, titrate)",
            "5. Set individualized HbA1c target",
            "6. Schedule follow-up in 3 months",
            "7. Order baseline labs (lipid panel, renal function, liver function)"
        ],
        contraindications=["eGFR <30", "Active liver disease", "History of lactic acidosis"],
        evidence_level="A",
        source="ADA Standards of Care 2025",
        last_reviewed="2025-01-10",
        keywords=["diabetes", "metformin", "glucose", "HbA1c"]
    ),
    create_protocol(
        "TX-002", "Hypertension First-Line Treatment",
        category="treatment", specialty="Cardiology", condition="Hypertension",
        description="First-line pharmacological treatment for essential hypertension",
        steps=[
            "1. Confirm diagnosis (≥130/80 mmHg on multiple readings)",
            "2. Assess cardiovascular risk and target organ damage",
            "3. Initiate lifestyle modifications",
            "4. Start first-line agent based on patient factors:",
            "   - ACE inhibitor or ARB (preferred if diabetes/CKD)",
            "   - Calcium channel blocker (preferred if elderly/Black)",
            "   - Thiazide diuretic",
            "5. Start at low dose, titrate every 2-4 weeks",
            "6. Target BP <130/80 for most patients"
        ],
        contraindications=["ACEi: pregnancy, angioedema history", "CCB: heart failure with reduced EF"],
        evidence_level="A",
        source="ACC/AHA Hypertension Guidelines 2024",
        last_reviewed="2024-11-15",
        keywords=["blood pressure", "hypertension", "ACE inhibitor", "antihypertensive"]
    ),
    # Diagnostic protocols
    create_protocol(
        "DX-001", "Chest Pain Evaluation",
        category="diagnostic", specialty="Cardiology", condition="Chest Pain",
        description="Diagnostic workup for acute chest pain presentation",
        steps=[
            "1. Obtain focused history (OPQRST)",
            "2. Perform physical examination",
            "3. Obtain 12-lead ECG within 10 minutes",
            "4. Order troponin (high-sensitivity if available)",
            "5. Calculate HEART score or similar risk stratification",
            "6. If STEMI: activate cath lab immediately",
            "7. If NSTEMI/UA: antiplatelet therapy, cardiology consult",
            "8. Consider alternative diagnoses (PE, aortic dissection, etc.)"
        ],
        contraindications=[],
        evidence_level="A",
        source="ACC/AHA Chest Pain Guidelines 2024",
        last_reviewed="2024-10-20",
        keywords=["chest pain", "MI", "ECG", "troponin", "cardiac"]
    ),
    create_protocol(
        "DX-002", "Stroke Assessment (NIHSS)",
        category="diagnostic", specialty="Neurology", condition="Stroke",
        description="Rapid stroke assessment using NIH Stroke Scale",
        steps=[
            "1. Note time of symptom onset (last known well)",
            "2. Perform NIHSS assessment:",
            "   - Level of consciousness",
            "   - Gaze",
            "   - Visual fields",
            "   - Facial palsy",
            "   - Motor arm/leg",
            "   - Limb ataxia",
            "   - Sensory",
            "   - Language",
            "   - Dysarthria",
            "   - Extinction/inattention",
            "3. Order CT head (non-contrast) STAT",
            "4. If <4.5 hours and eligible: consider tPA",
            "5. If LVO suspected: consider thrombectomy"
        ],
        contraindications=["tPA: recent surgery, bleeding disorder, BP >185/110"],
        evidence_level="A",
        source="AHA/ASA Stroke Guidelines 2024",
        last_reviewed="2024-09-15",
        keywords=["stroke", "NIHSS", "tPA", "thrombectomy", "neurological"]
    ),
    # Preventive protocols
    create_protocol(
        "PV-001", "Adult Immunization Schedule",
        category="preventive", specialty="Primary Care", condition="Preventive Care",
        description="Recommended adult immunization schedule",
        steps=[
            "1. Review immunization history",
            "2. Assess risk factors and contraindications",
            "3. Recommended vaccines for all adults:",
            "   - Influenza: annually",
            "   - Td/Tdap: every 10 years",
            "   - COVID-19: per current guidelines",
            "4. Age-based vaccines:",
            "   - Shingles (50+): 2 doses",
            "   - Pneumococcal (65+): PCV20 or PCV15+PPSV23",
            "5. Risk-based vaccines as indicated",
            "6. Document in immunization registry"
        ],
        contraindications=["Severe allergic reaction to vaccine component", "Moderate/severe acute illness"],
        evidence_level="A",
        source="CDC ACIP Recommendations 2025",
        last_reviewed="2025-01-01",
        keywords=["vaccine", "immunization", "preventive", "flu", "COVID"]
    ),
]

for protocol in protocols:
    glyph = model.encode(protocol)
    print(f"  ✓ {protocol.attributes['protocol_id']}: {protocol.attributes['name']}")

# =============================================================================
# Protocol Lookup Functions
# =============================================================================

def lookup_protocol(query: str, top_k: int = 3):
    """
    Look up relevant medical protocols based on a query.
    
    Returns protocols with citations and evidence levels.
    """
    print(f"\n{'='*60}")
    print(f"PROTOCOL LOOKUP")
    print(f"Query: {query}")
    print('='*60)
    print("\n⚠️  DISCLAIMER: For educational purposes only. Not medical advice.")
    
    results = model.similarity_search(query, top_k=top_k)
    
    protocols_found = []
    for result in results:
        if "protocol_id" in result.attributes:
            attrs = result.attributes
            protocols_found.append({
                "protocol_id": attrs["protocol_id"],
                "name": attrs["name"],
                "category": attrs["category"],
                "specialty": attrs["specialty"],
                "evidence_level": attrs["evidence_level"],
                "source": attrs["source"],
                "relevance": result.score
            })
    
    print(f"\nRelevant Protocols ({len(protocols_found)}):")
    for p in protocols_found:
        evidence_icon = "🟢" if p["evidence_level"] == "A" else "🟡" if p["evidence_level"] == "B" else "🟠"
        print(f"\n  {evidence_icon} {p['protocol_id']}: {p['name']}")
        print(f"     Category: {p['category']} | Specialty: {p['specialty']}")
        print(f"     Evidence Level: {p['evidence_level']}")
        print(f"     Source: {p['source']}")
        print(f"     Relevance: {p['relevance']:.2f}")
    
    return protocols_found


def get_protocol_details(protocol_id: str):
    """
    Get full details of a specific protocol.
    """
    print(f"\n{'='*60}")
    print(f"PROTOCOL DETAILS: {protocol_id}")
    print('='*60)
    print("\n⚠️  DISCLAIMER: For educational purposes only. Not medical advice.")
    
    results = model.similarity_search(protocol_id, top_k=1)
    
    if not results or "protocol_id" not in results[0].attributes:
        print("Protocol not found")
        return None
    
    attrs = results[0].attributes
    
    print(f"\n{attrs['name']}")
    print(f"{'='*60}")
    print(f"ID: {attrs['protocol_id']}")
    print(f"Category: {attrs['category']}")
    print(f"Specialty: {attrs['specialty']}")
    print(f"Condition: {attrs['condition']}")
    print(f"\nDescription:")
    print(f"  {attrs['description']}")
    print(f"\nSteps:")
    for step in attrs['steps']:
        print(f"  {step}")
    
    if attrs['contraindications']:
        print(f"\nContraindications:")
        for contra in attrs['contraindications']:
            print(f"  ⚠️  {contra}")
    
    print(f"\nEvidence & Source:")
    print(f"  Evidence Level: {attrs['evidence_level']}")
    print(f"  Source: {attrs['source']}")
    print(f"  Last Reviewed: {attrs['last_reviewed']}")
    
    return attrs


def check_contraindications(protocol_id: str, patient_factors: list):
    """
    Check if a protocol has contraindications for given patient factors.
    """
    print(f"\n{'='*60}")
    print(f"CONTRAINDICATION CHECK: {protocol_id}")
    print('='*60)
    
    results = model.similarity_search(protocol_id, top_k=1)
    
    if not results or "protocol_id" not in results[0].attributes:
        return None
    
    attrs = results[0].attributes
    contraindications = attrs.get('contraindications', [])
    
    print(f"\nProtocol: {attrs['name']}")
    print(f"Patient Factors: {patient_factors}")
    
    warnings = []
    for factor in patient_factors:
        for contra in contraindications:
            if factor.lower() in contra.lower():
                warnings.append({
                    "factor": factor,
                    "contraindication": contra
                })
    
    if warnings:
        print(f"\n⚠️  WARNINGS FOUND:")
        for w in warnings:
            print(f"  • {w['factor']}: {w['contraindication']}")
        print(f"\n  Consult physician before proceeding.")
    else:
        print(f"\n✓ No contraindications identified for given factors.")
        print(f"  Note: This is not a comprehensive check.")
    
    return warnings


def find_protocols_by_specialty(specialty: str):
    """
    Find all protocols for a given medical specialty.
    """
    print(f"\n{'='*60}")
    print(f"PROTOCOLS BY SPECIALTY: {specialty}")
    print('='*60)
    
    results = model.similarity_search(specialty, top_k=20)
    
    specialty_protocols = []
    for result in results:
        if "protocol_id" in result.attributes:
            attrs = result.attributes
            if specialty.lower() in attrs.get("specialty", "").lower():
                specialty_protocols.append({
                    "protocol_id": attrs["protocol_id"],
                    "name": attrs["name"],
                    "category": attrs["category"],
                    "condition": attrs["condition"]
                })
    
    print(f"\nProtocols Found: {len(specialty_protocols)}")
    for p in specialty_protocols:
        print(f"  • {p['protocol_id']}: {p['name']}")
        print(f"    {p['category']} - {p['condition']}")
    
    return specialty_protocols

# =============================================================================
# Test Protocol Lookups
# =============================================================================

print("\n" + "="*60)
print("TESTING MEDICAL PROTOCOLS")
print("="*60)

# Look up protocols
lookup_protocol("patient having heart attack")
lookup_protocol("how to treat high blood pressure")
lookup_protocol("allergic reaction emergency")

# Get protocol details
get_protocol_details("EM-001")

# Check contraindications
check_contraindications("TX-001", ["kidney disease", "liver problems"])

# Find by specialty
find_protocols_by_specialty("Cardiology")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("medical-protocols.glyphh")
print("✓ Model exported to medical-protocols.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @medical-protocols.glyphh")

print("\nLookup protocol via API:")
print('  curl -X POST http://localhost:8000/api/v1/medical-protocols/lookup \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"query": "chest pain evaluation"}\'')

print("\n" + "="*60)
print("KEY FEATURES")
print("="*60)
print("""
1. EVIDENCE-BASED
   - Every protocol has evidence level (A-D)
   - Citations to authoritative sources
   
2. TRACEABLE
   - Full audit trail of recommendations
   - Source and review date documented
   
3. SAFETY-FOCUSED
   - Contraindication checking
   - Clear disclaimers
   
4. HIERARCHICAL
   - Organized by specialty and category
   - Easy navigation and discovery

⚠️  IMPORTANT: This is a demonstration model only.
    Not intended for actual clinical use.
""")
