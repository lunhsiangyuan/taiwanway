'use client'

import { MapPin, Clock } from "lucide-react"
import { useLanguage } from "@/lib/i18n/language-context"

export function BusinessInfoSection() {
    const { t } = useLanguage()

    return (
        <section className="py-12 bg-muted/30">
            <div className="container px-4 md:px-6 mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                    {/* Address Column */}
                    <div className="flex flex-col items-center text-center p-6 bg-background rounded-lg shadow-sm">
                        <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                            <MapPin className="h-6 w-6 text-primary" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2">{t('contact.address')}</h3>
                        <p className="text-muted-foreground">
                            26 South St<br />
                            Middletown, NY 10940
                        </p>
                    </div>

                    {/* Hours Column */}
                    <div className="flex flex-col items-center text-center p-6 bg-background rounded-lg shadow-sm">
                        <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                            <Clock className="h-6 w-6 text-primary" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2">{t('contact.businessHours')}</h3>
                        <p className="text-muted-foreground mb-1">
                            {t('contact.schedule')}
                        </p>
                        <p className="text-lg font-medium text-primary">
                            11:00 AM - 7:00 PM
                        </p>
                        <p className="text-sm text-muted-foreground mt-2">
                            ({t('contact.closed')})
                        </p>
                    </div>
                </div>
            </div>
        </section>
    )
}
