# JSON-LD Templates Reference
**Skill:** seo-aeo-geo-gbp-orchestrator v2.1.0
**Used by:** Module 06 (Schema Generator)

---

## DEPLOYMENT INSTRUCTIONS

All JSON-LD schema goes in the HTML `<head>` section, inside a `<script type="application/ld+json">` tag.

**Single schema block:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "...",
  ...
}
</script>
```

**Multiple schemas on one page — use @graph (preferred):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { ... first schema ... },
    { ... second schema ... }
  ]
}
</script>
```

**WordPress + RankMath:** Check existing schema before adding. View Source → search `application/ld+json`. If RankMath is generating LocalBusiness schema, either edit via RankMath's schema editor or disable RankMath schema for that post type — do not create conflicting duplicate blocks.

**Cloudflare Pages / Static HTML:** Add directly to `<head>` — no plugin conflicts.

---

## TEMPLATE: COMPLETE GLEN HOMEPAGE SCHEMA

Ready to deploy on `https://www.glenegrant.com` — uses `@graph` to combine all relevant types.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness", "ProfessionalService"],
      "@id": "https://www.glenegrant.com/#business",
      "name": "Glen E. Grant Creative",
      "description": "Toronto commercial photographer specializing in fashion, glamour, lifestyle, and brand photography for businesses and agencies across Canada. Operating since 2000.",
      "url": "https://www.glenegrant.com",
      "telephone": "+1-416-801-2525",
      "email": "glen@glenegrant.com",
      "priceRange": "$799-$2999",
      "address": {
        "@type": "PostalAddress",
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
      "foundingDate": "2000",
      "founder": {
        "@type": "Person",
        "@id": "https://profile.glenegrant.com/#glen",
        "name": "Glen E. Grant"
      },
      "sameAs": [
        "https://profile.glenegrant.com",
        "https://github.com/Glenskii"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://profile.glenegrant.com/#glen",
      "name": "Glen E. Grant",
      "jobTitle": "Commercial Photographer & Software Developer",
      "worksFor": {
        "@id": "https://www.glenegrant.com/#business"
      },
      "url": "https://profile.glenegrant.com",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Toronto",
        "addressRegion": "ON",
        "addressCountry": "CA"
      },
      "sameAs": [
        "https://www.glenegrant.com",
        "https://github.com/Glenskii"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.glenegrant.com/#website",
      "url": "https://www.glenegrant.com",
      "name": "Glen E. Grant Creative",
      "publisher": {
        "@id": "https://www.glenegrant.com/#business"
      }
    }
  ]
}
```

---

## TEMPLATE: PROFILE PAGE (profile.glenegrant.com)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://profile.glenegrant.com/#glen",
      "name": "Glen E. Grant",
      "givenName": "Glen",
      "familyName": "Grant",
      "jobTitle": "Commercial Photographer & Software Developer",
      "description": "Toronto commercial photographer with 25+ years editorial and brand experience. Developer of Watermark Gienie V3, IdeaThreader Pro, Sitemap Architect Pro, MailMindz, and other software products.",
      "url": "https://profile.glenegrant.com",
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
        "postalCode": "M6K 3R1",
        "addressCountry": "CA"
      },
      "award": "Cannes recognition — Unmasking the Pain (October 2024)",
      "knowsAbout": [
        "Commercial Photography",
        "Fashion Photography",
        "Brand Photography",
        "Software Development",
        "Electron Applications",
        "Cloudflare Workers"
      ],
      "sameAs": [
        "https://www.glenegrant.com",
        "https://github.com/Glenskii"
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://profile.glenegrant.com/#webpage",
      "url": "https://profile.glenegrant.com",
      "name": "Glen E. Grant — Commercial Photographer & Software Developer",
      "about": {
        "@id": "https://profile.glenegrant.com/#glen"
      },
      "mainEntity": {
        "@id": "https://profile.glenegrant.com/#glen"
      }
    }
  ]
}
```

---

## TEMPLATE: SOFTWARE PRODUCT — WATERMARK GIENIE V3

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "@id": "https://watermarkgienie.com/#app",
      "name": "Watermark Gienie V3",
      "description": "Professional batch watermarking software for Windows. Process up to 5,000 images with up to 3 watermark layers, custom positioning, opacity control, and multi-core processing.",
      "url": "https://watermarkgienie.com",
      "applicationCategory": "PhotographyApplication",
      "operatingSystem": "Windows 10, Windows 11",
      "downloadUrl": "https://watermarkgienie.com/download",
      "softwareVersion": "3.0",
      "author": {
        "@type": "Person",
        "@id": "https://profile.glenegrant.com/#glen",
        "name": "Glen E. Grant"
      },
      "offers": [
        {
          "@type": "Offer",
          "name": "Trial",
          "description": "10 images per batch, 2 watermark layers",
          "price": "0",
          "priceCurrency": "USD"
        },
        {
          "@type": "Offer",
          "name": "Pro License",
          "description": "5,000 images per batch, 3 watermark layers",
          "price": "49",
          "priceCurrency": "USD"
        }
      ],
      "featureList": [
        "Batch process up to 5,000 images",
        "3 simultaneous watermark layers",
        "Multi-core processing engine",
        "JPEG, PNG, WebP support",
        "EXIF data preservation",
        "Custom positioning, opacity, rotation"
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How many images can Watermark Gienie V3 process at once?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Watermark Gienie V3 Pro processes up to 5,000 images per batch using multi-core processing for maximum speed. The Trial version processes up to 10 images per batch."
          }
        },
        {
          "@type": "Question",
          "name": "Does Watermark Gienie V3 work on Mac?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Watermark Gienie V3 is currently a Windows application, compatible with Windows 10 and Windows 11."
          }
        }
      ]
    }
  ]
}
```

---

## VALIDATION QUICK REFERENCE

| Tool | URL | What it checks |
|------|-----|----------------|
| Google Rich Results Test | search.google.com/test/rich-results | Rich result eligibility |
| Schema.org Validator | validator.schema.org | Schema validity |
| Google Search Console | GSC → Enhancements tab | Deployed schema performance |

**Common validation errors:**

- `"price" must be a string` — prices must be `"49"` not `49`
- `Missing required field "offers"` — SoftwareApplication needs at least one Offer
- `"url" must be an absolute URL` — use `"https://..."` not `"/path"`
- `"datePublished" must be ISO 8601` — use `"2026-05-17"` not `"May 17, 2026"`
- `Duplicate @type` — if using @graph, don't repeat the same @id in two separate blocks
