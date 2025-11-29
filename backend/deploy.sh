#!/bin/bash
# Deploy Gospel Guide Search API to Google Cloud Run

set -e

# Configuration
PROJECT_ID="gospel-study-474301"
SERVICE_NAME="gospel-guide-api"
REGION="us-central1"  # Change if you prefer different region
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
BUCKET_NAME="gospel-guide-content-$PROJECT_ID"

echo "🚀 Deploying Gospel Guide to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"

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
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars="BUCKET_NAME=$BUCKET_NAME" \
    --set-env-vars="INDEX_DIR=/tmp/indexes" \
    --set-env-vars="OPENAI_API_KEY=$OPENAI_API_KEY"

# Get service URL
echo "🎉 Deployment complete!"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "Service URL: $SERVICE_URL"
echo ""
echo "Test your API:"
echo "curl \"$SERVICE_URL/health\""
echo "curl \"$SERVICE_URL/search?q=What+is+faith?&mode=book-of-mormon-only\""
echo ""
echo "Next steps:"
echo "1. Test your API endpoints"
echo "2. Build your Next.js frontend"  
echo "3. Connect frontend to this API URL"