import Header from "../components/Header"
import "../globals.css"

export default function DashboardLayout({ children }: {
  children: React.ReactNode
}) {
  return (
    <section>
      <Header />
      {children}
    </section>
  )
}