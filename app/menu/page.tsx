import { Header } from "@/components/header"
import { Snacks } from "@/components/snacks"
import { MainDishes } from "@/components/main-dishes"
import { Desserts } from "@/components/desserts"
import { DrinksList } from "@/components/drinks-list"
import { Footer } from "@/components/footer"

export default function MenuPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="w-full max-w-7xl mx-auto py-8">
        <Snacks />
        <MainDishes />
        <Desserts />
        <DrinksList />
      </div>
      <Footer />
    </main>
  )
}

