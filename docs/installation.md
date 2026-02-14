# Installation

This page covers all installation options for Glyphh SDK and Runtime.

## SDK Installation

### From PyPI (Recommended)

```bash
pip install glyphh
```

### From GitHub Releases

Download the latest wheel from [GitHub Releases](https://github.com/glyphh/glyphh-sdk/releases):

```bash
# Download the wheel for your platform
pip install glyphh-X.Y.Z-py3-none-any.whl
```

### From Source

```bash
git clone https://github.com/glyphh/glyphh-sdk.git
cd glyphh-sdk
pip install -e .
```

### Verify Installation

```bash
# Check version
glyphh --version

# Test import
python -c "import glyphh; print(f'Glyphh SDK {glyphh.__version__}')"
```

## Runtime Installation

### Docker (Recommended)

Pull the latest image:

```bash
docker pull ghcr.io/glyphh/runtime:latest
```

Or a specific version:

```bash
docker pull ghcr.io/glyphh/runtime:1.0.0
```

### From GitHub Releases

Download the Docker image or source from [GitHub Releases](https://github.com/glyphh/glyphh-runtime/releases).

### From Source

```bash
git clone https://github.com/glyphh/glyphh-runtime.git
cd glyphh-runtime
pip install -r requirements.txt
```

## Version Compatibility

| SDK Version | Runtime Version | Notes |
|-------------|-----------------|-------|
| 0.1.x | 1.0.x | Initial release |
| 0.2.x | 1.1.x | Added NL query support |

## System Requirements

### SDK

- Python 3.9 or higher
- pip 21.0 or higher
- 100MB disk space

### Runtime

- Docker 20.10 or higher (for Docker deployment)
- PostgreSQL 14+ with pgvector extension
- 512MB RAM minimum (2GB recommended)
- 1GB disk space

## Troubleshooting

### SDK Installation Issues

**pip install fails with "No matching distribution"**
- Ensure Python 3.9+ is installed
- Try upgrading pip: `pip install --upgrade pip`

**Import error after installation**
- Check Python path: `python -c "import sys; print(sys.path)"`
- Reinstall: `pip uninstall glyphh && pip install glyphh`

### Runtime Installation Issues

**Docker pull fails**
- Check Docker is running: `docker info`
- Authenticate to GitHub Container Registry if needed

**Database connection error**
- Ensure PostgreSQL is running
- Check DATABASE_URL environment variable
- Verify pgvector extension is installed

## Next Steps

- [Getting Started](getting-started.md) - Build your first model
- [SDK Reference](sdk-reference.md) - Complete API documentation
- [Runtime Deployment](runtime-deployment.md) - Production deployment
