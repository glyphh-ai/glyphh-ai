# Troubleshooting Guide

Common issues and solutions for Glyphh SDK and Runtime.

## CLI Issues

### Command Not Found

```
zsh: command not found: glyphh
```

**Solution:** Ensure SDK is installed and in PATH:

```bash
pip install glyphh
# Or if using virtual environment
source venv/bin/activate
```

### Connection Error

```
❌ Connection Error: Could not connect to http://localhost:8000
```

**Solutions:**
1. Start the runtime: `docker-compose up -d`
2. Check RUNTIME_URL in .env
3. Verify network connectivity

### Authentication Error

```
❌ Authentication Error: Invalid or missing JWT token
```

**Solutions:**
1. Get a new token from https://platform.glyphh.com
2. Update JWT_TOKEN in .env
3. Ensure token hasn't expired

### Authorization Error

```
❌ Authorization Error: You don't have permission
```

**Solutions:**
1. Check token permissions in Platform UI
2. Ensure you have deploy permissions for the org

## Runtime Issues

### Database Connection Failed

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
1. Check DATABASE_URL in environment
2. Ensure PostgreSQL is running: `docker-compose ps db`
3. Verify pgvector extension is installed

### License Validation Failed

```
License validation failed: Unable to reach platform
```

**Solutions:**
1. Check LICENSE_KEY is correct
2. Verify network can reach platform.glyphh.com
3. Runtime enters 7-day grace period on failure

### Out of Memory

```
MemoryError: Unable to allocate array
```

**Solutions:**
1. Reduce model dimension
2. Use lite runtime image
3. Increase container memory limits

## SDK Issues

### Dimension Mismatch

```
ValueError: Dimension mismatch: expected 10000, got 5000
```

**Solution:** Ensure all glyphs use the same EncoderConfig dimension.

### Invalid Config

```
ConfigurationException: Invalid dimension: must be positive
```

**Solution:** Check EncoderConfig values:
- dimension > 0
- seed is an integer
- weights are 0.0-1.0

### Encoding Failed

```
EncodingException: Failed to encode concept
```

**Solutions:**
1. Check concept has required attributes
2. Verify attribute values are strings
3. Check for special characters in values

## Query Issues

### No Results

```json
{"results": [], "total_count": 0}
```

**Solutions:**
1. Verify data was loaded successfully
2. Check query syntax
3. Lower similarity threshold

### Low Similarity Scores

**Solutions:**
1. Adjust similarity weights in config
2. Ensure concepts have matching attributes
3. Check encoder configuration matches

## Getting Help

- [GitHub Issues](https://github.com/glyphh-ai/glyphh-sdk/issues)
- [Discord Community](https://discord.gg/glyphh)
- [Email Support](mailto:support@glyphh.ai)
