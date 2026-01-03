'use client';

import Image from 'next/image';

interface VideoLogoProps {
  className?: string;
  size?: 'small' | 'medium' | 'large';
}

export default function VideoLogo({ className = '', size = 'medium' }: VideoLogoProps) {
  const sizeClasses = {
    small: 'w-8 h-8',
    medium: 'w-16 h-16 lg:w-24 lg:h-24',
    large: 'w-20 h-20 lg:w-28 lg:h-28'
  };

  const sizePixels = {
    small: 32,
    medium: 96,
    large: 112
  };

  return (
    <div className={`${sizeClasses[size]} ${className} rounded-xl overflow-hidden ring-2 ring-neutral-700/50 bg-transparent flex items-center justify-center`}>
      <div className="w-full h-full relative">
        <Image
          src="/scripture_study.jpeg"
          alt="Gospel Study App Logo"
          width={sizePixels[size]}
          height={sizePixels[size]}
          className="w-full h-full object-cover"
          priority
        />
      </div>
    </div>
  );
}
