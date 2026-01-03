# Audio Cache System - Implementation Guide

## 🎯 Overview

The audio cache system provides **on-demand caching** of TTS-generated audio files in Google Cloud Storage, dramatically reducing load times and TTS API costs for repeated requests.

### Key Features
- ✅ **On-demand caching**: Generate once, serve instantly on subsequent requests
- ✅ **Google Cloud Storage**: Persistent, scalable, cost-effective storage
- ✅ **30-day age-based cleanup**: Manual trigger to keep cache fresh
- ✅ **Cache statistics**: Monitor usage and storage
- ✅ **Automatic integration**: Works transparently with existing TTS endpoints

---

## 📊 Performance Impact

### Before Caching:
- **First request**: 30-60 seconds (TTS generation + music mixing)
- **Subsequent requests**: 30-60 seconds (regenerate every time)
- **Cost**: $0.016 per 1000 characters, every request

### After Caching:
- **First request**: 30-60 seconds (TTS generation + upload to cache)
- **Subsequent requests**: 0.5 seconds (download from cache) ⚡
- **Cost**: $0.016 once, then ~$0.01/month storage
- **Savings**: 90%+ cost reduction, 98%+ time reduction

---

## 🗂️ Cache Structure

### Google Cloud Storage Layout:
```
gs://your-bucket/audio-cache/
  
  podcast/
    podcast_{hash}_{voice}.mp3           # Podcast with fixed voices
    
  study_guide/
    study_guide_week_01_essential_alnilam.mp3
    study_guide_week_01_essential_aoede.mp3
    
  lesson_plan/
    lesson_plan_week_01_adult_alnilam.mp3
    lesson_plan_week_01_adult_aoede.mp3
    
  core_content/
    core_content_week_01_alnilam.mp3
    
  daily_thoughts/
    daily_thoughts_week_01_alnilam.mp3
```

---

## 🔧 Cache Management

### 1. Get Cache Statistics

**Endpoint**: `GET /cache/stats`

**Response**:
```json
{
  "total_files": 156,
  "total_size_mb": 78.5,
  "oldest_file_age_days": 28,
  "newest_file_age_days": 0,
  "files_over_30_days": 0,
  "by_type": {
    "podcast": {
      "count": 6,
      "size_mb": 15.0
    },
    "study_guide": {
      "count": 52,
      "size_mb": 26.0
    }
  }
}
```

**Usage**:
```bash
curl https://your-api-url/cache/stats
```

---

### 2. Clean Up Old Files (Recommended Monthly)

**Endpoint**: `DELETE /cache/cleanup?older_than_days=30`

**Response**:
```json
{
  "message": "Cache cleanup complete",
  "deleted_files": 45,
  "freed_mb": 22.5,
  "kept_files": 111,
  "oldest_remaining_age_days": 15,
  "cleanup_threshold_days": 30
}
```

**Usage**:
```bash
# Clean files older than 30 days (default)
curl -X DELETE https://your-api-url/cache/cleanup

# Custom age threshold
curl -X DELETE "https://your-api-url/cache/cleanup?older_than_days=45"
```

**Recommended Schedule**: Run on the 1st of each month to keep cache fresh.

---

### 3. Clear All Cache (Nuclear Option)

**Endpoint**: `DELETE /cache/clear`

**Response**:
```json
{
  "message": "All audio cache cleared",
  "deleted_files": 156,
  "freed_mb": 78.5
}
```

**Usage**:
```bash
curl -X DELETE https://your-api-url/cache/clear
```

**⚠️ Warning**: This deletes ALL cached audio. Use only when:
- Updating TTS voice models
- Changing audio generation logic
- Major backend updates requiring fresh audio

---

## 🔄 How It Works

### Cache Flow Diagram:

```
┌─────────────────────────────────────────┐
│  User requests podcast audio            │
│  (Week 1, Essential, Alnilam/Aoede)    │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Check GCS     │
        │  Cache         │
        └───────┬────────┘
                │
       ┌────────┴────────┐
       │                 │
    Cache               Cache
    HIT ✅              MISS ❌
       │                 │
       ▼                 ▼
  ┌────────┐      ┌──────────────┐
  │Download│      │Generate Audio│
  │from GCS│      │with TTS      │
  │        │      │(30-60 sec)   │
  │0.5 sec │      └──────┬───────┘
  └────┬───┘             │
       │                 ▼
       │          ┌──────────────┐
       │          │Upload to GCS │
       │          │Cache         │
       │          └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌───────────────┐
        │ Return Audio  │
        │ to User       │
        └───────────────┘
```

---

## 💰 Cost Analysis

### Storage Costs (Google Cloud Storage):
- **Price**: $0.020 per GB/month (Standard Storage)
- **Average file size**: ~500KB per audio file
- **Estimate**: 200 cached files = ~100MB = **$0.002/month**

### TTS API Costs (Google Cloud TTS):
- **Without cache**: $0.016 per 1000 characters × every request
- **With cache**: $0.016 per 1000 characters × once (first request only)
- **Savings example**: 
  - 100 users request same podcast
  - Without cache: 100 × $0.016 = $1.60
  - With cache: 1 × $0.016 = **$0.016** (99% savings!)

### Download Costs:
- **Price**: $0.12 per GB egress (North America)
- **Estimate**: 1000 downloads × 500KB = 500MB = **$0.06**

**Total Monthly Cost**: ~$0.07 for 1000 users vs $16+ without caching

---

## 🚀 Deployment

### Environment Variables Required:
```bash
BUCKET_NAME=your-gcs-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### GCS Bucket Setup:
1. Create bucket: `gsutil mb gs://your-bucket-name`
2. Set lifecycle rule (optional):
```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 60,
          "matchesPrefix": ["audio-cache/"]
        }
      }
    ]
  }
}
```

### Service Account Permissions:
- `storage.objects.create`
- `storage.objects.get`
- `storage.objects.delete`
- `storage.objects.list`

---

## 📝 Monthly Maintenance Checklist

### On the 1st of Each Month:

1. **Check Cache Stats**:
```bash
curl https://your-api-url/cache/stats
```

2. **Review Statistics**:
   - How many files are cached?
   - How much storage is used?
   - How many files are over 30 days old?

3. **Clean Up Old Files**:
```bash
curl -X DELETE https://your-api-url/cache/cleanup
```

4. **Verify Results**:
   - Check `deleted_files` count
   - Verify `freed_mb` storage
   - Confirm `oldest_remaining_age_days` is reasonable

---

## 🔍 Troubleshooting

### Cache not working?

1. **Check if cache manager initialized**:
```python
# In logs, look for:
"✅ Audio caching enabled"
"✅ Audio Cache Manager initialized"
```

2. **Verify GCS permissions**:
```bash
gsutil ls gs://your-bucket/audio-cache/
```

3. **Check environment variables**:
```bash
echo $BUCKET_NAME
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### Audio generation slow even with cache?

1. **Check cache hit rate** in logs:
```
"✅ Cache HIT: audio-cache/podcast/..."  # Good!
"❌ Cache MISS: audio-cache/podcast/..." # Generating new
```

2. **Verify cache is being uploaded**:
```
"💾 Cached audio for future requests: ..."
```

### Storage costs increasing?

1. **Check total cached files**:
```bash
curl https://your-api-url/cache/stats
```

2. **Run cleanup more frequently**:
```bash
# Clean files older than 14 days instead of 30
curl -X DELETE "https://your-api-url/cache/cleanup?older_than_days=14"
```

---

## 🎓 Best Practices

1. **Monthly Cleanup**: Always run cleanup on the 1st of each month
2. **Monitor Storage**: Check stats weekly for unusual growth
3. **Version Updates**: Clear all cache when updating TTS voices or audio logic
4. **Backup Strategy**: GCS provides 99.999999999% durability - no additional backup needed
5. **Cost Optimization**: Cache only popular content (current week ± 4 weeks)

---

## 📚 API Reference

### AudioCacheManager Methods

```python
# Check if audio exists in cache
cache_exists = cache_manager.check_cache(cache_key)

# Get cached audio bytes
audio_bytes = cache_manager.get_cached_audio(cache_key)

# Upload audio to cache
success = cache_manager.upload_to_cache(cache_key, audio_bytes)

# Get statistics
stats = cache_manager.get_cache_stats()

# Cleanup old files
result = cache_manager.cleanup_old_files(max_age_days=30)

# Clear all cache
result = cache_manager.clear_all_cache()
```

---

## 🎉 Summary

The audio cache system provides:
- ⚡ **98% faster** audio loading for cached content
- 💰 **90%+ cost savings** on TTS API calls
- 🔒 **Persistent** caching across deployments
- 🌍 **Scalable** to millions of requests
- 🧹 **Easy maintenance** with manual cleanup triggers

**Next Steps**: Deploy, test with a few requests, monitor cache statistics, and set up monthly cleanup schedule!
