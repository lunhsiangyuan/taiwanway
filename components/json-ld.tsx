export function JsonLd() {
    const restaurantJsonLd = {
        "@context": "https://schema.org",
        "@type": "CafeOrCoffeeShop",
        "@id": "https://taiwanwayny.com/#restaurant",
        "name": "TaiwanWay 臺灣味",
        "image": [
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/LOGO-A(%E5%8E%BB%E8%83%8C)-01-md2UWlZPf63lgtuEOcu8FhyaJJySOU.png",
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg",
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
            "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
            "https://06jfzz4maekxll04.public.blob.vercel-storage.com/pineapple-cake-QtQVUryed5EphoMtw2te8NyLjQFrSq.jpg"
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
            "latitude": 41.4437301,
            "longitude": -74.4206521
        },
        "url": "https://taiwanwayny.com",
        "telephone": "845-381-1002",
        "email": "taiwanway10940@gmail.com",
        "servesCuisine": ["Taiwanese", "Bubble Tea", "Asian"],
        "priceRange": "$$",
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Monday",
                "opens": "11:00",
                "closes": "19:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Tuesday",
                "opens": "11:00",
                "closes": "19:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Friday",
                "opens": "11:00",
                "closes": "19:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Saturday",
                "opens": "11:00",
                "closes": "19:00"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "69",
            "bestRating": "5"
        },
        "menu": "https://taiwanwayny.com/menu",
        "acceptsReservations": "Yes",
        "description": "Authentic Taiwanese cuisine in Middletown, NY. Serving Beef Noodle Soup, Braised Pork Rice, Bubble Tea, and Homemade Desserts.",
        "hasMenu": {
            "@type": "Menu",
            "name": "TaiwanWay Menu",
            "url": "https://taiwanwayny.com/menu",
            "hasMenuSection": [
                {
                    "@type": "MenuSection",
                    "name": "Rice Dishes",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Braised Pork Rice (滷肉飯)",
                            "description": "Traditional Taiwanese braised pork over rice",
                            "offers": {
                                "@type": "Offer",
                                "price": "10.99",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Chicken Rice (雞肉飯)",
                            "description": "Taiwanese-style chicken over rice",
                            "offers": {
                                "@type": "Offer",
                                "price": "10.99",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Noodle Soups",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Beef Noodle Soup (牛肉麵)",
                            "description": "Signature Taiwanese braised beef noodle soup",
                            "offers": {
                                "@type": "Offer",
                                "price": "13.99",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Homemade Desserts",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Taiwan Pineapple Cake (台灣鳳梨酥)",
                            "description": "Handmade Taiwanese pineapple pastry",
                            "offers": {
                                "@type": "Offer",
                                "price": "3.25",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Taiwanese Black Tea",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Taiwanese Bubble Tea (招牌珍珠奶茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "6.45",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Taiwanese Milk Tea (蜜香奶茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.65",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Caffeine-Free",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Brown Sugar Bubble Milk (黑糖珍珠鮮奶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "6.45",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Jasmine Green Tea",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Honey Jasmine Green Tea (茉莉蜂蜜綠茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "4.85",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Jasmine Green Bubble Tea (茉莉珍珠奶綠)",
                            "offers": {
                                "@type": "Offer",
                                "price": "6.45",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Taiwanese Oolong Tea",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Honey Oolong Bubble Tea (蜂蜜烏龍珍珠奶茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "6.65",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Honey Oolong Milk Tea (蜂蜜烏龍奶茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.85",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Ippodo Japanese Matcha",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Matcha Latte (抹茶拿鐵)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.95",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                },
                {
                    "@type": "MenuSection",
                    "name": "Pot-Brewed Tea (Sugar-Free)",
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": "Dong Pian (冬片)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.00",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Spring Tea (春茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.00",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Jin Xuan (金萱)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.00",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Tie Guan Yin (鐵觀音)",
                            "offers": {
                                "@type": "Offer",
                                "price": "6.00",
                                "priceCurrency": "USD"
                            }
                        },
                        {
                            "@type": "MenuItem",
                            "name": "Ali Mountain Black Tea (阿里山紅茶)",
                            "offers": {
                                "@type": "Offer",
                                "price": "5.00",
                                "priceCurrency": "USD"
                            }
                        }
                    ]
                }
            ]
        }
    }

    const websiteJsonLd = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": "https://taiwanwayny.com/#website",
        "name": "TaiwanWay 臺灣味",
        "alternateName": ["TaiwanWay", "臺灣味", "台灣味"],
        "url": "https://taiwanwayny.com",
        "inLanguage": ["en-US", "zh-TW", "es"],
        "publisher": { "@id": "https://taiwanwayny.com/#restaurant" },
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://taiwanwayny.com/menu?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    }

    const localBusinessJsonLd = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://taiwanwayny.com/#localbusiness",
        "name": "TaiwanWay 臺灣味",
        "legalName": "FONGFOOD LLC",
        "alternateName": ["TaiwanWay", "臺灣味"],
        "url": "https://taiwanwayny.com",
        "telephone": "+1-845-381-1002",
        "email": "taiwanway10940@gmail.com",
        "image": "https://taiwanwayny.com/images/storefront.jpg",
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
            "latitude": 41.4437301,
            "longitude": -74.4206521
        },
        "areaServed": [
            { "@type": "City", "name": "Middletown, NY" },
            { "@type": "AdministrativeArea", "name": "Orange County, NY" },
            { "@type": "AdministrativeArea", "name": "Hudson Valley" }
        ],
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "paymentAccepted": "Cash, Credit Card",
        "sameAs": [
            "https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A"
        ],
        "openingHoursSpecification": [
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "11:00", "closes": "19:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Tuesday", "opens": "11:00", "closes": "19:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "11:00", "closes": "19:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:00", "closes": "19:00" }
        ]
    }

    const organizationJsonLd = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://taiwanwayny.com/#organization",
        "name": "FONGFOOD LLC d/b/a TaiwanWay",
        "alternateName": "TaiwanWay 臺灣味",
        "url": "https://taiwanwayny.com",
        "logo": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/LOGO-A(%E5%8E%BB%E8%83%8C)-01-md2UWlZPf63lgtuEOcu8FhyaJJySOU.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+1-845-381-1002",
            "contactType": "customer service",
            "email": "taiwanway10940@gmail.com",
            "availableLanguage": ["en", "zh-Hant", "es"]
        }
    }

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(restaurantJsonLd) }}
            />
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessJsonLd) }}
            />
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationJsonLd) }}
            />
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }}
            />
        </>
    )
}

// Breadcrumb schema — use on inner pages. Pass ordered list of {name, url}
export function BreadcrumbJsonLd({ items }: { items: Array<{ name: string; url: string }> }) {
    const breadcrumbJsonLd = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items.map((item, i) => ({
            "@type": "ListItem",
            "position": i + 1,
            "name": item.name,
            "item": item.url,
        })),
    }
    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
        />
    )
}
