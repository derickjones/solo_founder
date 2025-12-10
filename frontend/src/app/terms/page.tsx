'use client';

import Link from 'next/link';

export default function TermsOfUse() {
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
          <h1 className="text-3xl font-bold text-white">Terms of Use</h1>
          <p className="text-neutral-400 mt-2">Effective Date: December 3, 2025</p>
        </div>

        <div className="prose prose-invert prose-blue max-w-none">
          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">1. Acceptance of Terms</h2>
            <p className="text-neutral-300 mb-4">
              By accessing and using the Gospel Study Assistant ("Service"), you accept and agree to be bound by the terms and provision of this agreement.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">2. Purpose and Scope</h2>
            <p className="text-neutral-300 mb-4">
              The Gospel Study Assistant is designed to help users study and explore the scriptures and teachings of The Church of Jesus Christ of Latter-day Saints. This service provides AI-powered search and question-answering capabilities for educational and spiritual study purposes.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">3. Content Sources and Fair Use</h2>
            <div className="text-neutral-300 mb-4 space-y-4">
              <p>This service provides AI-powered search and study tools that reference content from:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>The Holy Scriptures (Book of Mormon, Bible, Doctrine & Covenants, Pearl of Great Price)</li>
                <li>General Conference talks and addresses</li>
                <li>Come Follow Me curriculum and study guides</li>
                <li>Other publicly available Church materials</li>
              </ul>
              
              <div className="bg-neutral-800 border-l-4 border-blue-500 p-4 my-6">
                <h3 className="font-semibold text-white mb-2">Fair Use Declaration</h3>
                <p className="text-sm">
                  This service operates under fair use principles (17 U.S.C. § 107) as a transformative tool that 
                  provides search, analysis, and study assistance. We do not reproduce substantial portions of 
                  copyrighted materials, but rather provide AI-powered search and contextual assistance for study purposes.
                </p>
              </div>

              <p>
                <strong>Transformative Nature:</strong> Our service transforms how users interact with religious texts 
                by providing AI-powered search, question-answering, and study assistance tools. The service does not 
                substitute for original materials but enhances study through technological assistance.
              </p>

              <p>
                <strong>No Endorsement:</strong> This service is independently operated and is not affiliated with, 
                endorsed by, or sponsored by The Church of Jesus Christ of Latter-day Saints. All Church-produced 
                content remains the property of The Church of Jesus Christ of Latter-day Saints.
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">4. Service Model and Licensing</h2>
            <div className="text-neutral-300 mb-4 space-y-4">
              <p>
                <strong>Technology Service:</strong> Users pay for access to AI-powered search technology, user interface, 
                hosting, and computational resources - not for the underlying religious content itself, which remains 
                freely available through official Church channels.
              </p>
              
              <p>
                <strong>Respect for Original Sources:</strong> We encourage users to access original materials directly 
                through official Church websites and publications. This service is designed to supplement, not replace, 
                direct scripture study and official Church resources.
              </p>
              
              <p>
                <strong>Content Limitations:</strong> Our service provides search results, contextual assistance, and study tools. 
                For complete texts, official interpretations, and authoritative doctrine, users should consult original sources.
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">5. AI-Generated Responses</h2>
            <p className="text-neutral-300 mb-4">
              Responses provided by this service are generated by artificial intelligence and should be used for study and reflection purposes. While we strive for accuracy, AI responses may not always reflect official Church doctrine or teachings. For authoritative guidance, please consult:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-neutral-300 mb-4">
              <li>Official Church websites and publications</li>
              <li>Local Church leaders</li>
              <li>The scriptures themselves</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">6. User Responsibilities</h2>
            <p className="text-neutral-300 mb-4">Users agree to:</p>
            <ul className="list-disc pl-6 space-y-2 text-neutral-300 mb-4">
              <li>Use the service for lawful and appropriate purposes</li>
              <li>Not attempt to compromise the security or functionality of the service</li>
              <li>Respect the religious nature and intent of the content</li>
              <li>Not use the service to republish or redistribute substantial portions of copyrighted materials</li>
              <li>Acknowledge that original content remains the property of The Church of Jesus Christ of Latter-day Saints</li>
              <li>Consult original sources for authoritative doctrine and complete texts</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">7. Privacy and Data</h2>
            <p className="text-neutral-300 mb-4">
              We are committed to protecting your privacy. Questions and interactions with the service may be logged for improvement purposes. We do not sell personal information or share it with third parties except as necessary to provide the service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">8. Disclaimer of Warranties</h2>
            <p className="text-neutral-300 mb-4">
              This service is provided "as is" without warranties of any kind. We make no representations about the accuracy, completeness, or reliability of the AI-generated responses or the availability of the service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">9. Limitation of Liability</h2>
            <p className="text-neutral-300 mb-4">
              The creators and operators of this service shall not be liable for any direct, indirect, incidental, special, or consequential damages resulting from the use or inability to use the service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">10. Changes to Terms</h2>
            <p className="text-neutral-300 mb-4">
              We reserve the right to modify these terms at any time. Continued use of the service after changes constitutes acceptance of the new terms.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">11. Contact Information</h2>
            <p className="text-neutral-300 mb-4">
              For questions about these terms or the service, please contact us through the appropriate channels provided on our website.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">12. Copyright Notice</h2>
            <div className="text-neutral-300 mb-4 space-y-3">
              <p className="font-medium">© 2025 Gospel Study Assistant • AI-powered gospel study</p>
              <p className="text-sm">
                This service provides AI-powered search and study tools. Content from The Church of Jesus Christ 
                of Latter-day Saints remains their property and is referenced under fair use principles for 
                educational and spiritual study purposes.
              </p>
              <p className="text-sm text-neutral-400">
                The Gospel Study Assistant is an independent service and is not affiliated with, 
                endorsed by, or sponsored by The Church of Jesus Christ of Latter-day Saints.
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}