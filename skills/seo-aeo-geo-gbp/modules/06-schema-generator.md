# MODULE 06: SCHEMA GENERATOR
**Skill:** seo-aeo-geo-gbp-orchestrator v2.1.0
**Trigger:** `/seo schema [url or business-type]`

---

## PURPOSE

Generate ready-to-deploy JSON-LD schema markup for all relevant schema types. Every block produced is valid, complete, and immediately usable — not a template with [PLACEHOLDER] text. When Glen's brand entity bundle is loaded, schema is pre-populated with real data.

---

## INPUT REQUIREMENTS

```yaml
required:
  - at_least_one_of:
    - target_url          # URL to generate schema for
    - business_type       # "photographer" | "software-product" | "personal-brand" | "local-service"

optional:
  - schema_types: []      # Specific types to generate. If empty: skill recommends based on page type
  - page_content: ""      # Page body text (paste or fetch) — used to extract FAQ items, prices, etc.
  - product_name: ""      # For SoftwareApplication / Product schemas
  - review_data: {}       # Aggregate rating data for AggregateRating schema
```

---

## SCHEMA TYPE SELECTION LOGIC

Based on the URL or business type, recommend the appropriate schema types:

```
IF page = homepage (local business):
  → LocalBusiness + Organization + Person (if personal brand)

IF page = service page:
  → Service + LocalBusiness (nested) + FAQPage (if FAQ section exists)

IF page = product/software landing page:
  → SoftwareApplication + Product + AggregateRating + FAQPage

IF page = about page (personal brand):
  → Person + Organization + Award (if awards present)

IF page = blog/article:
  → Article + BreadcrumbList + FAQPage (if Q&A content)

IF page = pricing page:
  → Offer + PriceSpecification (nested in Product or Service)

IF page = contact page:
  → LocalBusiness (contact details focus) + GeoCoordinates
```

**Stack schema where multiple types apply.** Google supports multiple schema blocks per page.

---

## SCHEMA GENERATION — ALL TYPES

### 1. LocalBusiness / ProfessionalService

For local businesses. Glen's photography business uses `ProfessionalService` (subtype of `LocalBusiness`).

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "ProfessionalService"],
  "@id": "https://www.glenegrant.com/#business",
  "name": "Glen E. Grant Creative",
  "description": "Toronto commercial photographer specializing in fashion, glamour, lifestyle, and brand photography. Operating since 2000.",
  "url": "https://www.glenegrant.com",
  "telephone": "+1-416-801-2525",
  "email": "glen@glenegrant.com",
  "priceRange": "$799-$2999",
  "image": "https://www.glenegrant.com/assets/images/glen-e-grant-commercial-photographer-toronto.avif",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.glenegrant.com/assets/images/glen-e-grant-logo.png"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "",
    "addressLocality": "Toronto",
    "addressRegion": "ON",
    "postalCode": "M6K 3R1",
    "addressCountry": "CA"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 43.6532,
    "longitude": -79.3832
  },
  "areaServed": {
    "@type": "City",
    "name": "Toronto"
  },
  "serviceType": [
    "Commercial Photography",
    "Fashion Photography",
    "Brand Photography",
    "Lifestyle Photography",
    "Fitness Photography",
    "Editorial Photography"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Photography Packages",
    "itemListElement": [
      {
        "@type": "Offer",
        "name": "Foundation Package",
        "description": "Portfolio-focused commercial photography session",
        "price": "799",
        "priceCurrency": "CAD"
      },
      {
        "@type": "Offer",
        "name": "Strategic Package",
        "description": "Full commercial photography production for brand campaigns",
        "price": "1799",
        "priceCurrency": "CAD"
      },
      {
        "@type": "Offer",
        "name": "Enterprise Package",
        "description": "Multi-day production with AI content multiplication",
        "price": "2999",
        "priceCurrency": "CAD"
      }
    ]
  },
  "founder": {
    "@type": "Person",
    "@id": "https://profile.glenegrant.com/#glen",
    "name": "Glen E. Grant"
  },
  "foundingDate": "2000",
  "sameAs": [
    "https://profile.glenegrant.com",
    "https://github.com/Glenskii"
  ]
}
```

---

### 2. Person Schema (Personal Brand)

For `profile.glenegrant.com` and About pages.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://profile.glenegrant.com/#glen",
  "name": "Glen E. Grant",
  "givenName": "Glen",
  "familyName": "Grant",
  "jobTitle": "Commercial Photographer & Software Developer",
  "description": "Toronto commercial photographer with 25+ years of editorial and brand photography experience. Developer of Watermark Gienie V3, IdeaThreader Pro, Sitemap Architect Pro, and other software products.",
  "url": "https://profile.glenegrant.com",
  "image": "https://profile.glenegrant.com/assets/glen-e-grant-headshot.avif",
  "email": "glen@glenegrant.com",
  "telephone": "+1-416-801-2525",
  "worksFor": {
    "@type": "Organization",
    "@id": "https://www.glenegrant.com/#business",
    "name": "Glen E. Grant Creative"
  },
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Toronto",
    "addressRegion": "ON",
    "addressCountry": "CA",
    "postalCode": "M6K 3R1"
  },
  "alumniOf": [],
  "award": "Cannes recognition — Unmasking the Pain (October 2024)",
  "knowsAbout": [
    "Commercial Photography",
    "Fashion Photography",
    "Brand Photography",
    "Software Development",
    "AI Content Generation",
    "Electron Applications",
    "Cloudflare Workers"
  ],
  "sameAs": [
    "https://www.glenegrant.com",
    "https://github.com/Glenskii"
  ]
}
```

---

### 3. SoftwareApplication Schema

For software product landing pages (Watermark Gienie V3, IdeaThreader Pro, etc.)

**Watermark Gienie V3 example:**
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "https://watermarkgienie.com/#app",
  "name": "Watermark Gienie V3",
  "description": "Professional batch watermarking software for Windows. Process up to 5,000 images with multiple watermark layers, custom positioning, and multi-core processing.",
  "url": "https://watermarkgienie.com",
  "applicationCategory": "PhotographyApplication",
  "applicationSubCategory": "Batch Image Processing",
  "operatingSystem": "Windows 10, Windows 11",
  "softwareVersion": "3.0",
  "datePublished": "2024-01-01",
  "offers": [
    {
      "@type": "Offer",
      "name": "Watermark Gienie V3 Trial",
      "description": "Trial version — 10 images per batch, 2 watermark layers",
      "price": "0",
      "priceCurrency": "USD"
    },
    {
      "@type": "Offer",
      "name": "Watermark Gienie V3 Pro",
      "description": "Pro version — 5,000 images per batch, 3 watermark layers",
      "price": "49",
      "priceCurrency": "USD"
    }
  ],
  "author": {
    "@type": "Person",
    "@id": "https://profile.glenegrant.com/#glen",
    "name": "Glen E. Grant"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Glen E. Grant Creative",
    "url": "https://www.glenegrant.com"
  },
  "downloadUrl": "https://watermarkgienie.com/download",
  "featureList": [
    "Batch process up to 5,000 images",
    "3 watermark layers simultaneously",
    "Multi-core processing engine",
    "JPEG, PNG, WebP support",
    "Custom watermark positioning and opacity",
    "EXIF data preservation"
  ]
}
```

---

### 4. FAQPage Schema

For pages with FAQ sections. Must match the actual Q&A content on the page exactly.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does commercial photography cost in Toronto?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Commercial photography in Toronto typically ranges from $799 for portfolio shoots to $2,999 for full production brand campaigns. Glen E. Grant Creative offers Foundation, Strategic, and Enterprise packages covering fashion, lifestyle, and brand photography for Toronto businesses and agencies."
      }
    },
    {
      "@type": "Question",
      "name": "What types of commercial photography does Glen E. Grant specialize in?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Glen E. Grant specializes in fashion, glamour, lifestyle, brand, fitness, and editorial photography for businesses and agencies across Canada. Services include full production brand campaigns and AI-powered content multiplication for high-volume visual content needs."
      }
    },
    {
      "@type": "Question",
      "name": "How far in advance should I book a commercial photographer in Toronto?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "For standard commercial shoots in Toronto, 2-3 weeks lead time is recommended. For larger productions with talent coordination and location scouting, 4-6 weeks provides the best results. Priority bookings are available — contact glen@glenegrant.com to discuss availability."
      }
    }
  ]
}
```

---

### 5. Article / BlogPosting Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "[article-url]#article",
  "headline": "[Article headline — max 110 characters]",
  "description": "[Article meta description — 150 chars]",
  "image": {
    "@type": "ImageObject",
    "url": "[featured image URL]",
    "width": 1200,
    "height": 630
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "author": {
    "@type": "Person",
    "@id": "https://profile.glenegrant.com/#glen",
    "name": "Glen E. Grant"
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://www.glenegrant.com/#business",
    "name": "Glen E. Grant Creative",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.glenegrant.com/assets/images/glen-e-grant-logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "[article-url]"
  }
}
```

---

### 6. BreadcrumbList Schema

For all interior pages — critical for SERP breadcrumb display.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.glenegrant.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[Section Name]",
      "item": "https://www.glenegrant.com/[section]/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[Page Name]",
      "item": "https://www.glenegrant.com/[section]/[page]/"
    }
  ]
}
```

---

### 7. AggregateRating Schema

Only add when real reviews exist. Never fabricate rating count or values.

```json
{
  "@context": "https://schema.org",
  "@type": "AggregateRating",
  "itemReviewed": {
    "@id": "https://www.glenegrant.com/#business"
  },
  "ratingValue": "[actual average]",
  "reviewCount": "[actual count]",
  "bestRating": "5",
  "worstRating": "1"
}
```

**Embed this inside the LocalBusiness or SoftwareApplication block, not standalone.**

---

### 8. HowTo Schema

For how-to pages or instructional content.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[How to X title]",
  "description": "[Brief description of what the reader will accomplish]",
  "totalTime": "PT[N]M",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "[Step 1 name]",
      "text": "[Complete step description]",
      "image": {
        "@type": "ImageObject",
        "url": "[step illustration if available]"
      }
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "[Step 2 name]",
      "text": "[Complete step description]"
    }
  ]
}
```

---

## SCHEMA PLACEMENT RULES

**All schema goes in `<head>` via `<script type="application/ld+json">` tags.**

```html
<script type="application/ld+json">
{
  // schema block here
}
</script>
```

**Stacking multiple schema types:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "LocalBusiness block" },
    { "FAQPage block" },
    { "BreadcrumbList block" }
  ]
}
</script>
```

Using `@graph` is the cleanest approach — combines all schema for a page into one block.

**WordPress + RankMath warning:** RankMath generates its own schema automatically. Before adding hand-written schema, check what RankMath is already generating (via browser → View Source → search for "application/ld+json"). Adding duplicate schema blocks causes validation errors. Either:
- Disable RankMath schema for specific post types, OR
- Use RankMath's schema editor to customize instead of hand-writing

---

## SCHEMA VALIDATION

After generating schema, validate before deploying:

1. **Google's Rich Results Test:** `search.google.com/test/rich-results`
2. **Schema.org Validator:** `validator.schema.org`
3. **Check for:**
   - No `@type` errors
   - No required fields missing (different by schema type)
   - Prices formatted as numeric strings, not "$X"
   - Dates in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDThh:mm:ssZ)
   - URLs are absolute (https://...), not relative (/path)

---

## SCHEMA OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCHEMA GENERATION REPORT
Target: [url]
Date: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCHEMA TYPES GENERATED: [list]
SCHEMA TYPES RECOMMENDED BUT NOT YET GENERATED: [list with reason]

[Schema block 1 — labeled, complete JSON-LD]

[Schema block 2 — labeled, complete JSON-LD]

[...]

COMBINED @GRAPH BLOCK (paste this into <head>):
[single @graph block combining all schemas above]

VALIDATION CHECKLIST
□ Test at search.google.com/test/rich-results
□ Confirm no RankMath schema conflicts (if WordPress)
□ Verify all prices match live page pricing
□ Verify all URLs return 200

NEXT MODULES
→ /seo audit [url]    verify schema is rendering after deploy
→ /seo aeo [url]      align FAQ schema questions with AEO targets
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
