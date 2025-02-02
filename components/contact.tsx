'use client'

import { Clock, MapPin, Phone } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useLanguage } from "@/lib/i18n/language-context"

export function Contact() {
  const { t } = useLanguage()

  return (
    <div className="py-20">
      <div className="container px-4 md:px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-8 text-center">{t('contact.getInTouch')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Map Section */}
            <div className="space-y-6">
              <h3 className="text-xl font-semibold">{t('contact.findUs')}</h3>
              <div className="aspect-video relative">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2986.7851508083437!2d-74.42330812346005!3d41.44533459467247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c33c1e0cef2c35%3A0x3f4a36d8e3c3c3c3!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1708561234567!5m2!1sen!2sus"
                  className="absolute inset-0 w-full h-full border-0"
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://www.google.com/maps/search/?api=1&query=Taiwanway+26+South+St+Middletown+NY"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <MapPin className="mr-2 h-4 w-4" />
                  {t('nav.getDirections')}
                </a>
              </Button>
            </div>

            {/* Contact Info */}
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-4">{t('contact.businessHours')}</h3>
                <div className="flex items-start gap-2 text-muted-foreground">
                  <Clock className="h-5 w-5 mt-0.5 shrink-0" />
                  <div>
                    <p>{t('contact.schedule')}</p>
                    <p>{t('contact.time')}</p>
                    <p className="mt-2">{t('contact.closed')}</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4">{t('contact.address')}</h3>
                <div className="flex items-start gap-2 text-muted-foreground">
                  <MapPin className="h-5 w-5 mt-0.5 shrink-0" />
                  <p>26 South St, Middletown NY</p>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4">{t('contact.phone')}</h3>
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Phone className="h-5 w-5 shrink-0" />
                  <a href="tel:845-381-1002" className="hover:text-primary">
                    845-381-1002
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

