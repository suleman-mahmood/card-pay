
function Banner() {


    const images = [
        "./assets/aboutUsBanner/photo1.png",
        "./assets/aboutUsBanner/photo2.png",
        "./assets/aboutUsBanner/photo3.png",
        "./assets/aboutUsBanner/photo4.png",
    ]

    return (
        <div className="hero w-screen bg-lightBlue bg-opacity-60 flex flex-col px-4 items-center py-2">
            <div className="hero-content text-center grid grid-cols-2 grid-rows-2 ">
                <img src={images[0]} className="rounded-2xl shadow-md border-2 border-gray-100"  />
                <img src={images[1]} className="rounded-2xl shadow-md border-2 border-gray-100" />
                <img src={images[3]} className="rounded-2xl shadow-md border-2 border-gray-100" />
                <img src={images[2]} className="rounded-2xl shadow-md border-2 border-gray-100" />
            </div>
            <h1 className="text-black font-semibold text-xl">CardPay</h1>
            <h2 className="text-gray-700 font-medium">Solving the unsolved Problems</h2>
        </div>
    )


}

export default Banner;
