"""
Google Cloud Text-to-Speech (TTS) Service using Vertex AI Chirp 3 HD Voices

This module provides high-quality, cost-effective text-to-speech conversion
using Google Cloud's Vertex AI with Chirp 3 HD voices.

Pricing: ~$0.016/1000 characters (vs ElevenLabs $0.30/1000)
Quality: Excellent with Chirp 3 HD voices
"""

import os
import logging
import base64
from typing import Optional, Dict
from google.cloud import texttospeech_v1 as texttospeech

logger = logging.getLogger(__name__)


class GoogleCloudTTS:
    """Google Cloud Text-to-Speech client using Chirp 3 HD voices"""
    
    # Chirp 3 HD voice options - high quality voices
    # Format: voice_name -> (language_code, voice_name)
    VOICE_OPTIONS = {
        # Male voices
        "algieba": ("en-US", "en-US-Chirp3-HD-Algieba"),
        "charon": ("en-US", "en-US-Chirp3-HD-Charon"),
        "fenrir": ("en-US", "en-US-Chirp3-HD-Fenrir"),
        "orus": ("en-US", "en-US-Chirp3-HD-Orus"),
        "puck": ("en-US", "en-US-Chirp3-HD-Puck"),
        # Female voices
        "aoede": ("en-US", "en-US-Chirp3-HD-Aoede"),
        "kore": ("en-US", "en-US-Chirp3-HD-Kore"),
        "leda": ("en-US", "en-US-Chirp3-HD-Leda"),
        "zephyr": ("en-US", "en-US-Chirp3-HD-Zephyr"),
        # Default for CFM - warm, authoritative male voice
        "cfm_male": ("en-US", "en-US-Chirp3-HD-Algieba"),
    }
    
    def __init__(self):
        """Initialize Google Cloud TTS client"""
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.default_voice = "cfm_male"
            logger.info("✅ Google Cloud TTS client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud TTS client: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if Google Cloud TTS is accessible"""
        try:
            # List available voices to verify connection
            request = texttospeech.ListVoicesRequest(language_code="en-US")
            response = self.client.list_voices(request=request)
            voice_count = len(response.voices)
            logger.info(f"✅ Google Cloud TTS connection successful - {voice_count} voices available")
            return True
        except Exception as e:
            logger.error(f"❌ Google Cloud TTS connection failed: {e}")
            return False
    
    def get_voice_config(self, voice: Optional[str] = None) -> tuple:
        """Get voice configuration (language_code, voice_name)"""
        voice_key = (voice or self.default_voice).lower()
        
        if voice_key in self.VOICE_OPTIONS:
            return self.VOICE_OPTIONS[voice_key]
        
        # Default to cfm_male if voice not found
        logger.warning(f"Voice '{voice}' not found, using default cfm_male")
        return self.VOICE_OPTIONS["cfm_male"]
    
    def chunk_text_smartly(self, text: str, max_length: int = 4500) -> list:
        """
        Split text into chunks that respect sentence boundaries.
        Google Cloud TTS has a 5000 byte limit per request.
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences
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
        
        logger.info(f"Split text into {len(chunks)} chunks for Google Cloud TTS")
        return chunks
    
    def generate_audio(
        self,
        text: str,
        voice: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[bytes]:
        """
        Generate audio from text using Google Cloud TTS
        
        Args:
            text: Text to convert to speech
            voice: Voice name to use (see VOICE_OPTIONS)
            speaking_rate: Speed of speech (0.25 to 4.0, default 1.0)
            pitch: Voice pitch adjustment (-20.0 to 20.0, default 0.0)
            
        Returns:
            Audio bytes in MP3 format or None if failed
        """
        try:
            language_code, voice_name = self.get_voice_config(voice)
            
            # Handle text chunking for long content
            chunks = self.chunk_text_smartly(text)
            audio_segments = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating audio for chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
                
                try:
                    # Set up synthesis input
                    synthesis_input = texttospeech.SynthesisInput(text=chunk)
                    
                    # Configure voice
                    voice_config = texttospeech.VoiceSelectionParams(
                        language_code=language_code,
                        name=voice_name
                    )
                    
                    # Configure audio output
                    audio_config = texttospeech.AudioConfig(
                        audio_encoding=texttospeech.AudioEncoding.MP3,
                        speaking_rate=speaking_rate,
                        pitch=pitch
                    )
                    
                    # Generate speech
                    response = self.client.synthesize_speech(
                        input=synthesis_input,
                        voice=voice_config,
                        audio_config=audio_config
                    )
                    
                    audio_segments.append(response.audio_content)
                    
                except Exception as e:
                    logger.error(f"Failed to generate audio for chunk {i+1}: {e}")
                    return None
            
            # Combine audio segments
            if len(audio_segments) == 1:
                combined_audio = audio_segments[0]
            else:
                # Simple concatenation for MP3 segments
                combined_audio = b''.join(audio_segments)
            
            logger.info(f"✅ Successfully generated {len(combined_audio)} bytes of audio")
            return combined_audio
            
        except Exception as e:
            logger.error(f"Google Cloud TTS audio generation failed: {e}")
            return None
    
    def generate_audio_base64(
        self,
        text: str,
        voice: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[str]:
        """Generate audio and return as base64 string for API responses"""
        audio_bytes = self.generate_audio(text, voice, speaking_rate, pitch)
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
        return None
    
    def list_available_voices(self) -> list:
        """List all available Chirp 3 HD voices"""
        return list(self.VOICE_OPTIONS.keys())


def create_google_tts_client() -> Optional[GoogleCloudTTS]:
    """
    Factory function to create Google Cloud TTS client
    
    Returns:
        GoogleCloudTTS instance or None if initialization fails
    """
    try:
        client = GoogleCloudTTS()
        if client.test_connection():
            return client
        return None
    except Exception as e:
        logger.error(f"Failed to create Google Cloud TTS client: {e}")
        return None
