import EventHeader from "@/app/components/EventHeader"
import "../../globals.css"

export default function DashboardLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {
  return (
    <section>
      <EventHeader />

      {children}
    </section>
  )
}