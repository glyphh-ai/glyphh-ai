# Glyphh Examples

Example code for building and deploying Glyphh models.

## Prerequisites

```bash
pip install glyphh
```

## Examples

### Basic Model

Create a simple model with concepts and similarity search:

```bash
python basic_model.py
```

### Intent Patterns

Add natural language query patterns to your model:

```bash
python intent_patterns.py
```

### FAQ Verification

Build an FAQ system where answers can't be wrong - every response is traced to an approved source:

```bash
python faq_verification.py
```

Key features:
- Deterministic answers with citations
- Approval tracking (who approved, when)
- Confidence scores for transparency
- Escalation when no confident match

### Churn Prediction

Predict customer churn using temporal pattern recognition:

```bash
python churn_prediction.py
```

Key features:
- No hardcoded sentiment rules
- Temporal edges learn from historical patterns
- Signals: spend, usage, support, defects, activity, renewal
- Explainable risk factors for each prediction

## Running Examples

1. Install the SDK:
   ```bash
   pip install glyphh
   ```

2. Run an example:
   ```bash
   cd examples
   python faq_verification.py
   ```

3. Deploy to runtime (optional):
   ```bash
   docker-compose up -d
   curl -X POST http://localhost:8000/api/deploy \
     -H "Content-Type: application/octet-stream" \
     --data-binary @faq-model.glyphh
   ```

## Example Output

```
Encoding concepts...
  ✓ Encoded: machine learning
  ✓ Encoded: neural network
  ✓ Encoded: deep learning

Similarity search for 'AI techniques':
  1. machine learning: 0.892
  2. deep learning: 0.856
  3. neural network: 0.823

Exporting model...
  ✓ Model exported to basic-model.glyphh
```
