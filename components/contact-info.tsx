import { Card, CardContent } from "@/components/ui/card"
import { MapPin, Clock, Phone } from "lucide-react"

export function ContactInfo() {
  return (
    <section className="py-20">
      <div className="container">
        <h2 className="text-4xl font-bold text-center mb-4">與我們聯繫 Get in Touch</h2>
        <p className="text-center text-muted-foreground max-w-2xl mx-auto mb-12">
          歡迎蒞臨品嚐我們的美食，或透過電話、電子郵件與我們聯繫。我們期待為您服務！
        </p>
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <MapPin className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-xl mb-2">地址 Location</h3>
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
                <h3 className="font-semibold text-xl mb-2">營業時間 Hours</h3>
                <p className="text-muted-foreground">週一、二、五、六</p>
                <p className="text-muted-foreground">11:00 AM - 7:00 PM</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Phone className="h-8 w-8 text-primary" />
                </div>
                <h3 className="font-semibold text-xl mb-2">聯絡方式 Contact</h3>
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

