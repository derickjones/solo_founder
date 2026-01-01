'use client';

import { SignUp } from '@clerk/nextjs'

export default function Page() {
  return (
    <div className="min-h-screen bg-neutral-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Get Started</h1>
          <p className="text-neutral-400">Create your Gospel Study App account</p>
        </div>
        
        <div className="flex justify-center">
          <SignUp 
            appearance={{
              elements: {
                rootBox: "mx-auto",
                card: "bg-neutral-800 border border-neutral-700",
                headerTitle: "text-white",
                headerSubtitle: "text-neutral-400",
                socialButtonsBlockButton: "bg-neutral-700 border-neutral-600 text-white hover:bg-neutral-600",
                formButtonPrimary: "bg-blue-600 hover:bg-blue-700 text-white",
                formFieldInput: "bg-neutral-700 border-neutral-600 text-white",
                identityPreviewText: "text-white",
                identityPreviewEditButton: "text-blue-400"
              }
            }}
          />
        </div>
      </div>
    </div>
  )
}