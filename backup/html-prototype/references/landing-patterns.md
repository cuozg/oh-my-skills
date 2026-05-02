# Landing Page Patterns for HTML Prototypes

Landing pages differ fundamentally from app prototypes. Where apps have multiple screens with navigation and persistent state, landing pages are single-scroll experiences designed around a conversion goal. They combine hero sections, social proof, feature showcases, pricing, and calls-to-action into a linear narrative that guides visitors toward a single action. All patterns below use CSS custom properties from the shared css-system.md and produce self-contained HTML with no external dependencies beyond Google Fonts.

## Table of Contents
1. [Landing Page Archetypes](#landing-page-archetypes)
2. [Navigation Bar](#navigation-bar)
3. [Hero Section](#hero-section)
4. [Feature Grid](#feature-grid)
5. [Testimonial Section](#testimonial-section)
6. [Pricing Table](#pricing-table)
7. [FAQ Section](#faq-section)
8. [CTA Section](#cta-section)
9. [Stats Section](#stats-section)
10. [How It Works](#how-it-works)
11. [Footer](#footer)
12. [Scroll Animations](#scroll-animations)

---

## Landing Page Archetypes

### Hero-Centric
Best for products with strong visual identity, design tools, or consumer apps. The hero dominates the viewport with a bold visual and single CTA, then supports with features and social proof below. Use when the product speaks visually.
**Section order:** Hero > Features > Social Proof > CTA > Footer

### Conversion-Optimized
Best for SaaS trials, lead generation, and signup funnels. Places the CTA immediately in the hero and repeats it after every major section. Benefits are framed as pain-point solutions. Use when the goal is signups or free trials.
**Section order:** Hero+CTA > Benefits > Pricing > FAQ > Final CTA > Footer

### Feature Showcase
Best for complex products, developer tools, and enterprise SaaS. Opens with a concise hero, then dedicates substantial space to a feature grid followed by deep-dive sections on each major capability. Use when the product has many differentiating features.
**Section order:** Hero > Feature Grid > Deep Feature Sections > Integrations > CTA > Footer

### Social Proof-First
Best for services, B2C brands, and marketplaces. Leads with strong testimonials immediately after the hero to build trust before presenting the offering. Use when credibility is the primary conversion driver.
**Section order:** Hero > Testimonials > How it Works > Pricing > CTA > Footer

### Storytelling
Best for brands, agencies, nonprofits, and mission-driven products. Uses full-width visuals and a narrative arc: problem, solution, impact. Each section flows into the next like a story. Use when emotional resonance matters more than feature comparison.
**Section order:** Full-width Hero > Problem > Solution > Impact > Team > CTA > Footer

### Minimal & Direct
Best for simple products, app launches, waitlists, and pre-launch pages. Everything fits in one or two viewports. No pricing, no feature grids -- just a clear value proposition and a single action. Use when simplicity is the message.
**Section order:** Centered Hero > One Feature Block > CTA > Footer

---

## Navigation Bar

Fixed top navigation that transitions from transparent (over the hero) to solid on scroll. Includes a hamburger menu for mobile.

```html
<nav id="navbar" style="position:fixed;top:0;left:0;right:0;z-index:1000;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;transition:background 0.3s,box-shadow 0.3s;">
  <a href="#" style="display:flex;align-items:center;gap:8px;text-decoration:none;">
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="8" fill="var(--primary)"/><path d="M10 16l4 4 8-8" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span style="font-size:20px;font-weight:700;color:var(--text);">Acme</span>
  </a>
  <div class="nav-links" style="display:flex;align-items:center;gap:32px;">
    <a href="#features" style="text-decoration:none;color:var(--text-dim);font-size:15px;font-weight:500;">Features</a>
    <a href="#pricing" style="text-decoration:none;color:var(--text-dim);font-size:15px;font-weight:500;">Pricing</a>
    <a href="#faq" style="text-decoration:none;color:var(--text-dim);font-size:15px;font-weight:500;">FAQ</a>
    <a href="#cta" style="background:var(--primary);color:#fff;padding:10px 20px;border-radius:8px;text-decoration:none;font-size:14px;font-weight:600;">Get Started</a>
  </div>
  <button class="hamburger" onclick="document.querySelector('.mobile-menu').classList.toggle('open')" style="display:none;background:none;border:none;cursor:pointer;padding:8px;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h18M3 18h18" stroke="var(--text)" stroke-width="2" stroke-linecap="round"/></svg>
  </button>
</nav>

<div class="mobile-menu" style="position:fixed;top:0;left:0;right:0;bottom:0;background:var(--surface);z-index:999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:32px;transform:translateY(-100%);transition:transform 0.3s ease;">
  <a href="#features" style="text-decoration:none;color:var(--text);font-size:20px;font-weight:600;">Features</a>
  <a href="#pricing" style="text-decoration:none;color:var(--text);font-size:20px;font-weight:600;">Pricing</a>
  <a href="#faq" style="text-decoration:none;color:var(--text);font-size:20px;font-weight:600;">FAQ</a>
  <a href="#cta" style="background:var(--primary);color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-size:16px;font-weight:600;">Get Started</a>
</div>

<style>
  .mobile-menu.open { transform: translateY(0); }
  @media (max-width: 768px) {
    .nav-links { display: none !important; }
    .hamburger { display: block !important; }
  }
</style>

<script>
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  if (window.scrollY > 60) {
    nav.style.background = 'var(--surface)';
    nav.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
  } else {
    nav.style.background = 'transparent';
    nav.style.boxShadow = 'none';
  }
});
</script>
```

---

## Hero Section

### Variant A: Centered Hero

Heading, subheading, and CTA centered on the page. Clean and versatile.

```html
<section style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:var(--bg);">
  <div style="max-width:720px;">
    <span style="display:inline-block;padding:6px 16px;border-radius:20px;background:var(--primary-dim);color:var(--primary);font-size:13px;font-weight:600;margin-bottom:24px;">Now in public beta</span>
    <h1 style="font-size:clamp(36px,5vw,64px);font-weight:800;color:var(--text);line-height:1.1;margin:0 0 20px;">Ship faster with less complexity</h1>
    <p style="font-size:clamp(16px,2vw,20px);color:var(--text-dim);line-height:1.6;margin:0 0 40px;">The all-in-one platform that replaces your project management, CI/CD, and deployment tools. Built for teams that move fast.</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="#" style="background:var(--primary);color:#fff;padding:14px 32px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:600;">Start free trial</a>
      <a href="#" style="background:var(--surface);color:var(--text);padding:14px 32px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:600;border:1px solid var(--border);">Watch demo</a>
    </div>
  </div>
</section>
```

### Variant B: Split Hero

Text on the left, product screenshot or illustration on the right. Ideal for showing the product in context.

```html
<section style="min-height:100vh;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:64px;padding:120px 48px 80px;background:var(--bg);">
  <div>
    <span style="display:inline-block;padding:6px 16px;border-radius:20px;background:var(--primary-dim);color:var(--primary);font-size:13px;font-weight:600;margin-bottom:20px;">Trusted by 5,000+ teams</span>
    <h1 style="font-size:clamp(32px,4vw,56px);font-weight:800;color:var(--text);line-height:1.1;margin:0 0 20px;">Analytics that actually help you grow</h1>
    <p style="font-size:18px;color:var(--text-dim);line-height:1.6;margin:0 0 36px;">Stop guessing. Get real-time insights into user behavior, conversion funnels, and revenue metrics -- all in one dashboard.</p>
    <a href="#" style="display:inline-block;background:var(--primary);color:#fff;padding:14px 32px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:600;">Get started free</a>
  </div>
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:24px;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;">
    <div style="width:100%;height:100%;background:linear-gradient(135deg,var(--primary-dim),var(--accent-dim));border-radius:8px;display:flex;align-items:center;justify-content:center;">
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none"><rect x="8" y="28" width="12" height="28" rx="3" fill="var(--primary)" opacity="0.5"/><rect x="26" y="16" width="12" height="40" rx="3" fill="var(--primary)" opacity="0.7"/><rect x="44" y="8" width="12" height="48" rx="3" fill="var(--primary)"/></svg>
    </div>
  </div>
</section>
<style>
  @media (max-width: 768px) {
    section:has(> div > h1) { grid-template-columns: 1fr !important; padding: 100px 24px 60px !important; }
  }
</style>
```

### Variant C: Full-Width Gradient Hero

Bold gradient background with overlaid text. High visual impact for brand-driven pages.

```html
<section style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#0f172a 100%);position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 40%,rgba(59,130,246,0.15),transparent 60%);"></div>
  <div style="max-width:720px;position:relative;z-index:1;">
    <h1 style="font-size:clamp(36px,5vw,72px);font-weight:800;color:#fff;line-height:1.05;margin:0 0 24px;">Build the future of your business</h1>
    <p style="font-size:clamp(16px,2vw,20px);color:rgba(255,255,255,0.7);line-height:1.6;margin:0 0 40px;">Enterprise-grade infrastructure with startup-speed deployment. Scale from zero to millions without changing a line of code.</p>
    <a href="#" style="display:inline-block;background:#fff;color:#0f172a;padding:16px 36px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:700;">Request early access</a>
  </div>
</section>
```

---

## Feature Grid

### Variant A: Three-Column Icon Cards

Classic feature grid with inline SVG icon, title, and description per card.

```html
<section id="features" style="padding:96px 24px;background:var(--surface);">
  <div style="max-width:1080px;margin:0 auto;text-align:center;margin-bottom:64px;">
    <h2 style="font-size:clamp(28px,3.5vw,42px);font-weight:800;color:var(--text);margin:0 0 16px;">Everything you need to ship</h2>
    <p style="font-size:18px;color:var(--text-dim);max-width:560px;margin:0 auto;">Powerful features that replace your entire tool stack. No more switching between tabs.</p>
  </div>
  <div style="max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:32px;">
    <div style="padding:32px;border-radius:16px;border:1px solid var(--border);background:var(--bg);">
      <div style="width:48px;height:48px;border-radius:12px;background:var(--primary-dim);display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Instant deployments</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">Push to main and your changes are live in under 30 seconds. Zero-downtime rollbacks included.</p>
    </div>
    <div style="padding:32px;border-radius:16px;border:1px solid var(--border);background:var(--bg);">
      <div style="width:48px;height:48px;border-radius:12px;background:var(--accent-dim);display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Built-in security</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">SOC 2 compliant out of the box. Automatic SSL, DDoS protection, and vulnerability scanning on every deploy.</p>
    </div>
    <div style="padding:32px;border-radius:16px;border:1px solid var(--border);background:var(--bg);">
      <div style="width:48px;height:48px;border-radius:12px;background:var(--primary-dim);display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="var(--primary)" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="7" r="4" stroke="var(--primary)" stroke-width="2"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" stroke="var(--primary)" stroke-width="2" stroke-linecap="round"/></svg>
      </div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Team collaboration</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">Real-time multiplayer editing, branch previews, and async review workflows your team will actually enjoy.</p>
    </div>
  </div>
</section>
```

### Variant B: Bento Grid

Mixed-size cards in a visually dynamic layout. Larger cards for hero features, smaller for supporting ones.

```html
<section style="padding:96px 24px;background:var(--bg);">
  <div style="max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:auto auto;gap:20px;">
    <div style="grid-column:span 2;padding:40px;border-radius:20px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;display:flex;flex-direction:column;justify-content:flex-end;min-height:280px;">
      <h3 style="font-size:28px;font-weight:800;margin:0 0 8px;">AI-powered search</h3>
      <p style="font-size:16px;opacity:0.85;margin:0;">Natural language queries across your entire codebase. Find anything in milliseconds.</p>
    </div>
    <div style="padding:32px;border-radius:20px;border:1px solid var(--border);background:var(--surface);">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" style="margin-bottom:16px;"><path d="M12 2v20M2 12h20" stroke="var(--primary)" stroke-width="2" stroke-linecap="round"/></svg>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">One-click integrations</h3>
      <p style="font-size:14px;color:var(--text-dim);margin:0;">Connect Slack, GitHub, Linear, and 40+ tools in seconds.</p>
    </div>
    <div style="padding:32px;border-radius:20px;border:1px solid var(--border);background:var(--surface);">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" style="margin-bottom:16px;"><circle cx="12" cy="12" r="10" stroke="var(--accent)" stroke-width="2"/><path d="M12 6v6l4 2" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"/></svg>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Real-time sync</h3>
      <p style="font-size:14px;color:var(--text-dim);margin:0;">Changes propagate across all clients within 50ms.</p>
    </div>
    <div style="grid-column:span 2;padding:40px;border-radius:20px;border:1px solid var(--border);background:var(--surface);display:flex;align-items:center;gap:40px;">
      <div style="flex:1;">
        <h3 style="font-size:22px;font-weight:700;color:var(--text);margin:0 0 8px;">Advanced analytics</h3>
        <p style="font-size:15px;color:var(--text-dim);margin:0;">Track every metric that matters. Custom dashboards, automated reports, and anomaly detection.</p>
      </div>
      <div style="width:160px;height:100px;background:var(--primary-dim);border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><polyline points="4,36 16,20 28,28 44,8" stroke="var(--primary)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
    </div>
  </div>
</section>
<style>
  @media (max-width: 768px) {
    section > div[style*="grid-template-columns:repeat(3"] { grid-template-columns: 1fr !important; }
    section > div[style*="grid-template-columns:repeat(3"] > div[style*="grid-column:span 2"] { grid-column: span 1 !important; }
  }
</style>
```

---

## Testimonial Section

### Variant A: Card Grid

Three testimonial cards with avatar, quote, and attribution.

```html
<!-- Helper: generates 5 star SVGs. Call stars() in a script or inline the output. -->
<style>.stars{display:flex;gap:2px;margin-bottom:16px;}.stars svg{width:18px;height:18px;fill:var(--primary);}</style>
<script>function starsHTML(){const s='<svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.27 5.82 22 7 14.14 2 9.27l6.91-1.01z"/></svg>';return '<div class="stars">'+s.repeat(5)+'</div>';}</script>

<section style="padding:96px 24px;background:var(--bg);">
  <div style="max-width:1080px;margin:0 auto;text-align:center;margin-bottom:64px;">
    <h2 style="font-size:clamp(28px,3.5vw,42px);font-weight:800;color:var(--text);margin:0 0 16px;">Loved by teams everywhere</h2>
    <p style="font-size:18px;color:var(--text-dim);">See what our customers are saying.</p>
  </div>
  <div style="max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px;">
    <!-- Card 1 -->
    <div class="testimonial-card" style="padding:32px;border-radius:16px;background:var(--surface);border:1px solid var(--border);">
      <div class="stars"></div>
      <p style="font-size:15px;color:var(--text);line-height:1.7;margin:0 0 20px;">"We cut our deployment time from 45 minutes to under a minute. The team collaboration features alone saved us 10 hours a week."</p>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;">SK</div>
        <div><div style="font-size:14px;font-weight:600;color:var(--text);">Sarah Kim</div><div style="font-size:13px;color:var(--text-dim);">CTO at Relay</div></div>
      </div>
    </div>
    <!-- Card 2 -->
    <div class="testimonial-card" style="padding:32px;border-radius:16px;background:var(--surface);border:1px solid var(--border);">
      <div class="stars"></div>
      <p style="font-size:15px;color:var(--text);line-height:1.7;margin:0 0 20px;">"The analytics dashboard is incredible. We finally have real-time visibility into what our users are doing. Revenue grew 23% in the first quarter."</p>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--primary));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;">MJ</div>
        <div><div style="font-size:14px;font-weight:600;color:var(--text);">Marcus Johnson</div><div style="font-size:13px;color:var(--text-dim);">VP Product at Nova</div></div>
      </div>
    </div>
    <!-- Card 3 -->
    <div class="testimonial-card" style="padding:32px;border-radius:16px;background:var(--surface);border:1px solid var(--border);">
      <div class="stars"></div>
      <p style="font-size:15px;color:var(--text);line-height:1.7;margin:0 0 20px;">"Migrated from three separate tools. The onboarding took less than a day and the support team was exceptional throughout."</p>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#f59e0b,#ef4444);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;">AL</div>
        <div><div style="font-size:14px;font-weight:600;color:var(--text);">Aisha Lopez</div><div style="font-size:13px;color:var(--text-dim);">Engineering Lead at Orbit</div></div>
      </div>
    </div>
  </div>
</section>
<script>document.querySelectorAll('.testimonial-card .stars').forEach(el=>{el.innerHTML=starsHTML().replace('<div class="stars">','').replace('</div>','');});</script>
```

### Variant B: Large Featured Quote

Single prominent testimonial with large quotation and photo area.

```html
<section style="padding:96px 24px;background:var(--surface);">
  <div style="max-width:800px;margin:0 auto;text-align:center;">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" style="margin-bottom:24px;"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1zm12 0c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z" fill="var(--primary)" opacity="0.2"/></svg>
    <p style="font-size:clamp(20px,3vw,28px);color:var(--text);line-height:1.6;font-weight:500;margin:0 0 32px;">"Switching to this platform was the single best infrastructure decision we made this year. Our team ships twice as fast and our incident rate dropped by 80%."</p>
    <div style="display:flex;align-items:center;justify-content:center;gap:16px;">
      <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;">DR</div>
      <div style="text-align:left;">
        <div style="font-size:16px;font-weight:700;color:var(--text);">David Reeves</div>
        <div style="font-size:14px;color:var(--text-dim);">Head of Engineering, Meridian Health</div>
      </div>
    </div>
  </div>
</section>
```

---

## Pricing Table

Three-tier pricing with a highlighted recommended plan.

```html
<!-- Pricing uses a CSS ::before checkmark to avoid repeating SVGs -->
<style>
  .price-list{list-style:none;padding:0;margin:0 0 32px;display:flex;flex-direction:column;gap:12px;}
  .price-list li{display:flex;align-items:center;gap:10px;font-size:15px;color:var(--text);}
  .price-list li::before{content:'';width:18px;height:18px;flex-shrink:0;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none'%3E%3Cpath d='M20 6L9 17l-5-5' stroke='%2322c55e' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") no-repeat center;}
</style>

<section id="pricing" style="padding:96px 24px;background:var(--bg);">
  <div style="max-width:1080px;margin:0 auto;text-align:center;margin-bottom:64px;">
    <h2 style="font-size:clamp(28px,3.5vw,42px);font-weight:800;color:var(--text);margin:0 0 16px;">Simple, transparent pricing</h2>
    <p style="font-size:18px;color:var(--text-dim);">No hidden fees. Cancel anytime.</p>
  </div>
  <div style="max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;align-items:start;">
    <div style="padding:36px;border-radius:16px;border:1px solid var(--border);background:var(--surface);">
      <h3 style="font-size:18px;font-weight:600;color:var(--text-dim);margin:0 0 8px;">Starter</h3>
      <div style="margin-bottom:24px;"><span style="font-size:48px;font-weight:800;color:var(--text);">$0</span><span style="font-size:16px;color:var(--text-dim);">/month</span></div>
      <ul class="price-list"><li>Up to 3 projects</li><li>Basic analytics</li><li>Community support</li></ul>
      <a href="#" style="display:block;text-align:center;padding:14px;border-radius:10px;border:1px solid var(--border);color:var(--text);text-decoration:none;font-weight:600;font-size:15px;">Get started</a>
    </div>
    <div style="padding:36px;border-radius:16px;border:2px solid var(--primary);background:var(--surface);position:relative;">
      <span style="position:absolute;top:-13px;left:50%;transform:translateX(-50%);background:var(--primary);color:#fff;font-size:12px;font-weight:700;padding:4px 16px;border-radius:20px;">Most popular</span>
      <h3 style="font-size:18px;font-weight:600;color:var(--primary);margin:0 0 8px;">Pro</h3>
      <div style="margin-bottom:24px;"><span style="font-size:48px;font-weight:800;color:var(--text);">$29</span><span style="font-size:16px;color:var(--text-dim);">/month</span></div>
      <ul class="price-list"><li>Unlimited projects</li><li>Advanced analytics</li><li>Priority support</li><li>Custom integrations</li></ul>
      <a href="#" style="display:block;text-align:center;padding:14px;border-radius:10px;background:var(--primary);color:#fff;text-decoration:none;font-weight:600;font-size:15px;">Start free trial</a>
    </div>
    <div style="padding:36px;border-radius:16px;border:1px solid var(--border);background:var(--surface);">
      <h3 style="font-size:18px;font-weight:600;color:var(--text-dim);margin:0 0 8px;">Enterprise</h3>
      <div style="margin-bottom:24px;"><span style="font-size:48px;font-weight:800;color:var(--text);">Custom</span></div>
      <ul class="price-list"><li>Everything in Pro</li><li>SSO and SAML</li><li>Dedicated account manager</li><li>99.99% SLA</li></ul>
      <a href="#" style="display:block;text-align:center;padding:14px;border-radius:10px;border:1px solid var(--border);color:var(--text);text-decoration:none;font-weight:600;font-size:15px;">Contact sales</a>
    </div>
  </div>
</section>
```

---

## FAQ Section

Accordion-style with JavaScript expand/collapse.

```html
<section id="faq" style="padding:96px 24px;background:var(--surface);">
  <div style="max-width:720px;margin:0 auto;">
    <h2 style="font-size:clamp(28px,3.5vw,42px);font-weight:800;color:var(--text);text-align:center;margin:0 0 48px;">Frequently asked questions</h2>
    <div class="faq-list" style="display:flex;flex-direction:column;gap:2px;">
      <div class="faq-item" style="border:1px solid var(--border);border-radius:12px;overflow:hidden;">
        <button onclick="this.parentElement.classList.toggle('open')" style="width:100%;padding:20px 24px;background:var(--bg);border:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;font-size:16px;font-weight:600;color:var(--text);text-align:left;">
          How long is the free trial?
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="transition:transform 0.2s;flex-shrink:0;"><path d="M6 9l6 6 6-6" stroke="var(--text-dim)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div style="max-height:0;overflow:hidden;transition:max-height 0.3s ease;">
          <div style="padding:0 24px 20px;font-size:15px;color:var(--text-dim);line-height:1.7;">The Pro plan includes a 14-day free trial with full access to all features. No credit card required. You can downgrade to the free Starter plan at any time.</div>
        </div>
      </div>
      <div class="faq-item" style="border:1px solid var(--border);border-radius:12px;overflow:hidden;">
        <button onclick="this.parentElement.classList.toggle('open')" style="width:100%;padding:20px 24px;background:var(--bg);border:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;font-size:16px;font-weight:600;color:var(--text);text-align:left;">
          Can I migrate from my existing tools?
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="transition:transform 0.2s;flex-shrink:0;"><path d="M6 9l6 6 6-6" stroke="var(--text-dim)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div style="max-height:0;overflow:hidden;transition:max-height 0.3s ease;">
          <div style="padding:0 24px 20px;font-size:15px;color:var(--text-dim);line-height:1.7;">Yes. We provide one-click migration from GitHub, GitLab, Bitbucket, Jira, and Linear. Most teams complete migration in under an hour. Our support team is available to help with custom migrations.</div>
        </div>
      </div>
      <!-- Repeat .faq-item pattern for additional questions -->
    </div>
  </div>
</section>

<style>
  .faq-item.open svg { transform: rotate(180deg); }
  .faq-item.open > div:last-child { max-height: 200px; }
</style>
```

---

## CTA Section

### Variant A: Full-Width Banner

Bold background color with centered heading and CTA button.

```html
<section id="cta" style="padding:80px 24px;background:var(--primary);text-align:center;">
  <div style="max-width:640px;margin:0 auto;">
    <h2 style="font-size:clamp(28px,4vw,44px);font-weight:800;color:#fff;margin:0 0 16px;">Ready to ship faster?</h2>
    <p style="font-size:18px;color:rgba(255,255,255,0.8);margin:0 0 36px;">Join 5,000+ teams already building with us. Start your free trial today.</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="#" style="background:#fff;color:var(--primary);padding:16px 36px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:700;">Start free trial</a>
      <a href="#" style="background:transparent;color:#fff;padding:16px 36px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:600;border:2px solid rgba(255,255,255,0.3);">Talk to sales</a>
    </div>
  </div>
</section>
```

### Variant B: Card-Style CTA

Floating card with gradient background, contained within the page width.

```html
<section style="padding:96px 24px;background:var(--bg);">
  <div style="max-width:900px;margin:0 auto;background:linear-gradient(135deg,var(--primary),var(--accent));border-radius:24px;padding:64px 48px;text-align:center;">
    <h2 style="font-size:clamp(24px,3.5vw,38px);font-weight:800;color:#fff;margin:0 0 16px;">Start building today</h2>
    <p style="font-size:17px;color:rgba(255,255,255,0.8);margin:0 0 32px;max-width:480px;margin-left:auto;margin-right:auto;">Free for individuals and small teams. No credit card required.</p>
    <a href="#" style="display:inline-block;background:#fff;color:var(--primary);padding:16px 36px;border-radius:10px;text-decoration:none;font-size:16px;font-weight:700;">Get started free</a>
  </div>
</section>
```

---

## Stats Section

Big numbers with labels. Optional counter animation via JavaScript.

```html
<section style="padding:80px 24px;background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:960px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;text-align:center;">
    <div>
      <div class="stat-number" data-target="5000" style="font-size:clamp(36px,5vw,56px);font-weight:800;color:var(--primary);margin-bottom:8px;">0</div>
      <div style="font-size:15px;color:var(--text-dim);font-weight:500;">Teams worldwide</div>
    </div>
    <div>
      <div class="stat-number" data-target="99.9" data-suffix="%" style="font-size:clamp(36px,5vw,56px);font-weight:800;color:var(--primary);margin-bottom:8px;">0</div>
      <div style="font-size:15px;color:var(--text-dim);font-weight:500;">Uptime SLA</div>
    </div>
    <div>
      <div class="stat-number" data-target="2" data-suffix="M+" style="font-size:clamp(36px,5vw,56px);font-weight:800;color:var(--primary);margin-bottom:8px;">0</div>
      <div style="font-size:15px;color:var(--text-dim);font-weight:500;">Deployments per month</div>
    </div>
    <div>
      <div class="stat-number" data-target="30" data-suffix="s" style="font-size:clamp(36px,5vw,56px);font-weight:800;color:var(--primary);margin-bottom:8px;">0</div>
      <div style="font-size:15px;color:var(--text-dim);font-weight:500;">Average deploy time</div>
    </div>
  </div>
</section>

<script>
// Counter animation (triggered by IntersectionObserver in Scroll Animations section)
function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const suffix = el.dataset.suffix || '';
  const isDecimal = target % 1 !== 0;
  const duration = 1500;
  const start = performance.now();
  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = isDecimal ? (eased * target).toFixed(1) : Math.floor(eased * target);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
</script>
```

---

## How It Works

Three-step numbered process with icons and connecting line.

```html
<section style="padding:96px 24px;background:var(--bg);">
  <div style="max-width:1080px;margin:0 auto;text-align:center;margin-bottom:64px;">
    <h2 style="font-size:clamp(28px,3.5vw,42px);font-weight:800;color:var(--text);margin:0 0 16px;">Get started in three steps</h2>
    <p style="font-size:18px;color:var(--text-dim);">Up and running in under five minutes.</p>
  </div>
  <div style="max-width:900px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:48px;position:relative;">
    <div style="text-align:center;">
      <div style="width:64px;height:64px;border-radius:50%;background:var(--primary);color:#fff;font-size:24px;font-weight:800;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">1</div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Connect your repo</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">Link your GitHub, GitLab, or Bitbucket repository with one click. We auto-detect your framework.</p>
    </div>
    <div style="text-align:center;">
      <div style="width:64px;height:64px;border-radius:50%;background:var(--primary);color:#fff;font-size:24px;font-weight:800;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">2</div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Configure your pipeline</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">Set build commands, environment variables, and deployment targets. Smart defaults mean most projects need zero configuration.</p>
    </div>
    <div style="text-align:center;">
      <div style="width:64px;height:64px;border-radius:50%;background:var(--primary);color:#fff;font-size:24px;font-weight:800;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">3</div>
      <h3 style="font-size:18px;font-weight:700;color:var(--text);margin:0 0 8px;">Push and deploy</h3>
      <p style="font-size:15px;color:var(--text-dim);line-height:1.6;margin:0;">Every push to main triggers a production deployment. Preview branches get their own URL automatically.</p>
    </div>
  </div>
</section>
```

---

## Footer

Multi-column footer with logo, navigation links, social icons, and copyright.

```html
<footer style="padding:64px 24px 32px;background:#0f172a;color:#94a3b8;">
  <div style="max-width:1080px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;">
    <div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
        <svg width="28" height="28" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="8" fill="#3b82f6"/><path d="M10 16l4 4 8-8" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span style="font-size:18px;font-weight:700;color:#fff;">Acme</span>
      </div>
      <p style="font-size:14px;line-height:1.7;margin:0 0 20px;max-width:280px;">The modern platform for teams that ship. Deploys, analytics, and collaboration in one place.</p>
      <div style="display:flex;gap:16px;">
        <a href="#" style="color:#94a3b8;"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
        <a href="#" style="color:#94a3b8;"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg></a>
        <a href="#" style="color:#94a3b8;"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
      </div>
    </div>
    <div>
      <h4 style="font-size:14px;font-weight:700;color:#fff;margin:0 0 16px;text-transform:uppercase;letter-spacing:0.05em;">Product</h4>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Features</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Pricing</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Changelog</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;">Documentation</a>
    </div>
    <div>
      <h4 style="font-size:14px;font-weight:700;color:#fff;margin:0 0 16px;text-transform:uppercase;letter-spacing:0.05em;">Company</h4>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">About</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Blog</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Careers</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;">Contact</a>
    </div>
    <div>
      <h4 style="font-size:14px;font-weight:700;color:#fff;margin:0 0 16px;text-transform:uppercase;letter-spacing:0.05em;">Legal</h4>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Privacy policy</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;margin-bottom:10px;">Terms of service</a>
      <a href="#" style="display:block;color:#94a3b8;text-decoration:none;font-size:14px;">Security</a>
    </div>
  </div>
  <div style="max-width:1080px;margin:40px auto 0;padding-top:24px;border-top:1px solid #1e293b;font-size:13px;color:#64748b;">2025 Acme Inc. All rights reserved.</div>
</footer>
<style>
  @media (max-width: 768px) { footer > div:first-child { grid-template-columns: 1fr 1fr !important; } }
  @media (max-width: 480px) { footer > div:first-child { grid-template-columns: 1fr !important; } }
</style>
```

---

## Scroll Animations

Reusable IntersectionObserver setup for fade-in-on-scroll, staggered grid reveals, and stat counter triggers.

```html
<style>
  .reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
  .reveal.visible { opacity: 1; transform: translateY(0); }
  .reveal-stagger > * { opacity: 0; transform: translateY(24px); transition: opacity 0.5s ease, transform 0.5s ease; }
  .reveal-stagger.visible > *:nth-child(1) { transition-delay: 0s; }
  .reveal-stagger.visible > *:nth-child(2) { transition-delay: 0.1s; }
  .reveal-stagger.visible > *:nth-child(3) { transition-delay: 0.2s; }
  .reveal-stagger.visible > *:nth-child(4) { transition-delay: 0.3s; }
  .reveal-stagger.visible > * { opacity: 1; transform: translateY(0); }
</style>

<script>
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Trigger stat counters if present
      entry.target.querySelectorAll('.stat-number').forEach(el => {
        if (!el.dataset.animated) {
          el.dataset.animated = 'true';
          animateCounter(el);
        }
      });
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => observer.observe(el));
</script>
```

**Usage:** Add `class="reveal"` to any section for fade-in on scroll. Add `class="reveal-stagger"` to a grid container for staggered child reveals. The observer auto-triggers `animateCounter()` for any `.stat-number` elements inside revealed sections.
