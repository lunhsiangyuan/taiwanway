'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import { Phone, Mail, Clock, Users, PartyPopper, Gift } from 'lucide-react'
import { Card } from '@/components/ui/card'

const cateringMenuItems = [
  {
    name: { zh: '牛肉麵派對盤 (10人份)', en: 'Beef Noodle Soup Tray (10 servings)', es: 'Bandeja de Sopa de Fideos con Res (10 porciones)' },
  },
  {
    name: { zh: '滷肉飯派對盤 (10人份)', en: 'Braised Pork Rice Tray (10 servings)', es: 'Bandeja de Arroz con Cerdo Guisado (10 porciones)' },
  },
  {
    name: { zh: '珍珠奶茶派對組 (12杯)', en: 'Bubble Tea Party Pack (12 cups)', es: 'Paquete de Fiesta de Té de Burbujas (12 vasos)' },
  },
  {
    name: { zh: '鳳梨酥綜合禮盒 (12入)', en: 'Assorted Pineapple Cake Box (12 pcs)', es: 'Caja de Pasteles de Piña Surtidos (12 pzas)' },
  },
  {
    name: { zh: '綜合茶飲組合 (6杯, 6種口味)', en: 'Mixed Tea Sampler (6 cups, 6 flavors)', es: 'Muestrario de Té Mixto (6 vasos, 6 sabores)' },
  },
]

const serviceCards = [
  {
    icon: Users,
    title: { zh: '企業團餐', en: 'Corporate Catering', es: 'Catering Corporativo' },
    description: {
      zh: '10人以上，可客製化菜單。適合公司會議、員工聚餐、商務活動。',
      en: '10+ people, custom menu available. Perfect for meetings, team lunches & corporate events.',
      es: 'Más de 10 personas, menú personalizado. Ideal para reuniones, almuerzos y eventos corporativos.',
    },
  },
  {
    icon: PartyPopper,
    title: { zh: '派對套餐', en: 'Party Packages', es: 'Paquetes de Fiesta' },
    description: {
      zh: '生日派對、慶祝活動、家庭聚會。精心搭配的套餐讓派對更完美。',
      en: 'Birthdays, celebrations & family gatherings. Curated packages to make your party perfect.',
      es: 'Cumpleaños, celebraciones y reuniones familiares. Paquetes seleccionados para tu fiesta perfecta.',
    },
  },
  {
    icon: Gift,
    title: { zh: '節慶團購', en: 'Holiday Group Buy', es: 'Compras Grupales Festivas' },
    description: {
      zh: '中秋月餅禮盒、農曆新年年菜、感恩節特餐。提前預訂享優惠。',
      en: 'Mid-Autumn mooncakes, Lunar New Year feast, Thanksgiving specials. Pre-order for best prices.',
      es: 'Pasteles de luna, banquete de Año Nuevo Lunar, especiales de Acción de Gracias. Reserve con anticipación.',
    },
  },
]

const sectionText = {
  heroTitle: { zh: '企業團餐 & 團購服務', en: 'Catering & Group Orders', es: 'Catering y Pedidos Grupales' },
  heroDescription: {
    zh: '從公司聚餐到節慶派對，TaiwanWay 為您量身打造道地台灣美食盛宴。',
    en: 'From corporate lunches to holiday parties, TaiwanWay crafts authentic Taiwanese feasts tailored for your event.',
    es: 'Desde almuerzos corporativos hasta fiestas navideñas, TaiwanWay prepara auténticos banquetes taiwaneses para su evento.',
  },
  servicesTitle: { zh: '我們的服務', en: 'Our Services', es: 'Nuestros Servicios' },
  menuTitle: { zh: '團餐菜單精選', en: 'Catering Menu Highlights', es: 'Destacados del Menú de Catering' },
  menuNote: {
    zh: '以上為熱門品項，更多選擇歡迎來電洽詢。可依需求客製化菜單。',
    en: 'These are our popular picks. Contact us for more options. Custom menus available upon request.',
    es: 'Estos son nuestros platos populares. Contáctenos para más opciones. Menús personalizados disponibles.',
  },
  contactTitle: { zh: '預約團餐', en: 'Book Your Catering', es: 'Reserve su Catering' },
  contactNote: {
    zh: '請提前 3 天聯繫我們，以便準備最新鮮的食材。',
    en: 'Contact us 3 days in advance so we can prepare the freshest ingredients.',
    es: 'Contáctenos con 3 días de anticipación para preparar los ingredientes más frescos.',
  },
  phone: { zh: '電話', en: 'Phone', es: 'Teléfono' },
  email: { zh: '電子郵件', en: 'Email', es: 'Correo Electrónico' },
  advanceNotice: { zh: '提前預訂', en: 'Advance Notice', es: 'Aviso Previo' },
  threeDays: {
    zh: '請於活動前 3 天預約',
    en: 'Please book 3 days before your event',
    es: 'Reserve 3 días antes de su evento',
  },
}

export function CateringPage() {
  const { language } = useLanguage()

  const getText = (textObj: Record<string, string>) =>
    textObj[language] || textObj.en

  return (
    <div className="min-h-screen">
      {/* Hero 區塊 */}
      <section className="relative bg-[#2D1810] pt-32 pb-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-[#2D1810]" />
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <p className="font-body text-sm font-medium uppercase tracking-[0.3em] text-[hsl(44,80%,60%)] mb-4">
            TaiwanWay
          </p>
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
            {getText(sectionText.heroTitle)}
          </h1>
          <p className="font-body text-lg text-white/70 max-w-2xl mx-auto leading-relaxed">
            {getText(sectionText.heroDescription)}
          </p>
        </div>
      </section>

      {/* 服務卡片區塊 */}
      <section className="py-20 bg-[#FAF7F2] px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-[#2D1810] text-center mb-12">
            {getText(sectionText.servicesTitle)}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {serviceCards.map((card) => {
              const Icon = card.icon
              return (
                <Card
                  key={card.title.en}
                  className="p-8 bg-white border border-[hsl(30,15%,85%)] hover:shadow-lg transition-shadow duration-300"
                >
                  <div className="flex items-center justify-center w-14 h-14 rounded-full bg-[hsl(44,80%,40%)]/10 mb-6">
                    <Icon className="h-7 w-7 text-[hsl(44,80%,40%)]" />
                  </div>
                  <h3 className="font-heading text-xl font-bold text-[#2D1810] mb-3">
                    {getText(card.title)}
                  </h3>
                  <p className="font-body text-[hsl(17,20%,40%)] leading-relaxed">
                    {getText(card.description)}
                  </p>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* 團餐菜單精選區塊 */}
      <section className="py-20 bg-white px-4">
        <div className="max-w-3xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-[#2D1810] text-center mb-12">
            {getText(sectionText.menuTitle)}
          </h2>
          <div className="space-y-0">
            {cateringMenuItems.map((item, index) => (
              <div
                key={item.name.en}
                className={`py-5 ${
                  index < cateringMenuItems.length - 1 ? 'border-b border-[hsl(30,15%,85%)]' : ''
                }`}
              >
                <span className="font-body text-[#2D1810] text-base md:text-lg">
                  {getText(item.name)}
                </span>
              </div>
            ))}
          </div>
          <div className="mt-10 text-center p-6 bg-[hsl(44,80%,40%)]/10 rounded-xl">
            <p className="font-heading text-lg font-semibold text-[#2D1810] mb-2">
              {getText({ zh: '價格請私訊或來電洽詢', en: 'Contact us for pricing', es: 'Contáctenos para precios' })}
            </p>
            <p className="font-body text-sm text-[hsl(17,20%,40%)]">
              {getText({ zh: '📞 845-381-1002 ｜ ✉️ taiwanway10940@gmail.com', en: '📞 845-381-1002 ｜ ✉️ taiwanway10940@gmail.com', es: '📞 845-381-1002 ｜ ✉️ taiwanway10940@gmail.com' })}
            </p>
          </div>
          <p className="font-body text-sm text-[hsl(17,20%,40%)] text-center mt-6 leading-relaxed">
            {getText(sectionText.menuNote)}
          </p>
        </div>
      </section>

      {/* 聯繫預約區塊 */}
      <section className="py-20 bg-[#2D1810] px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-white mb-6">
            {getText(sectionText.contactTitle)}
          </h2>
          <p className="font-body text-white/70 mb-12 text-lg leading-relaxed max-w-xl mx-auto">
            {getText(sectionText.contactNote)}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* 電話 */}
            <div className="flex flex-col items-center gap-3">
              <div className="flex items-center justify-center w-12 h-12 rounded-full bg-white/10">
                <Phone className="h-5 w-5 text-[hsl(44,80%,60%)]" />
              </div>
              <h3 className="font-body font-semibold text-white text-sm uppercase tracking-wider">
                {getText(sectionText.phone)}
              </h3>
              <a
                href="tel:845-381-1002"
                className="font-body text-white/70 hover:text-white transition-colors"
              >
                845-381-1002
              </a>
            </div>

            {/* Email */}
            <div className="flex flex-col items-center gap-3">
              <div className="flex items-center justify-center w-12 h-12 rounded-full bg-white/10">
                <Mail className="h-5 w-5 text-[hsl(44,80%,60%)]" />
              </div>
              <h3 className="font-body font-semibold text-white text-sm uppercase tracking-wider">
                {getText(sectionText.email)}
              </h3>
              <a
                href="mailto:taiwanway10940@gmail.com"
                className="font-body text-white/70 hover:text-white transition-colors"
              >
                taiwanway10940@gmail.com
              </a>
            </div>

            {/* 提前預訂 */}
            <div className="flex flex-col items-center gap-3">
              <div className="flex items-center justify-center w-12 h-12 rounded-full bg-white/10">
                <Clock className="h-5 w-5 text-[hsl(44,80%,60%)]" />
              </div>
              <h3 className="font-body font-semibold text-white text-sm uppercase tracking-wider">
                {getText(sectionText.advanceNotice)}
              </h3>
              <p className="font-body text-white/70">
                {getText(sectionText.threeDays)}
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
