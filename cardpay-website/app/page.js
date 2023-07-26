"use client";
import Layout from "./(layouts)/plainLayout"
import TopBanner from "./Components/HomePage/topBanner"
import Features from "./Components/HomePage/features";
import MyCarousel from "./Components/HomePage/partnerCarousal";
import Traction from "./Components/HomePage/traction";

export default function Home() {
  return (
    <Layout>
      <TopBanner />
      <Features />
      <Traction />
      <MyCarousel />
    </Layout>
  )
}
