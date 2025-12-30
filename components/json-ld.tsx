export function JsonLd() {
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": "Taiwanway",
        "image": [
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/LOGO-A(%E5%8E%BB%E8%83%8C)-01-md2UWlZPf63lgtuEOcu8FhyaJJySOU.png",
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg"
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "26 South St",
            "addressLocality": "Middletown",
            "addressRegion": "NY",
            "postalCode": "10940",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 41.4459,
            "longitude": -74.4229
        },
        "url": "https://taiwanwayny.com",
        "telephone": "+18453811002",
        "priceRange": "$$",
        "servesCuisine": "Taiwanese",
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Friday", "Saturday"],
                "opens": "11:00",
                "closes": "19:00"
            }
        ],
        "menu": "https://taiwanwayny.com/menu",
        "acceptsReservations": "false",
        "description": "Authentic Taiwanese cuisine in Middletown, NY. Serving Beef Noodle Soup, Braised Pork Rice, Bubble Tea, and Homemade Desserts."
    }

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    )
}
