# Model Versioning Guide

This guide explains how to version your Glyphh models effectively using semantic versioning, manage version history, and publish models to the marketplace.

## Semantic Versioning for Models

Glyphh models use semantic versioning (SemVer) in the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Increment when you make incompatible changes to the model structure
  - Changing layer/segment/role names
  - Removing roles or segments
  - Changing dimension or encoding strategy
  
- **MINOR**: Increment when you add functionality in a backward-compatible manner
  - Adding new roles or segments
  - Adding new intent patterns or stored procedures
  - Expanding the model's capabilities
  
- **PATCH**: Increment for backward-compatible bug fixes
  - Fixing typos in role names
  - Adjusting weights
  - Updating metadata

### Example Version Progression

```
1.0.0 - Initial release
1.0.1 - Fixed typo in role name
1.1.0 - Added new "category" role
1.2.0 - Added intent patterns for NL queries
2.0.0 - Restructured layers (breaking change)
```

## Setting Model Version

### In notebook.py

Set the version constant at the top of your notebook:

```python
MODEL_NAME = "my_model"
MODEL_VERSION = "1.2.0"  # Semantic version
```

The version is automatically embedded when you export:

```python
export_model(encoder, glyphs, intent_encoder, stored_procedures)
```

### Using CLI

Specify version when creating a package:

```bash
glyphh package create --output my_model.glyphh --version 1.2.0
```

View version information:

```bash
glyphh package info my_model.glyphh
```

## Version History

### How Version History Works

Every time you deploy a model to the Runtime, a version history entry is created:

- **version**: The semantic version from the .glyphh file
- **deployed_at**: Timestamp of deployment
- **deployed_by**: User who deployed (if authenticated)
- **is_current**: Whether this is the currently active version

### Viewing Version History

**Via API:**
```bash
curl https://runtime.glyphh.com/api/models/{org_id}/{model_id}/versions
```

**Response:**
```json
{
  "org_id": "my-org",
  "model_id": "my-model",
  "versions": [
    {
      "version": "1.2.0",
      "deployed_at": "2024-01-15T10:30:00Z",
      "deployed_by": "user@example.com",
      "is_current": true
    },
    {
      "version": "1.1.0",
      "deployed_at": "2024-01-10T14:20:00Z",
      "deployed_by": "user@example.com",
      "is_current": false
    }
  ]
}
```

**In Studio UI:**
Version history is displayed in the model details view.

### Version History Retention

Version history is retained even when:
- The model is undeployed
- The model is deleted from the platform
- A new version is deployed

This ensures you always have an audit trail of deployments.

## SDK Version vs Model Version

It's important to understand the difference:

| Aspect | SDK Version | Model Version |
|--------|-------------|---------------|
| What it represents | Glyphh SDK release | Your model's release |
| Who controls it | Glyphh team | You |
| Format | X.Y.Z (e.g., 0.1.0) | X.Y.Z (e.g., 1.2.0) |
| Where stored | SDK package | .glyphh file metadata |

The SDK version is recorded alongside your model version during deployment for compatibility tracking.

## Publishing to Marketplace

### Requirements for Publishing

Before publishing a model to the marketplace:

1. **Version**: Must have a valid semantic version
2. **Description**: At least 20 characters
3. **Category**: Select from NLP, Vision, Audio, Multimodal, Analytics, or Custom

### Publishing Workflow

1. **Prepare your model** with proper versioning
2. **Add description** in the Studio UI Info tab
3. **Click "Share"** to publish to marketplace
4. **Users can import** your model to their workspace

### Version Validation on Publish

When publishing updates to an already-published model:
- The new version should be greater than the previous published version
- Use semantic versioning to communicate the nature of changes

### Unpublishing

You can unpublish a model at any time:
- The model becomes private again
- Users who already imported keep their copy
- You can republish later with a new version

## Best Practices

### 1. Start with 1.0.0

Begin your model at version 1.0.0 when it's ready for use:

```python
MODEL_VERSION = "1.0.0"
```

### 2. Document Changes

Keep a changelog in your model's metadata:

```python
metadata={
    "changelog": {
        "1.2.0": "Added intent patterns for customer queries",
        "1.1.0": "Added category role",
        "1.0.0": "Initial release"
    }
}
```

### 3. Test Before Incrementing

Always test your model before incrementing the version:

```python
# Test similarity
test_similarity(glyph1, glyph2)

# Test intent matching
test_intent_matching(intent_encoder, test_queries)

# Then export with new version
MODEL_VERSION = "1.2.0"
export_model(encoder, glyphs, intent_encoder)
```

### 4. Use Pre-release Versions for Testing

For testing, use pre-release versions:

```python
MODEL_VERSION = "1.2.0-beta.1"
```

### 5. Coordinate with Deployments

When deploying to production:
1. Increment version appropriately
2. Deploy to staging first
3. Verify functionality
4. Deploy to production

## Troubleshooting

### Invalid Version Format

If you see "Invalid version format" error:
- Ensure version follows X.Y.Z format
- Use only numbers and dots
- Example: `1.0.0`, `2.1.3`, `10.20.30`

### Version Not Updating

If version history shows old version:
- Verify MODEL_VERSION is updated in notebook.py
- Re-export the .glyphh file
- Redeploy to Runtime

### Missing Version History

If version history is empty:
- Model may not have been deployed yet
- Check Runtime logs for deployment errors
