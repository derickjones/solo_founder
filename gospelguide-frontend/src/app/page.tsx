'use client';

import { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [sourceCount, setSourceCount] = useState(5);

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar 
        selectedSources={selectedSources}
        setSelectedSources={setSelectedSources}
        sourceCount={sourceCount}
        setSourceCount={setSourceCount}
      />
      <ChatInterface 
        selectedSources={selectedSources}
        sourceCount={sourceCount}
      />
    </div>
  );
}