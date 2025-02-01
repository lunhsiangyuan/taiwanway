import Link from "next/link"
import { Facebook, Instagram, Twitter, Mail, Phone } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-secondary/30 border-t">
      <div className="w-full px-4 md:px-6 lg:px-8 max-w-screen-2xl mx-auto py-8 pb-16 md:py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-semibold mb-4">快速連結 Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-muted-foreground hover:text-primary">
                  首頁 Home
                </Link>
              </li>
              <li>
                <Link href="/menu" className="text-muted-foreground hover:text-primary">
                  菜單 Menu
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-muted-foreground hover:text-primary">
                  關於我們 About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-primary">
                  聯絡我們 Contact
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-4">營業時間 Hours</h3>
            <p className="text-muted-foreground">週一、二、五、六</p>
            <p className="text-muted-foreground">11:00 AM - 7:00 PM</p>
          </div>
          <div>
            <h3 className="font-semibold mb-4">聯絡我們 Contact</h3>
            <p className="text-muted-foreground">26 South St, Middletown NY</p>
            <p className="text-muted-foreground">845-381-1002</p>
            <p className="text-muted-foreground">usamyheish@gmail.com</p>
          </div>
          <div className="pb-6 md:pb-0">
            <h3 className="font-semibold mb-4">關注我們 Follow Us</h3>
            <div className="flex flex-wrap gap-4">
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Facebook className="h-6 w-6" />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Instagram className="h-6 w-6" />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Twitter className="h-6 w-6" />
              </a>
              <a href="mailto:usamyheish@gmail.com" className="text-muted-foreground hover:text-primary">
                <Mail className="h-6 w-6" />
              </a>
              <a href="tel:845-381-1002" className="text-muted-foreground hover:text-primary">
                <Phone className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t text-center text-muted-foreground">
          <p>&copy; 2025 Taiwanway. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

