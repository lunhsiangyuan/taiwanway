import { Clock, MapPin, Phone } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Contact() {
  return (
    <section className="py-20 bg-secondary">
      <div className="container">
        <h2 className="text-3xl font-bold text-center mb-12">來找我們 Visit Us</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-3xl mx-auto">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <MapPin className="h-8 w-8 text-primary" />
            </div>
            <h3 className="font-semibold mb-2">地址 Location</h3>
            <p className="text-muted-foreground">26 South St, Middletown NY</p>
          </div>
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <Clock className="h-8 w-8 text-primary" />
            </div>
            <h3 className="font-semibold mb-2">營業時間 Hours</h3>
            <p className="text-muted-foreground">週一、二、五、六</p>
            <p className="text-muted-foreground">11:00 AM - 7:00 PM</p>
          </div>
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <Phone className="h-8 w-8 text-primary" />
            </div>
            <h3 className="font-semibold mb-2">聯絡我們 Contact</h3>
            <p className="text-muted-foreground">845-381-1002</p>
            <p className="text-muted-foreground">usamyheish@gmail.com</p>
          </div>
        </div>
        <div className="mt-12 text-center">
          <Button size="lg" className="bg-primary hover:bg-primary/90">
            立即訂位 Make a Reservation
          </Button>
        </div>
      </div>
    </section>
  )
}

