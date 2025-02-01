import { Header } from "@/components/header"
import { MainDishes } from "@/components/main-dishes"
import { DrinksList } from "@/components/drinks-list"
import { Footer } from "@/components/footer"

export default function MenuPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="w-full max-w-7xl mx-auto py-8">
        <MainDishes />
        <DrinksList />
      </div>
      <Footer />
    </main>
  )
}

