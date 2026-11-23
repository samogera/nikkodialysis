"""Legal page content for the Nikko Dialysis Center site (Privacy, Terms, Cookies, Accessibility).
Plain-language drafts based on Kenya's Data Protection Act, 2019. Have a Kenyan advocate review before launch."""

LEGAL_NAV = [("privacy", "Privacy policy"), ("terms", "Terms of use"), ("cookies", "Cookie policy"), ("accessibility", "Accessibility")]


def privacy(C):
    e = C["email"]
    return ("Privacy policy", "How we collect, use and protect your personal information, and the rights you have under Kenya's Data Protection Act, 2019.", [
        ("who", "Who we are", f"""<p>{C['name']} ("we", "us") runs an outpatient haemodialysis centre at {C['street']}, {C['area']}, Nairobi, Kenya. We are the <strong>data controller</strong> for personal data collected through this website and when you contact us.</p>
<p>Questions about this policy or your data: <a href="mailto:{e}">{e}</a> or <a href="tel:{C['phone_tel']}">{C['phone_display']}</a>.</p>"""),
        ("scope", "What this policy covers", """<p>This policy covers information you give us through this website (booking requests, email sign-ups), and when you call, WhatsApp or email us. Medical records created during your treatment are covered by our separate patient confidentiality notice, which you receive at your first visit.</p>"""),
        ("collect", "Information we collect", """<ul>
<li><strong>Contact details:</strong> name, phone number, email address (optional).</li>
<li><strong>Request details:</strong> the services you ask about, who the request is for, preferred shift, contact method and time, travel dates, your current dialysis unit and any message you write.</li>
<li><strong>Consent records:</strong> the date, time and wording of the consent you gave.</li>
<li><strong>Technical data:</strong> basic information your browser sends (such as device type and time zone). If you accept analytics, anonymous usage statistics; we do not use advertising trackers.</li>
</ul>
<p>We do not ask you to upload medical records through this website. Please don't include detailed medical information in the message box.</p>"""),
        ("health", "Health information", """<p>Information about your health is <strong>sensitive personal data</strong> under the Act. We only process it with your explicit consent (given on our booking form) or where it is necessary to provide your care, and it is handled by staff bound by professional confidentiality.</p>"""),
        ("use", "How and why we use it", """<div class="table"><div><span>Purpose</span><span>What we do</span><span>Legal basis</span></div>
<div><span>Respond to requests</span><span>Call, WhatsApp or email you about your enquiry and arrange a consultation, transfer, tour or holiday sessions</span><span>Your consent</span></div>
<div><span>Check your cover</span><span>Verify SHA eligibility and request insurer pre-authorisation</span><span>Your consent; steps before providing care</span></div>
<div><span>Provide care</span><span>Plan and deliver treatment once you become a patient</span><span>Provision of health care; legal obligations</span></div>
<div><span>Patient tips</span><span>Send occasional education emails, only if you opt in</span><span>Your consent (withdraw any time)</span></div>
<div><span>Improve the site</span><span>Anonymous analytics and error reports, only if you accept</span><span>Your consent</span></div>
<div><span>Keep the site safe</span><span>Spam and abuse protection, security logs</span><span>Legitimate interests</span></div></div>"""),
        ("share", "Who we share it with", """<p>We never sell your data or share it for advertising. We share only what is needed with:</p>
<ul><li>The <strong>Social Health Authority</strong> and your <strong>insurer</strong>, to verify cover, with your consent.</li>
<li>Your <strong>referring doctor</strong> or <strong>home dialysis unit</strong>, for transfers and holiday sessions.</li>
<li><strong>Service providers</strong> who process data on our behalf under written agreements: website hosting (Vercel), email delivery (Resend) and, if you consent, analytics (Plausible) and error monitoring (Sentry).</li>
<li>Authorities, where the law requires it.</li></ul>"""),
        ("transfers", "Transfers outside Kenya", """<p>Some of our service providers store data outside Kenya. Where this happens we rely on appropriate safeguards required by the Data Protection Act, 2019 and its regulations, such as contractual protections and providers with recognised security standards.</p>"""),
        ("retention", "How long we keep it", """<div class="table"><div><span>Data</span><span>Kept for</span><span>Then</span></div>
<div><span>Enquiries that don't lead to care</span><span>12 months</span><span>Deleted</span></div>
<div><span>Email sign-ups</span><span>Until you unsubscribe</span><span>Deleted within 30 days</span></div>
<div><span>Patient records</span><span>As required by Kenyan health regulations</span><span>Securely destroyed</span></div>
<div><span>Analytics</span><span>Aggregated, no personal identifiers</span><span>N/A</span></div></div>"""),
        ("security", "How we protect it", """<p>The site is served only over HTTPS. Enquiries are sent to a restricted mailbox and accessed only by staff who need them. We use strong passwords and two-factor authentication on our accounts, keep backups, and train staff on confidentiality. If a breach is likely to put you at risk, we will notify the Data Commissioner and you as the Act requires.</p>"""),
        ("rights", "Your rights", f"""<p>Under section 26 of the Data Protection Act, 2019 you have the right to:</p>
<ul><li>be informed of how your data is used;</li><li>access the personal data we hold about you;</li><li>object to the processing of all or part of your data;</li><li>correct false or misleading data;</li><li>delete false, misleading or no-longer-needed data;</li><li>withdraw consent at any time (this doesn't affect processing already done);</li><li>ask for your data in a portable format, where applicable.</li></ul>
<p>To use any right, email <a href="mailto:{e}">{e}</a> or ask at reception. We may ask you to confirm your identity, and we aim to respond within 14 days. There is no charge in most cases.</p>
<p>If you are in the EU or UK, you have equivalent rights under the GDPR.</p>"""),
        ("children", "Children", """<p>Requests about a patient under 18 should be made by a parent or guardian. We do not knowingly collect data directly from children through this website.</p>"""),
        ("complaints", "Complaints", """<p>Please contact us first so we can put things right. You can also complain to the <strong>Office of the Data Protection Commissioner</strong>: <a href="https://www.odpc.go.ke" rel="noopener" target="_blank">odpc.go.ke</a>.</p>"""),
        ("changes", "Changes to this policy", """<p>We may update this policy. The date at the top shows the latest version. Significant changes will be highlighted on this page.</p>"""),
    ])


def terms(C):
    e = C["email"]
    return ("Terms of use", "The rules for using this website. By using it, you agree to these terms.", [
        ("about", "About this website", f"""<p>This website is operated by {C['name']}, {C['street']}, {C['area']}, Nairobi, Kenya. It gives general information about our dialysis services and lets you send us a booking request.</p>"""),
        ("medical", "Not medical advice", """<p>Information on this website is general and for information only. It does not replace advice from your doctor or care team, and it does not create a doctor–patient relationship. Always follow the advice of your own clinicians about your treatment, diet and fluids.</p>"""),
        ("emergency", "Not for emergencies", """<p>Do not use this website, our forms, email or WhatsApp in an emergency. Go to the nearest hospital emergency department or call <strong>999</strong> or <strong>112</strong>.</p>"""),
        ("bookings", "Booking requests", """<p>A request sent through this website is <strong>not a confirmed appointment</strong>. A session is confirmed only when a member of our team contacts you and agrees a date and time. Availability depends on chair capacity and clinical suitability.</p>
<p>For holiday dialysis we need the clinical information listed on our Services page before we can confirm sessions.</p>"""),
        ("fees", "Fees, insurance and payment", """<p>Prices, insurance arrangements and SHA benefits can change. We confirm what is covered and any amount you need to pay <strong>in writing before treatment</strong>. Listing an insurer on this site means we generally accept that insurer; your cover depends on your individual plan and approval.</p>
<p>We accept M-Pesa, Airtel Money, bank transfer and cash, and issue a receipt for every payment.</p>"""),
        ("conduct", "Using the site properly", """<p>Please don't misuse the site: for example, by sending false or spam requests, trying to access systems you're not allowed to, or interfering with the site's security or performance. We may block requests that look automated or abusive.</p>"""),
        ("ip", "Content and trademarks", """<p>Text, design, photos and the Nikko logo belong to Nikko Dialysis Center or are used with permission. You may share links to our pages; please don't copy content for commercial use without our permission.</p>
<p>Insurer and payment logos are trademarks of their owners and are shown only to indicate accepted cover or payment methods.</p>"""),
        ("links", "Links to other websites", """<p>We may link to other sites, such as the Office of the Data Protection Commissioner or map services. We are not responsible for their content or privacy practices.</p>"""),
        ("accuracy", "Accuracy and availability", """<p>We work to keep this site accurate and available, but we cannot guarantee it is always complete, current or uninterrupted. Please confirm important details, such as opening hours, with us directly.</p>"""),
        ("liability", "Liability", """<p>To the extent allowed by Kenyan law, we are not liable for loss arising from reliance on general information on this website. Nothing in these terms limits liability that cannot be limited by law, including for negligence in the care we provide.</p>"""),
        ("privacy", "Privacy", """<p>Our <a href="/privacy">privacy policy</a> and <a href="/cookies">cookie policy</a> explain how we handle your information.</p>"""),
        ("law", "Governing law", """<p>These terms are governed by the laws of Kenya, and the courts of Kenya have jurisdiction over any dispute.</p>"""),
        ("contact", "Contact", f"""<p>Questions about these terms: <a href="mailto:{e}">{e}</a>.</p>"""),
    ])


def cookies(C):
    return ("Cookie policy", "What we store in your browser, why, and how to change your choice.", [
        ("what", "What are cookies?", """<p>Cookies and similar technologies (like local storage) are small pieces of data a website saves in your browser. Some are essential for a site to work; others help the owner understand how the site is used.</p>"""),
        ("ours", "What we use", """<div class="table"><div><span>Name</span><span>Purpose</span><span>Type · duration</span></div>
<div><span>nikko-consent</span><span>Remembers whether you chose "Accept all" or "Essential only"</span><span>Essential · until cleared</span></div>
<div><span>nikko-checklist</span><span>Remembers the items you ticked on the first-session checklist (stays on your device)</span><span>Essential · until cleared</span></div>
<div><span>Plausible Analytics</span><span>Anonymous page-view statistics. Uses no cookies and collects no personal data</span><span>Analytics · only if accepted</span></div>
<div><span>Sentry</span><span>Reports technical errors so we can fix them</span><span>Analytics · only if accepted</span></div></div>
<p>We do not use advertising or social-media tracking cookies. The embedded map (if shown) is provided by Google and may set its own cookies; see Google's privacy policy.</p>"""),
        ("choice", "Your choice", """<p>Analytics and error tracking load <strong>only after</strong> you choose "Accept all" in the cookie notice. You can change your mind at any time:</p>
<p><button class="btn btn-dark btn-sm" type="button" data-cookie-settings>Change cookie settings</button></p>
<p>You can also clear or block cookies and site data in your browser settings. Blocking essential storage may stop some features (like remembering your choice) from working.</p>"""),
        ("changes", "Changes", """<p>If we add new tools, we will update this page and ask for your consent again where needed.</p>"""),
    ])


def accessibility(C):
    e = C["email"]
    return ("Accessibility", "We want everyone, including people with visual, hearing, motor or cognitive impairments, to be able to use this site and our centre.", [
        ("standard", "Our standard", """<p>We aim to meet the <strong>Web Content Accessibility Guidelines (WCAG) 2.2, level AA</strong>.</p>"""),
        ("features", "What we've done", """<ul><li>Text is at least 16px, with colour contrast of 4.5:1 or more.</li><li>The whole site works with a keyboard, with visible focus outlines and a "Skip to content" link.</li><li>Images have text descriptions; decorative graphics are hidden from screen readers.</li><li>Forms have clear labels, error messages and large tap targets (at least 44px).</li><li>Animations switch off if your device is set to reduce motion.</li><li>Pages work on small screens and when zoomed to 200%.</li></ul>"""),
        ("limits", "Known limitations", """<p>Some downloadable guides may not yet be fully accessible. If you need any information in another format, such as large print or read aloud by phone, ask us and we'll provide it.</p>"""),
        ("visit", "Visiting the centre", f"""<p>Please call us on <a href="tel:{C['phone_tel']}">{C['phone_display']}</a> before your first visit if you need help with access, mobility or communication, so we can prepare.</p>"""),
        ("feedback", "Feedback", f"""<p>If something on this site is hard to use, tell us at <a href="mailto:{e}">{e}</a>. We aim to respond within 5 working days.</p>"""),
    ])
