#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Integration for Gospel Guide
Provides high-quality voice synthesis for CFM audio summaries
"""

import os
import base64
import io
import logging
from typing import Optional, List, Dict, Any
from elevenlabs import ElevenLabs, Voice, VoiceSettings

logger = logging.getLogger(__name__)

class ElevenLabsTTS:
    """ElevenLabs Text-to-Speech service for generating high-quality audio"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize ElevenLabs client"""
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required")
        
        self.client = ElevenLabs(api_key=self.api_key)
        self.max_chunk_length = 2500  # ElevenLabs character limit per request
        
        # Voice mapping for gospel content - professional, warm voices
        self.voice_options = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",  # Clear, professional female
            "drew": "29vD33N1CtxCmqQRPOHJ",   # Warm, authoritative male  
            "paul": "5Q0t7uMcjvnagumLfvZi",   # Deep, resonant male
            "antoni": "ErXwobaYiN019PkySvjV",  # Smooth, engaging male
            "bella": "EXAVITQu4vr4xnSDxMaL",  # Gentle, nurturing female
        }
        
        # Default voice for gospel content
        self.default_voice = "rachel"
    
    def get_available_voices(self) -> Dict[str, str]:
        """Get available voice options for gospel content"""
        try:
            voices = self.client.voices.get_all()
            available = {}
            
            for voice_id, voice_name in self.voice_options.items():
                # Verify voice exists
                try:
                    voice_info = next((v for v in voices.voices if v.voice_id == voice_name), None)
                    if voice_info:
                        available[voice_id] = {
                            "id": voice_name,
                            "name": voice_info.name,
                            "description": f"{voice_info.name} - {voice_info.category}"
                        }
                except Exception as e:
                    logger.warning(f"Voice {voice_id} not available: {e}")
            
            return available
            
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            return {}
    
    def chunk_text_smartly(self, text: str, max_length: int = None) -> List[str]:
        """
        Split text into chunks that respect sentence boundaries
        Similar to OpenAI TTS chunking but optimized for ElevenLabs
        """
        if max_length is None:
            max_length = self.max_chunk_length
            
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences first
        sentences = text.replace('\n\n', ' ¶ ').split('. ')
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Add period back except for last sentence
            if i < len(sentences) - 1 and not sentence.endswith(('!', '?', '¶')):
                sentence += '.'
                
            # Replace paragraph markers
            sentence = sentence.replace(' ¶ ', '\n\n')
            
            # Check if adding this sentence would exceed limit
            if current_chunk and len(current_chunk + ' ' + sentence) > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (' ' + sentence if current_chunk else sentence)
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        logger.info(f"Split text into {len(chunks)} chunks for ElevenLabs")
        return chunks
    
    def generate_audio(
        self, 
        text: str, 
        voice: Optional[str] = None,
        voice_settings: Optional[Dict[str, float]] = None
    ) -> Optional[bytes]:
        """
        Generate audio from text using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            voice: Voice ID or name to use
            voice_settings: Voice stability, clarity, style settings
            
        Returns:
            Audio bytes in MP3 format or None if failed
        """
        try:
            # Get voice ID
            voice_id = self.get_voice_id(voice)
            if not voice_id:
                logger.error(f"Invalid voice: {voice}")
                return None
            
            # Handle text chunking for long content
            chunks = self.chunk_text_smartly(text)
            audio_segments = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating audio for chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
                
                try:
                    # Generate audio for this chunk using the correct API
                    audio = self.client.text_to_speech.convert(
                        voice_id=voice_id,
                        text=chunk,
                        voice_settings=VoiceSettings(
                            stability=voice_settings.get("stability", 0.75) if voice_settings else 0.75,
                            similarity_boost=voice_settings.get("similarity_boost", 0.75) if voice_settings else 0.75,
                            style=voice_settings.get("style", 0.0) if voice_settings else 0.0,
                            use_speaker_boost=voice_settings.get("use_speaker_boost", True) if voice_settings else True
                        ),
                        model_id="eleven_monolingual_v1"  # High quality model
                    )
                    
                    # Convert generator to bytes
                    audio_bytes = b''.join(audio)
                    audio_segments.append(audio_bytes)
                    
                except Exception as e:
                    logger.error(f"Failed to generate audio for chunk {i+1}: {e}")
                    return None
            
            # Combine audio segments
            if len(audio_segments) == 1:
                combined_audio = audio_segments[0]
            else:
                # Simple concatenation for MP3 segments
                combined_audio = b''.join(audio_segments)
            
            logger.info(f"Successfully generated {len(combined_audio)} bytes of audio")
            return combined_audio
            
        except Exception as e:
            logger.error(f"ElevenLabs audio generation failed: {e}")
            return None
    
    def get_voice_id(self, voice: Optional[str]) -> Optional[str]:
        """Get ElevenLabs voice ID from voice name"""
        if not voice:
            voice = self.default_voice
        
        # Check if it's already a voice ID (starts with alphanumeric)
        if voice and len(voice) > 15 and voice.replace('_', '').replace('-', '').isalnum():
            return voice
        
        # Map friendly name to voice ID
        return self.voice_options.get(voice.lower(), self.voice_options[self.default_voice])
    
    def generate_audio_base64(
        self, 
        text: str, 
        voice: Optional[str] = None,
        voice_settings: Optional[Dict[str, float]] = None
    ) -> Optional[str]:
        """Generate audio and return as base64 string for API responses"""
        audio_bytes = self.generate_audio(text, voice, voice_settings)
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
        return None
    
    def test_connection(self) -> bool:
        """Test ElevenLabs API connection"""
        try:
            voices = self.client.voices.get_all()
            logger.info(f"ElevenLabs connection successful. Found {len(voices.voices)} voices.")
            return True
        except Exception as e:
            logger.error(f"ElevenLabs connection failed: {e}")
            return False

# Factory function for easy initialization
def create_elevenlabs_client(api_key: Optional[str] = None) -> Optional[ElevenLabsTTS]:
    """Create ElevenLabs TTS client if API key is available"""
    try:
        return ElevenLabsTTS(api_key)
    except Exception as e:
        logger.warning(f"ElevenLabs TTS not available: {e}")
        return None