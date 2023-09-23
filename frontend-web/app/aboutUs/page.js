"use client";
import PlainLayout from "../(layouts)/plainLayout"
import Banner from "../Components/AboutUs/banner";
import Story from "../Components/AboutUs/story";
import Vision from "../Components/AboutUs/vision"
import Founders from "../Components/AboutUs/founders";
import MyCarousel from "../Components/HomePage/partnerCarousal";


export default function Home() {
  return (
    <PlainLayout>
        <Banner />
        <Story />
        <Vision />
        <Founders />
        <MyCarousel />
    </PlainLayout>
  )
}