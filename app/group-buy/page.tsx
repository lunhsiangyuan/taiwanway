import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { GroupBuy } from "@/components/GroupBuy"

export default function GroupBuyPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="pt-4">
        <GroupBuy />
      </div>
      <Footer />
    </main>
  )
}
