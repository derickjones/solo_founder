#!/bin/bash
# Pre-deployment validation script for Gospel Guide API

set -e

echo "🔍 Gospel Guide Deployment Pre-Check"
echo "======================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with Google Cloud. Run: gcloud auth login"
    exit 1
fi

# Check project configuration
PROJECT_ID=$(gcloud config get-value project)
if [ "$PROJECT_ID" != "gospel-study-474301" ]; then
    echo "❌ Wrong project configured. Expected: gospel-study-474301, Got: $PROJECT_ID"
    echo "Run: gcloud config set project gospel-study-474301"
    exit 1
fi

# Check if .env file exists and has OPENAI_API_KEY
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Create one with:"
    echo "echo 'OPENAI_API_KEY=your-key-here' > .env"
    exit 1
fi

source .env
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    exit 1
fi

if [[ "$OPENAI_API_KEY" == "your-"* ]]; then
    echo "❌ OPENAI_API_KEY appears to be a placeholder. Set your actual key."
    exit 1
fi

# Check if required APIs are enabled
echo "🔧 Checking required APIs..."
REQUIRED_APIS=(
    "run.googleapis.com"
    "cloudbuild.googleapis.com" 
    "storage-api.googleapis.com"
)

for api in "${REQUIRED_APIS[@]}"; do
    if ! gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        echo "⚠️  Enabling $api..."
        gcloud services enable $api
    fi
done

# Check if Cloud Storage bucket exists
BUCKET_NAME="gospel-guide-content-gospel-study-474301"
if ! gsutil ls -b "gs://$BUCKET_NAME" &> /dev/null; then
    echo "⚠️  Cloud Storage bucket $BUCKET_NAME not found. Creating..."
    gsutil mb "gs://$BUCKET_NAME"
    gsutil versioning set on "gs://$BUCKET_NAME"
fi

# Check if content files exist
if [ ! -d "scripts/content" ] || [ -z "$(ls -A scripts/content)" ]; then
    echo "⚠️  Content files not found. Run scrapers first:"
    echo "cd scripts && python3 master_scraper.py"
fi

# Check if search indexes exist
if [ ! -d "search/indexes" ] || [ -z "$(ls -A search/indexes)" ]; then
    echo "⚠️  Search indexes not found. Build embeddings first:"
    echo "cd search && python3 build_embeddings.py"
fi

echo ""
echo "✅ All pre-deployment checks passed!"
echo "🚀 Ready to deploy. Run: ./deploy.sh"