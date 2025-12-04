#!/bin/bash
# Deploy Gospel Guide Search API to Google Cloud Run
# Updated version with improved error handling and conflict prevention

set -e

# Configuration
PROJECT_ID="gospel-study-474301"
SERVICE_NAME="gospel-guide-api"
REGION="us-central1"  # Change if you prefer different region
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
BUCKET_NAME="gospel-guide-content-$PROJECT_ID"  # Updated to match actual bucket naming

echo "🚀 Deploying Gospel Guide to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"

# Run pre-deployment checks
echo ""
echo "🔍 Running pre-deployment validation..."
if [ -f "check-deploy.sh" ]; then
    ./check-deploy.sh
else
    echo "⚠️  Pre-check script not found. Proceeding with basic checks..."
    
    # Basic checks
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  Warning: OPENAI_API_KEY environment variable is not set"
        echo "   The service will start successfully but lesson planning features will be unavailable."
        echo "   To enable lesson planning, set the environment variable in Cloud Run after deployment:"
        echo "   gcloud run services update $SERVICE_NAME --region=$REGION --set-env-vars OPENAI_API_KEY='your-api-key-here'"
        echo ""
        echo "🔄 Continuing deployment without OpenAI API key..."
    else
        echo "✅ OpenAI API key is configured"
    fi
fi

# Set active project
echo "📋 Setting active Google Cloud project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage-api.googleapis.com

# Create Cloud Storage bucket for content files
echo "📦 Creating Cloud Storage bucket for content..."
gsutil mb gs://$BUCKET_NAME 2>/dev/null || echo "Bucket already exists"
gsutil versioning set on gs://$BUCKET_NAME

# Upload content files to Cloud Storage
echo "⬆️  Uploading content files to Cloud Storage..."
if [ -d "scripts/content" ]; then
    gsutil -m cp scripts/content/*.json gs://$BUCKET_NAME/content/
    echo "✅ Content files uploaded"
else
    echo "⚠️  No content files found. Run scrapers first: cd scripts && python master_scraper.py"
fi

# Upload search indexes to Cloud Storage  
echo "⬆️  Uploading search indexes to Cloud Storage..."
if [ -d "search/indexes" ]; then
    gsutil -m cp search/indexes/* gs://$BUCKET_NAME/indexes/
    echo "✅ Search indexes uploaded"
else
    echo "⚠️  No search indexes found. Build embeddings first: cd search && python build_embeddings.py"
fi

# Build and submit Docker image
echo "🔨 Building Docker image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Clear any existing env vars and secrets to prevent type conflicts
echo "🧹 Clearing existing environment variables and secrets..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --clear-env-vars \
    --clear-secrets \
    --no-traffic \
    --project $PROJECT_ID

echo "⚙️  Deploying with proper configuration..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --cpu-boost \
    --startup-probe="initialDelaySeconds=120,timeoutSeconds=20,periodSeconds=30,failureThreshold=5,httpGet.port=8080,httpGet.path=/health" \
    --set-env-vars="BUCKET_NAME=$BUCKET_NAME,INDEX_DIR=indexes$(if [ ! -z "$OPENAI_API_KEY" ]; then echo ",OPENAI_API_KEY=$OPENAI_API_KEY"; fi)" \
    --project $PROJECT_ID

# Get service URL
echo "🎉 Deployment complete!"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "Service URL: $SERVICE_URL"
echo ""
echo "✅ Testing API health..."
sleep 10  # Give service time to start
if curl -f -s "$SERVICE_URL/health" > /dev/null; then
    echo "✅ API is healthy and responding!"
else
    echo "⚠️  API health check failed. Check the logs:"
    echo "gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME\" --limit=10 --project=$PROJECT_ID"
fi

echo ""
echo "📋 Test your API:"
echo "curl \"$SERVICE_URL/health\""
echo "curl \"$SERVICE_URL/config\""
echo "curl \"$SERVICE_URL/ask/stream\" -H \"Content-Type: application/json\" -d '{\"query\": \"What is faith?\"}'"
echo ""
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  To enable lesson planning features, set the OpenAI API key:"
    echo "gcloud run services update $SERVICE_NAME --region=$REGION --set-env-vars OPENAI_API_KEY='your-api-key-here'"
    echo ""
fi
echo "🔧 Troubleshooting:"
echo "- View logs: gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME\" --limit=20 --project=$PROJECT_ID"
echo "- Service status: gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID"
echo ""
echo "✨ Next steps:"
echo "1. Test your API endpoints above"
echo "2. Update your frontend API_BASE_URL to: $SERVICE_URL"  
echo "3. Deploy your Next.js frontend"