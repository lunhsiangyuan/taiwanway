import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { MainDishes } from "@/components/main-dishes"
import { DrinksList } from "@/components/drinks-list"

export default function MenuPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1 container mx-auto px-4 py-8">
        <MainDishes />
        <section id="drinks" className="mb-12 scroll-mt-20">
          <DrinksList />
        </section>
      </div>
      <Footer />
    </main>
  )
}

