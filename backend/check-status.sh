#!/bin/bash
# Check deployment status and health of Gospel Guide API

PROJECT_ID="gospel-study-474301"
SERVICE_NAME="gospel-guide-api"
REGION="us-central1"

echo "🔍 Gospel Guide API Status Check"
echo "================================"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --format='value(status.url)' 2>/dev/null)

if [ -z "$SERVICE_URL" ]; then
    echo "❌ Service not found or not deployed"
    echo "Run: ./deploy.sh to deploy the service"
    exit 1
fi

echo "🌐 Service URL: $SERVICE_URL"
echo ""

# Check service status
echo "📊 Service Status:"
gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --format='table(status.conditions[0].type, status.conditions[0].status, status.conditions[0].reason)'

echo ""

# Test health endpoint
echo "🩺 Health Check:"
if curl -f -s "$SERVICE_URL/health" --max-time 10 > /tmp/health_response.json; then
    echo "✅ API is healthy!"
    cat /tmp/health_response.json | jq . 2>/dev/null || cat /tmp/health_response.json
    rm -f /tmp/health_response.json
else
    echo "❌ Health check failed"
    echo "Check logs with: gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME\" --limit=10 --project=$PROJECT_ID"
fi

echo ""

# Show recent logs summary
echo "📝 Recent Logs (last 5 entries):"
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" \
    --limit=5 \
    --format='table(timestamp.date(tz=LOCAL), severity, textPayload.extract(first=100))' \
    --project=$PROJECT_ID

echo ""
echo "💡 Quick Commands:"
echo "• Full logs: gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME\" --limit=20 --project=$PROJECT_ID"
echo "• Test streaming: curl -X POST \"$SERVICE_URL/ask/stream\" -H \"Content-Type: application/json\" -d '{\"query\": \"What is faith?\"}'"
echo "• Service details: gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID"