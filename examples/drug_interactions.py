"""
Drug Interaction Checker Example

Check for potential drug-drug interactions using fact trees and
similarity search to identify contraindicated combinations.

Key Principle: Every interaction warning is traceable to clinical
evidence with severity levels and recommended actions.

This example demonstrates:
1. Creating drug concepts with interaction profiles
2. Fact trees for drug class relationships
3. Similarity search for finding interaction patterns
4. Severity-based warnings with clinical guidance

Use Cases:
- Pharmacy dispensing systems
- Electronic health records
- Medication reconciliation
- Clinical decision support

DISCLAIMER: This is a demonstration model only. Not for actual medical use.
"""

from glyphh import GlyphhModel, Concept, EncoderConfig

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Drug Concepts
# =============================================================================

def create_drug(
    drug_id: str,
    generic_name: str,
    brand_names: list,
    drug_class: str,
    mechanism: str,
    # Indications
    indications: list,
    # Interactions
    interacts_with: list,  # List of drug classes/names
    interaction_severity: dict,  # {drug: severity}
    # Contraindications
    contraindications: list,
    # Metabolism
    cyp_substrate: list = None,
    cyp_inhibitor: list = None,
    cyp_inducer: list = None,
):
    """Create a drug concept with interaction profile."""
    return Concept(
        name=f"drug_{drug_id}",
        attributes={
            "drug_id": drug_id,
            "generic_name": generic_name,
            "brand_names": brand_names,
            "drug_class": drug_class,
            "mechanism": mechanism,
            "indications": indications,
            "interacts_with": interacts_with,
            "interaction_severity": interaction_severity,
            "contraindications": contraindications,
            "cyp_substrate": cyp_substrate or [],
            "cyp_inhibitor": cyp_inhibitor or [],
            "cyp_inducer": cyp_inducer or [],
            # For cortex similarity
            "layer": drug_class,
        }
    )

# =============================================================================
# Define Drug Interaction Concepts
# =============================================================================

def create_interaction(
    interaction_id: str,
    drug_a: str,
    drug_b: str,
    severity: str,  # "contraindicated", "major", "moderate", "minor"
    mechanism: str,
    clinical_effect: str,
    management: str,
    evidence_level: str,
    source: str,
):
    """Create a drug interaction concept."""
    return Concept(
        name=f"interaction_{interaction_id}",
        attributes={
            "interaction_id": interaction_id,
            "drug_a": drug_a,
            "drug_b": drug_b,
            "severity": severity,
            "mechanism": mechanism,
            "clinical_effect": clinical_effect,
            "management": management,
            "evidence_level": evidence_level,
            "source": source,
        }
    )

# =============================================================================
# Create Drug Database
# =============================================================================

print("Creating drug database...")

drugs = [
    create_drug(
        "D001", "warfarin", ["Coumadin", "Jantoven"],
        drug_class="Anticoagulant",
        mechanism="Vitamin K antagonist",
        indications=["Atrial fibrillation", "DVT/PE", "Mechanical heart valve"],
        interacts_with=["NSAIDs", "Aspirin", "Antibiotics", "Antifungals"],
        interaction_severity={"aspirin": "major", "ibuprofen": "major", "fluconazole": "major"},
        contraindications=["Active bleeding", "Pregnancy"],
        cyp_substrate=["CYP2C9", "CYP3A4"],
    ),
    create_drug(
        "D002", "aspirin", ["Bayer", "Ecotrin"],
        drug_class="NSAID/Antiplatelet",
        mechanism="COX inhibitor, irreversible platelet inhibition",
        indications=["Pain", "Fever", "Cardiovascular prevention"],
        interacts_with=["Anticoagulants", "Other NSAIDs", "SSRIs"],
        interaction_severity={"warfarin": "major", "ibuprofen": "moderate"},
        contraindications=["Active GI bleeding", "Aspirin allergy"],
    ),
    create_drug(
        "D003", "ibuprofen", ["Advil", "Motrin"],
        drug_class="NSAID",
        mechanism="COX-1 and COX-2 inhibitor",
        indications=["Pain", "Fever", "Inflammation"],
        interacts_with=["Anticoagulants", "Aspirin", "ACE inhibitors", "Lithium"],
        interaction_severity={"warfarin": "major", "aspirin": "moderate", "lisinopril": "moderate"},
        contraindications=["GI bleeding", "Severe renal impairment", "Third trimester pregnancy"],
    ),
    create_drug(
        "D004", "lisinopril", ["Prinivil", "Zestril"],
        drug_class="ACE Inhibitor",
        mechanism="Angiotensin-converting enzyme inhibitor",
        indications=["Hypertension", "Heart failure", "Diabetic nephropathy"],
        interacts_with=["Potassium supplements", "NSAIDs", "ARBs"],
        interaction_severity={"potassium": "major", "ibuprofen": "moderate", "losartan": "major"},
        contraindications=["Pregnancy", "Angioedema history", "Bilateral renal artery stenosis"],
    ),
    create_drug(
        "D005", "metformin", ["Glucophage"],
        drug_class="Biguanide",
        mechanism="Decreases hepatic glucose production",
        indications=["Type 2 diabetes"],
        interacts_with=["Contrast dye", "Alcohol"],
        interaction_severity={"contrast": "major"},
        contraindications=["eGFR <30", "Metabolic acidosis"],
    ),
    create_drug(
        "D006", "simvastatin", ["Zocor"],
        drug_class="Statin",
        mechanism="HMG-CoA reductase inhibitor",
        indications=["Hyperlipidemia", "Cardiovascular prevention"],
        interacts_with=["CYP3A4 inhibitors", "Gemfibrozil", "Grapefruit"],
        interaction_severity={"clarithromycin": "contraindicated", "gemfibrozil": "major"},
        contraindications=["Active liver disease", "Pregnancy"],
        cyp_substrate=["CYP3A4"],
    ),
    create_drug(
        "D007", "clarithromycin", ["Biaxin"],
        drug_class="Macrolide Antibiotic",
        mechanism="Protein synthesis inhibitor",
        indications=["Respiratory infections", "H. pylori"],
        interacts_with=["Statins", "QT-prolonging drugs", "Warfarin"],
        interaction_severity={"simvastatin": "contraindicated", "warfarin": "major"},
        contraindications=["QT prolongation", "Severe hepatic impairment"],
        cyp_inhibitor=["CYP3A4"],
    ),
    create_drug(
        "D008", "fluconazole", ["Diflucan"],
        drug_class="Azole Antifungal",
        mechanism="Inhibits fungal CYP450",
        indications=["Fungal infections", "Candidiasis"],
        interacts_with=["Warfarin", "Statins", "QT-prolonging drugs"],
        interaction_severity={"warfarin": "major", "simvastatin": "major"},
        contraindications=["QT prolongation"],
        cyp_inhibitor=["CYP2C9", "CYP3A4"],
    ),
    create_drug(
        "D009", "sertraline", ["Zoloft"],
        drug_class="SSRI",
        mechanism="Selective serotonin reuptake inhibitor",
        indications=["Depression", "Anxiety", "OCD", "PTSD"],
        interacts_with=["MAOIs", "NSAIDs", "Anticoagulants", "Tramadol"],
        interaction_severity={"phenelzine": "contraindicated", "aspirin": "moderate", "tramadol": "major"},
        contraindications=["MAOI use within 14 days"],
        cyp_substrate=["CYP2D6"],
    ),
    create_drug(
        "D010", "omeprazole", ["Prilosec"],
        drug_class="Proton Pump Inhibitor",
        mechanism="H+/K+ ATPase inhibitor",
        indications=["GERD", "Peptic ulcer", "H. pylori"],
        interacts_with=["Clopidogrel", "Methotrexate"],
        interaction_severity={"clopidogrel": "major"},
        contraindications=[],
        cyp_inhibitor=["CYP2C19"],
    ),
]

for drug in drugs:
    glyph = model.encode(drug)
    print(f"  ✓ {drug.attributes['generic_name']} ({drug.attributes['drug_class']})")

# =============================================================================
# Create Known Interactions
# =============================================================================

print("\nCreating interaction database...")

interactions = [
    create_interaction(
        "INT001", "warfarin", "aspirin",
        severity="major",
        mechanism="Additive anticoagulant/antiplatelet effects",
        clinical_effect="Increased risk of bleeding",
        management="Avoid combination if possible. If necessary, monitor closely for bleeding.",
        evidence_level="A",
        source="Clinical Pharmacology Database"
    ),
    create_interaction(
        "INT002", "warfarin", "fluconazole",
        severity="major",
        mechanism="Fluconazole inhibits CYP2C9, increasing warfarin levels",
        clinical_effect="Significantly increased INR and bleeding risk",
        management="Reduce warfarin dose by 25-50%. Monitor INR closely.",
        evidence_level="A",
        source="FDA Drug Interaction Database"
    ),
    create_interaction(
        "INT003", "simvastatin", "clarithromycin",
        severity="contraindicated",
        mechanism="Clarithromycin inhibits CYP3A4, dramatically increasing simvastatin levels",
        clinical_effect="High risk of rhabdomyolysis",
        management="Do not use together. Use alternative antibiotic or switch statin.",
        evidence_level="A",
        source="FDA Drug Safety Communication"
    ),
    create_interaction(
        "INT004", "lisinopril", "ibuprofen",
        severity="moderate",
        mechanism="NSAIDs reduce prostaglandin-mediated renal blood flow",
        clinical_effect="Reduced antihypertensive effect, increased renal risk",
        management="Monitor blood pressure and renal function. Use lowest NSAID dose.",
        evidence_level="B",
        source="Clinical Pharmacology Database"
    ),
    create_interaction(
        "INT005", "sertraline", "tramadol",
        severity="major",
        mechanism="Both increase serotonin; additive serotonergic effects",
        clinical_effect="Risk of serotonin syndrome",
        management="Avoid combination. If necessary, monitor for serotonin syndrome symptoms.",
        evidence_level="B",
        source="FDA Drug Interaction Database"
    ),
    create_interaction(
        "INT006", "omeprazole", "clopidogrel",
        severity="major",
        mechanism="Omeprazole inhibits CYP2C19, reducing clopidogrel activation",
        clinical_effect="Reduced antiplatelet effect, increased cardiovascular risk",
        management="Use alternative PPI (pantoprazole) or H2 blocker.",
        evidence_level="B",
        source="FDA Drug Safety Communication"
    ),
]

for interaction in interactions:
    glyph = model.encode(interaction)
    print(f"  ✓ {interaction.attributes['drug_a']} + {interaction.attributes['drug_b']}: {interaction.attributes['severity']}")

# =============================================================================
# Interaction Checking Functions
# =============================================================================

def check_interaction(drug_a: str, drug_b: str):
    """
    Check for interaction between two drugs.
    """
    print(f"\n{'='*60}")
    print(f"INTERACTION CHECK")
    print(f"Drug A: {drug_a}")
    print(f"Drug B: {drug_b}")
    print('='*60)
    print("\n⚠️  DISCLAIMER: For demonstration only. Verify with clinical resources.")
    
    # Search for known interaction
    query = f"{drug_a} {drug_b} interaction"
    results = model.similarity_search(query, top_k=5)
    
    found_interaction = None
    for result in results:
        if "interaction_id" in result.attributes:
            attrs = result.attributes
            drugs_in_interaction = [attrs["drug_a"].lower(), attrs["drug_b"].lower()]
            if drug_a.lower() in drugs_in_interaction and drug_b.lower() in drugs_in_interaction:
                found_interaction = attrs
                break
    
    if found_interaction:
        severity = found_interaction["severity"]
        severity_icons = {
            "contraindicated": "🔴",
            "major": "🟠",
            "moderate": "🟡",
            "minor": "🟢"
        }
        
        print(f"\n{severity_icons.get(severity, '⚪')} INTERACTION FOUND: {severity.upper()}")
        print(f"\nMechanism:")
        print(f"  {found_interaction['mechanism']}")
        print(f"\nClinical Effect:")
        print(f"  {found_interaction['clinical_effect']}")
        print(f"\nManagement:")
        print(f"  {found_interaction['management']}")
        print(f"\nEvidence Level: {found_interaction['evidence_level']}")
        print(f"Source: {found_interaction['source']}")
        
        return found_interaction
    
    # Check drug profiles for class-level interactions
    drug_a_results = model.similarity_search(drug_a, top_k=1)
    drug_b_results = model.similarity_search(drug_b, top_k=1)
    
    if drug_a_results and drug_b_results:
        drug_a_attrs = drug_a_results[0].attributes
        drug_b_attrs = drug_b_results[0].attributes
        
        # Check if drug classes interact
        a_interacts = drug_a_attrs.get("interacts_with", [])
        b_class = drug_b_attrs.get("drug_class", "")
        
        if any(b_class.lower() in i.lower() for i in a_interacts):
            print(f"\n🟡 POTENTIAL CLASS INTERACTION")
            print(f"  {drug_a} may interact with {b_class} drugs")
            print(f"  Recommend clinical review")
            return {"severity": "potential", "drug_class": b_class}
    
    print(f"\n✓ No known interaction found")
    print(f"  Note: Absence of data does not guarantee safety")
    
    return None


def check_medication_list(medications: list):
    """
    Check a list of medications for all pairwise interactions.
    """
    print(f"\n{'='*60}")
    print(f"MEDICATION LIST REVIEW")
    print(f"Medications: {', '.join(medications)}")
    print('='*60)
    print("\n⚠️  DISCLAIMER: For demonstration only. Verify with clinical resources.")
    
    interactions_found = []
    
    # Check all pairs
    for i in range(len(medications)):
        for j in range(i + 1, len(medications)):
            drug_a = medications[i]
            drug_b = medications[j]
            
            # Search for interaction
            query = f"{drug_a} {drug_b}"
            results = model.similarity_search(query, top_k=3)
            
            for result in results:
                if "interaction_id" in result.attributes:
                    attrs = result.attributes
                    drugs_in_interaction = [attrs["drug_a"].lower(), attrs["drug_b"].lower()]
                    if drug_a.lower() in drugs_in_interaction or drug_b.lower() in drugs_in_interaction:
                        interactions_found.append({
                            "drug_a": drug_a,
                            "drug_b": drug_b,
                            "severity": attrs["severity"],
                            "clinical_effect": attrs["clinical_effect"]
                        })
                        break
    
    # Sort by severity
    severity_order = {"contraindicated": 0, "major": 1, "moderate": 2, "minor": 3}
    interactions_found.sort(key=lambda x: severity_order.get(x["severity"], 4))
    
    if interactions_found:
        print(f"\n⚠️  INTERACTIONS FOUND: {len(interactions_found)}")
        
        for interaction in interactions_found:
            severity_icons = {
                "contraindicated": "🔴",
                "major": "🟠",
                "moderate": "🟡",
                "minor": "🟢"
            }
            icon = severity_icons.get(interaction["severity"], "⚪")
            print(f"\n  {icon} {interaction['drug_a']} + {interaction['drug_b']}")
            print(f"     Severity: {interaction['severity'].upper()}")
            print(f"     Effect: {interaction['clinical_effect']}")
    else:
        print(f"\n✓ No known interactions found between listed medications")
    
    return interactions_found


def get_drug_info(drug_name: str):
    """
    Get detailed information about a drug.
    """
    print(f"\n{'='*60}")
    print(f"DRUG INFORMATION: {drug_name}")
    print('='*60)
    
    results = model.similarity_search(drug_name, top_k=1)
    
    if not results or "drug_id" not in results[0].attributes:
        print("Drug not found in database")
        return None
    
    attrs = results[0].attributes
    
    print(f"\nGeneric Name: {attrs['generic_name']}")
    print(f"Brand Names: {', '.join(attrs['brand_names'])}")
    print(f"Drug Class: {attrs['drug_class']}")
    print(f"Mechanism: {attrs['mechanism']}")
    
    print(f"\nIndications:")
    for ind in attrs['indications']:
        print(f"  • {ind}")
    
    print(f"\nKnown Interactions With:")
    for inter in attrs['interacts_with']:
        print(f"  • {inter}")
    
    if attrs['contraindications']:
        print(f"\nContraindications:")
        for contra in attrs['contraindications']:
            print(f"  ⚠️  {contra}")
    
    if attrs.get('cyp_substrate'):
        print(f"\nMetabolism (CYP Substrates): {', '.join(attrs['cyp_substrate'])}")
    if attrs.get('cyp_inhibitor'):
        print(f"CYP Inhibitor: {', '.join(attrs['cyp_inhibitor'])}")
    
    return attrs

# =============================================================================
# Test Drug Interaction Checker
# =============================================================================

print("\n" + "="*60)
print("TESTING DRUG INTERACTION CHECKER")
print("="*60)

# Check specific interactions
check_interaction("warfarin", "aspirin")
check_interaction("simvastatin", "clarithromycin")
check_interaction("lisinopril", "ibuprofen")

# Check medication list
check_medication_list(["warfarin", "aspirin", "lisinopril", "metformin"])

# Get drug info
get_drug_info("warfarin")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("drug-interactions.glyphh")
print("✓ Model exported to drug-interactions.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @drug-interactions.glyphh")

print("\nCheck interaction via API:")
print('  curl -X POST http://localhost:8000/api/v1/drug-interactions/check \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"drug_a": "warfarin", "drug_b": "aspirin"}\'')

print("\n" + "="*60)
print("KEY FEATURES")
print("="*60)
print("""
1. SEVERITY-BASED ALERTS
   - Contraindicated, Major, Moderate, Minor
   - Clear visual indicators
   
2. EVIDENCE-BASED
   - Citations to clinical sources
   - Evidence levels documented
   
3. ACTIONABLE GUIDANCE
   - Management recommendations
   - Alternative suggestions
   
4. COMPREHENSIVE CHECKING
   - Pairwise interaction checking
   - Full medication list review

⚠️  IMPORTANT: This is a demonstration model only.
    Not intended for actual clinical use.
""")
