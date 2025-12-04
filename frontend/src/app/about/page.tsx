'use client';

import Link from 'next/link';

export default function About() {
  return (
    <div className="min-h-screen bg-neutral-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <Link 
            href="/" 
            className="inline-flex items-center text-blue-400 hover:text-blue-300 mb-4"
          >
            ← Back to Gospel Study Assistant
          </Link>
          <h1 className="text-3xl font-bold text-white">About Gospel Study Assistant</h1>
          <p className="text-neutral-400 mt-2">AI-powered scripture study and gospel learning</p>
        </div>

        <div className="prose prose-invert prose-blue max-w-none">
          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Our Mission</h2>
            <p className="text-neutral-300 mb-4">
              The Gospel Study Assistant is designed to enhance personal and family scripture study by providing intelligent, searchable access to the vast library of Church teachings and scriptures. Our goal is to help members of The Church of Jesus Christ of Latter-day Saints deepen their understanding of gospel principles through AI-powered study tools.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">What We Offer</h2>
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div className="bg-neutral-800 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">Scripture Search</h3>
                <p className="text-neutral-300">
                  Comprehensive search across all standard works including the Book of Mormon, Bible, Doctrine & Covenants, and Pearl of Great Price.
                </p>
              </div>
              <div className="bg-neutral-800 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">General Conference</h3>
                <p className="text-neutral-300">
                  Access to decades of General Conference talks from Church leaders, searchable by speaker, topic, and time period.
                </p>
              </div>
              <div className="bg-neutral-800 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">AI-Powered Q&A</h3>
                <p className="text-neutral-300">
                  Ask questions in natural language and receive thoughtful responses based on Church teachings and scriptures.
                </p>
              </div>
              <div className="bg-neutral-800 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">Study Modes</h3>
                <p className="text-neutral-300">
                  Specialized study modes for different needs including youth, scholars, and Come Follow Me curriculum.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">How It Works</h2>
            <div className="space-y-4 text-neutral-300">
              <div className="flex items-start space-x-4">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-semibold text-sm">1</div>
                <div>
                  <h4 className="font-semibold text-white">Ask Your Question</h4>
                  <p>Type any gospel-related question in natural language.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-semibold text-sm">2</div>
                <div>
                  <h4 className="font-semibold text-white">AI Searches</h4>
                  <p>Our AI searches through scriptures, conference talks, and Church materials.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-semibold text-sm">3</div>
                <div>
                  <h4 className="font-semibold text-white">Get Insights</h4>
                  <p>Receive relevant answers with source citations and links to original materials.</p>
                </div>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Content Sources</h2>
            <p className="text-neutral-300 mb-4">
              All content is sourced from official Church publications and materials:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-neutral-300 mb-4">
              <li><strong>Standard Works:</strong> Book of Mormon, Bible, Doctrine & Covenants, Pearl of Great Price</li>
              <li><strong>General Conference:</strong> Talks from 2015-2025 by General Authorities and officers</li>
              <li><strong>Come Follow Me:</strong> Official curriculum materials and study guides</li>
              <li><strong>Church Publications:</strong> Official Church-approved educational materials</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Important Notes</h2>
            <div className="bg-yellow-900 bg-opacity-30 border border-yellow-600 rounded-lg p-6">
              <p className="text-yellow-200 mb-4">
                <strong>Disclaimer:</strong> While this tool provides AI-generated responses based on Church materials, it is not an official Church application. For authoritative doctrine and guidance, please consult:
              </p>
              <ul className="list-disc pl-6 space-y-1 text-yellow-200">
                <li>The scriptures themselves</li>
                <li>Official Church websites (churchofjesuschrist.org)</li>
                <li>Local Church leaders and teachers</li>
                <li>Current Church publications and manuals</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Technology</h2>
            <p className="text-neutral-300 mb-4">
              This application uses advanced AI and machine learning technologies to provide semantic search and natural language understanding. The system is continuously updated to improve accuracy and relevance of responses.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Feedback and Support</h2>
            <p className="text-neutral-300 mb-4">
              We're committed to continuous improvement. If you encounter issues, have suggestions, or would like to provide feedback, please reach out through the appropriate channels. Your input helps us make this tool more valuable for gospel study.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Version Information</h2>
            <div className="bg-neutral-800 p-4 rounded-lg">
              <p className="text-neutral-300">
                <strong>Current Version:</strong> 1.0<br/>
                <strong>Last Updated:</strong> December 2025<br/>
                <strong>Content Through:</strong> December 2025
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}