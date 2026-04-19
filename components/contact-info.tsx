'use client'

import { Card, CardContent } from "@/components/ui/card"
import { MapPin, Clock, Phone } from "lucide-react"
import { useLanguage } from "@/lib/i18n/language-context"

export function ContactInfo() {
  const { t } = useLanguage()

  return (
    <section className="py-20">
      <div className="container px-4 md:px-6">
        <h2 className="text-4xl font-bold text-center mb-4">{t('contact.getInTouch')}</h2>
        <p className="text-center text-muted-foreground max-w-2xl mx-auto mb-12">
          {t('contact.description')}
        </p>
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <MapPin className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-xl mb-2">{t('contact.address')}</h3>
                <p className="text-muted-foreground">26 South St</p>
                <p className="text-muted-foreground">Middletown, NY</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Clock className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-xl mb-2">{t('contact.businessHours')}</h3>
                <p className="text-muted-foreground">{t('contact.schedule')}</p>
                <p className="text-muted-foreground">{t('contact.time')}</p>
                <p className="text-muted-foreground mt-2">{t('contact.closed')}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Phone className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-xl mb-2">{t('contact.phone')}</h3>
                <p className="text-muted-foreground">845-381-1002</p>
                <p className="text-muted-foreground">usamyheish@gmail.com</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

