import EventHeader from "@/app/components/EventHeader"

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