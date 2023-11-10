import React from 'react'
import EventHeader from '../../components/EventHeader'
import "../../global.css"

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