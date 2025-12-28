'use client'

import { Clock, MapPin, Phone } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { useLanguage } from "@/lib/i18n/language-context"

export function Contact() {
  const { t } = useLanguage()

  return (
    <div className="py-20">
      <div className="container px-4 md:px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">{t('contact.title')}</h2>

          {/* Contact Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <Card className="flex flex-col md:flex-row items-center p-6 gap-4">
              <div className="flex justify-center md:w-1/4">
                <Clock className="h-8 w-8 text-primary" />
              </div>
              <div className="text-center md:text-left md:w-3/4">
                <h3 className="font-semibold text-xl mb-2">{t('contact.businessHours')}</h3>
                <div className="text-muted-foreground">
                  <p>{t('contact.schedule')}</p>
                  <p>{t('contact.time')}</p>
                  <p className="mt-2">{t('contact.closed')}</p>
                </div>
              </div>
            </Card>

            <Card className="flex flex-col md:flex-row items-center p-6 gap-4">
              <div className="flex justify-center md:w-1/4">
                <MapPin className="h-8 w-8 text-primary" />
              </div>
              <div className="text-center md:text-left md:w-3/4">
                <h3 className="font-semibold text-xl mb-2">{t('contact.address')}</h3>
                <p className="text-muted-foreground">26 South St</p>
                <p className="text-muted-foreground">Middletown, NY</p>
              </div>
            </Card>

            <Card className="flex flex-col md:flex-row items-center p-6 gap-4">
              <div className="flex justify-center md:w-1/4">
                <Phone className="h-8 w-8 text-primary" />
              </div>
              <div className="text-center md:text-left md:w-3/4">
                <h3 className="font-semibold text-xl mb-2">{t('contact.phone')}</h3>
                <a href="tel:845-381-1002" className="text-muted-foreground hover:text-primary block">
                  845-381-1002
                </a>
                <p className="text-muted-foreground">usamyheish@gmail.com</p>
              </div>
            </Card>
          </div>

          {/* Map Section */}
          <div className="space-y-6">
            <h3 className="text-xl font-semibold">{t('contact.findUs')}</h3>
            <div className="aspect-[21/9] relative rounded-lg overflow-hidden">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2986.7851508083437!2d-74.42330812346005!3d41.44533459467247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c33c1e0cef2c35%3A0x3f4a36d8e3c3c3c3!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1708561234567!5m2!1sen!2sus"
                className="absolute inset-0 w-full h-full border-0"
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
            <Button variant="outline" className="w-full md:w-auto" asChild>
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
        </div>
      </div>
    </div>
  )
}

