"""
Patient Triage Example

Assist with patient triage by matching symptoms to urgency levels
using similarity search and intent pattern matching.

Key Principle: Triage decisions are based on symptom pattern matching
against established clinical criteria, with clear escalation paths.

This example demonstrates:
1. Creating symptom and urgency level concepts
2. Intent patterns for symptom description parsing
3. Similarity search for matching symptom patterns
4. Risk-based triage recommendations

Use Cases:
- Emergency department triage
- Telehealth symptom assessment
- Nurse hotline decision support
- Urgent care intake

DISCLAIMER: This is a demonstration model only. Not for actual medical use.
"""

from glyphh import GlyphhModel, Concept, EncoderConfig
from glyphh import IntentEncoder, IntentPattern

# Configure encoder
config = EncoderConfig(dimension=10000, seed=42)

# Create model
model = GlyphhModel(config)

# =============================================================================
# Define Triage Levels (ESI - Emergency Severity Index)
# =============================================================================

triage_levels = [
    Concept(
        name="esi_1_resuscitation",
        attributes={
            "level": 1,
            "name": "Resuscitation",
            "description": "Immediate life-saving intervention required",
            "response_time": "Immediate",
            "examples": [
                "Cardiac arrest",
                "Respiratory arrest",
                "Severe trauma with active bleeding",
                "Unresponsive"
            ],
            "color": "Red",
            "action": "Immediate resuscitation room"
        }
    ),
    Concept(
        name="esi_2_emergent",
        attributes={
            "level": 2,
            "name": "Emergent",
            "description": "High risk situation, confused/lethargic, or severe pain",
            "response_time": "Within 10 minutes",
            "examples": [
                "Chest pain with cardiac history",
                "Stroke symptoms",
                "Severe allergic reaction",
                "High fever with altered mental status"
            ],
            "color": "Orange",
            "action": "Priority treatment area"
        }
    ),
    Concept(
        name="esi_3_urgent",
        attributes={
            "level": 3,
            "name": "Urgent",
            "description": "Stable but needs multiple resources",
            "response_time": "Within 30 minutes",
            "examples": [
                "Abdominal pain requiring labs and imaging",
                "Moderate asthma exacerbation",
                "Laceration requiring sutures",
                "Urinary symptoms with fever"
            ],
            "color": "Yellow",
            "action": "Treatment area when available"
        }
    ),
    Concept(
        name="esi_4_less_urgent",
        attributes={
            "level": 4,
            "name": "Less Urgent",
            "description": "Stable, needs one resource",
            "response_time": "Within 60 minutes",
            "examples": [
                "Simple laceration",
                "Sprained ankle",
                "Earache",
                "Prescription refill needed"
            ],
            "color": "Green",
            "action": "Fast track area"
        }
    ),
    Concept(
        name="esi_5_non_urgent",
        attributes={
            "level": 5,
            "name": "Non-Urgent",
            "description": "Stable, no resources needed",
            "response_time": "Within 120 minutes",
            "examples": [
                "Minor cold symptoms",
                "Medication question",
                "Suture removal",
                "Minor rash"
            ],
            "color": "Blue",
            "action": "Waiting area"
        }
    ),
]

print("Encoding triage levels...")
for level in triage_levels:
    glyph = model.encode(level)
    print(f"  ✓ ESI {level.attributes['level']}: {level.attributes['name']}")

# =============================================================================
# Define Symptom Pattern Concepts
# =============================================================================

symptom_patterns = [
    # Cardiac symptoms
    Concept(
        name="chest_pain_cardiac",
        attributes={
            "symptom_group": "Cardiac",
            "chief_complaint": "Chest pain",
            "associated_symptoms": ["shortness of breath", "sweating", "nausea", "arm pain", "jaw pain"],
            "red_flags": ["crushing pain", "radiating to arm", "diaphoresis", "history of heart disease"],
            "suggested_esi": 2,
            "rationale": "Potential acute coronary syndrome requires immediate evaluation"
        }
    ),
    # Respiratory symptoms
    Concept(
        name="difficulty_breathing_severe",
        attributes={
            "symptom_group": "Respiratory",
            "chief_complaint": "Difficulty breathing",
            "associated_symptoms": ["wheezing", "cough", "chest tightness", "unable to speak full sentences"],
            "red_flags": ["cyanosis", "tripod position", "accessory muscle use", "altered mental status"],
            "suggested_esi": 2,
            "rationale": "Severe respiratory distress requires immediate intervention"
        }
    ),
    Concept(
        name="cough_mild",
        attributes={
            "symptom_group": "Respiratory",
            "chief_complaint": "Cough",
            "associated_symptoms": ["runny nose", "sore throat", "mild fever"],
            "red_flags": [],
            "suggested_esi": 5,
            "rationale": "Likely viral URI, no resources needed"
        }
    ),
    # Neurological symptoms
    Concept(
        name="stroke_symptoms",
        attributes={
            "symptom_group": "Neurological",
            "chief_complaint": "Sudden weakness or numbness",
            "associated_symptoms": ["facial droop", "arm weakness", "speech difficulty", "confusion"],
            "red_flags": ["sudden onset", "one-sided symptoms", "time of onset known"],
            "suggested_esi": 2,
            "rationale": "Potential stroke - time-sensitive treatment window"
        }
    ),
    Concept(
        name="headache_severe",
        attributes={
            "symptom_group": "Neurological",
            "chief_complaint": "Severe headache",
            "associated_symptoms": ["worst headache of life", "neck stiffness", "fever", "vision changes"],
            "red_flags": ["thunderclap onset", "fever with stiff neck", "altered consciousness"],
            "suggested_esi": 2,
            "rationale": "Rule out subarachnoid hemorrhage or meningitis"
        }
    ),
    # Abdominal symptoms
    Concept(
        name="abdominal_pain_severe",
        attributes={
            "symptom_group": "Abdominal",
            "chief_complaint": "Severe abdominal pain",
            "associated_symptoms": ["vomiting", "fever", "rigid abdomen", "bloody stool"],
            "red_flags": ["rigid abdomen", "rebound tenderness", "hemodynamic instability"],
            "suggested_esi": 2,
            "rationale": "Possible surgical emergency"
        }
    ),
    Concept(
        name="abdominal_pain_moderate",
        attributes={
            "symptom_group": "Abdominal",
            "chief_complaint": "Abdominal pain",
            "associated_symptoms": ["nausea", "decreased appetite", "mild tenderness"],
            "red_flags": [],
            "suggested_esi": 3,
            "rationale": "Needs evaluation with labs and possible imaging"
        }
    ),
    # Trauma
    Concept(
        name="trauma_major",
        attributes={
            "symptom_group": "Trauma",
            "chief_complaint": "Major trauma",
            "associated_symptoms": ["multiple injuries", "altered consciousness", "significant bleeding"],
            "red_flags": ["mechanism of injury", "uncontrolled bleeding", "deformity"],
            "suggested_esi": 1,
            "rationale": "Trauma activation criteria met"
        }
    ),
    Concept(
        name="laceration_simple",
        attributes={
            "symptom_group": "Trauma",
            "chief_complaint": "Cut/laceration",
            "associated_symptoms": ["bleeding controlled", "no tendon/nerve involvement"],
            "red_flags": [],
            "suggested_esi": 4,
            "rationale": "Simple repair needed, one resource"
        }
    ),
    # Allergic
    Concept(
        name="allergic_reaction_severe",
        attributes={
            "symptom_group": "Allergic",
            "chief_complaint": "Allergic reaction",
            "associated_symptoms": ["hives", "swelling", "difficulty breathing", "throat tightness"],
            "red_flags": ["airway compromise", "hypotension", "rapid progression"],
            "suggested_esi": 2,
            "rationale": "Potential anaphylaxis requires immediate treatment"
        }
    ),
]

print("\nEncoding symptom patterns...")
for pattern in symptom_patterns:
    glyph = model.encode(pattern)
    print(f"  ✓ {pattern.attributes['chief_complaint']} ({pattern.attributes['symptom_group']})")

# =============================================================================
# Set up Intent Patterns
# =============================================================================

intent_encoder = IntentEncoder(config)

intent_encoder.add_pattern(IntentPattern(
    intent_type="symptom_report",
    example_phrases=[
        "I have",
        "I'm experiencing",
        "patient presents with",
        "complaining of",
        "symptoms include",
    ],
    query_template={
        "operation": "triage",
        "type": "symptom_assessment"
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="pain_report",
    example_phrases=[
        "pain in",
        "hurts",
        "aching",
        "sharp pain",
        "severe pain",
    ],
    query_template={
        "operation": "triage",
        "type": "pain_assessment"
    }
))

intent_encoder.add_pattern(IntentPattern(
    intent_type="emergency",
    example_phrases=[
        "can't breathe",
        "chest pain",
        "unconscious",
        "not responding",
        "severe bleeding",
    ],
    query_template={
        "operation": "triage",
        "type": "emergency",
        "priority": "immediate"
    }
))

model.intent_encoder = intent_encoder

# =============================================================================
# Triage Functions
# =============================================================================

def assess_symptoms(symptom_description: str):
    """
    Assess symptoms and suggest triage level.
    
    Returns suggested ESI level with rationale.
    """
    print(f"\n{'='*60}")
    print(f"SYMPTOM ASSESSMENT")
    print(f"Reported: {symptom_description}")
    print('='*60)
    print("\n⚠️  DISCLAIMER: For demonstration only. Not medical advice.")
    
    # Check intent for emergency keywords
    intent_match = model.intent_encoder.match_intent(symptom_description)
    
    if intent_match.intent_type == "emergency" and intent_match.is_high_confidence():
        print(f"\n🚨 EMERGENCY KEYWORDS DETECTED")
        print(f"   Intent: {intent_match.intent_type} ({intent_match.confidence:.2f})")
    
    # Find matching symptom patterns
    results = model.similarity_search(symptom_description, top_k=3)
    
    matched_patterns = []
    for result in results:
        if "symptom_group" in result.attributes:
            attrs = result.attributes
            matched_patterns.append({
                "chief_complaint": attrs["chief_complaint"],
                "symptom_group": attrs["symptom_group"],
                "suggested_esi": attrs["suggested_esi"],
                "rationale": attrs["rationale"],
                "red_flags": attrs.get("red_flags", []),
                "relevance": result.score
            })
    
    if matched_patterns:
        top_match = matched_patterns[0]
        suggested_esi = top_match["suggested_esi"]
        
        # Get ESI level details
        esi_details = None
        for level in triage_levels:
            if level.attributes["level"] == suggested_esi:
                esi_details = level.attributes
                break
        
        print(f"\nMatched Pattern: {top_match['chief_complaint']}")
        print(f"Symptom Group: {top_match['symptom_group']}")
        print(f"Relevance: {top_match['relevance']:.2f}")
        
        if top_match["red_flags"]:
            print(f"\n🚩 Red Flags to Assess:")
            for flag in top_match["red_flags"]:
                print(f"   • {flag}")
        
        print(f"\n{'='*60}")
        print(f"SUGGESTED TRIAGE LEVEL")
        print('='*60)
        
        if esi_details:
            color_emoji = {"Red": "🔴", "Orange": "🟠", "Yellow": "🟡", "Green": "🟢", "Blue": "🔵"}
            print(f"\n{color_emoji.get(esi_details['color'], '⚪')} ESI Level {suggested_esi}: {esi_details['name']}")
            print(f"   Response Time: {esi_details['response_time']}")
            print(f"   Action: {esi_details['action']}")
        
        print(f"\nRationale: {top_match['rationale']}")
        
        return {
            "suggested_esi": suggested_esi,
            "matched_pattern": top_match,
            "esi_details": esi_details,
            "other_matches": matched_patterns[1:]
        }
    
    print("\n⚠️  No clear pattern match. Recommend clinical assessment.")
    return None


def check_red_flags(symptoms: list):
    """
    Check a list of symptoms for red flags that indicate higher acuity.
    """
    print(f"\n{'='*60}")
    print(f"RED FLAG CHECK")
    print('='*60)
    
    all_red_flags = []
    
    for symptom in symptoms:
        results = model.similarity_search(symptom, top_k=2)
        
        for result in results:
            if "red_flags" in result.attributes:
                for flag in result.attributes["red_flags"]:
                    if flag.lower() in symptom.lower():
                        all_red_flags.append({
                            "symptom": symptom,
                            "red_flag": flag,
                            "pattern": result.attributes.get("chief_complaint")
                        })
    
    if all_red_flags:
        print(f"\n🚩 RED FLAGS IDENTIFIED:")
        for rf in all_red_flags:
            print(f"   • {rf['red_flag']}")
            print(f"     From: {rf['symptom']}")
        print(f"\n⚠️  Consider upgrading triage level")
    else:
        print(f"\n✓ No red flags identified in reported symptoms")
    
    return all_red_flags


def get_triage_questions(symptom_group: str):
    """
    Get relevant triage questions for a symptom group.
    """
    print(f"\n{'='*60}")
    print(f"TRIAGE QUESTIONS: {symptom_group}")
    print('='*60)
    
    # Standard triage questions by symptom group
    questions = {
        "Cardiac": [
            "When did the pain start?",
            "Is the pain constant or intermittent?",
            "Does the pain radiate anywhere?",
            "Are you sweating or feeling nauseous?",
            "Do you have a history of heart problems?",
            "Have you taken any medications?"
        ],
        "Respiratory": [
            "When did the breathing difficulty start?",
            "Can you speak in full sentences?",
            "Do you have a history of asthma or COPD?",
            "Are you coughing? Any blood?",
            "Do you have chest pain?",
            "Have you had recent illness or travel?"
        ],
        "Neurological": [
            "When did symptoms start exactly?",
            "Is there weakness on one side?",
            "Any changes in speech or vision?",
            "Any headache? Worst ever?",
            "Any recent head injury?",
            "History of stroke or seizures?"
        ],
        "Abdominal": [
            "Where exactly is the pain?",
            "When did it start?",
            "Any vomiting or diarrhea?",
            "Any blood in stool or vomit?",
            "When was your last bowel movement?",
            "Any fever?"
        ],
    }
    
    group_questions = questions.get(symptom_group, [
        "When did symptoms start?",
        "How severe on a scale of 1-10?",
        "Any other symptoms?",
        "Any relevant medical history?",
        "Any medications or allergies?"
    ])
    
    print(f"\nRecommended Questions:")
    for i, q in enumerate(group_questions, 1):
        print(f"  {i}. {q}")
    
    return group_questions

# =============================================================================
# Test Triage System
# =============================================================================

print("\n" + "="*60)
print("TESTING PATIENT TRIAGE")
print("="*60)

# Test various symptom presentations
test_cases = [
    "Patient has crushing chest pain radiating to left arm, sweating",
    "Mild cough and runny nose for 3 days",
    "Sudden severe headache, worst of my life, with stiff neck",
    "Cut on hand from kitchen knife, bleeding controlled",
    "Difficulty breathing, can't speak full sentences, wheezing",
]

for case in test_cases:
    assess_symptoms(case)

# Check red flags
print("\n" + "="*60)
print("RED FLAG ASSESSMENT")
print("="*60)

check_red_flags([
    "crushing chest pain",
    "sudden onset weakness on right side",
    "fever with stiff neck"
])

# Get triage questions
get_triage_questions("Cardiac")

# =============================================================================
# Export Model
# =============================================================================

print("\n" + "="*60)
print("EXPORTING MODEL")
print("="*60)

model.export("patient-triage.glyphh")
print("✓ Model exported to patient-triage.glyphh")

print("\nDeploy to runtime:")
print("  curl -X POST http://localhost:8000/api/deploy \\")
print("    -H 'Content-Type: application/octet-stream' \\")
print("    --data-binary @patient-triage.glyphh")

print("\nAssess symptoms via API:")
print('  curl -X POST http://localhost:8000/api/v1/patient-triage/assess \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"symptoms": "chest pain with shortness of breath"}\'')

print("\n" + "="*60)
print("KEY FEATURES")
print("="*60)
print("""
1. PATTERN-BASED TRIAGE
   - Match symptoms to established patterns
   - ESI level recommendations
   
2. RED FLAG DETECTION
   - Identify high-risk symptoms
   - Automatic escalation triggers
   
3. GUIDED ASSESSMENT
   - Symptom-specific questions
   - Structured data collection
   
4. SAFETY-FOCUSED
   - Clear disclaimers
   - Conservative recommendations

⚠️  IMPORTANT: This is a demonstration model only.
    Not intended for actual clinical use.
""")
