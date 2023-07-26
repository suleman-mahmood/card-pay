function Features() {
    return (
        <div className="hero min-h bg-white items-start mt-8">
            <div className="hero-content text-center flex flex-col">

                {/* Pay at vendors one */}
                <div className="card w-full bg-inherit shadow-sm">
                    <div className="card-body text-black p-2">
                        <div className="flex flex-row">
                            <h2 className="card-title mr-2">Pay at vendors</h2>
                            <img src="./assets/flyingArrow.png" style={{ maxWidth: '35%', height: 'auto', marginTop: '-30px' }} />
                        </div>
                        <p className="text-xs text-left text-gray-700">
                            Experience the Ease of CardPay!
                            Pay conveniently at your favorite places with multiple payment options like QR codes and cards.
                            No worries, just smooth transactions!
                        </p>
                        <div className="card-actions justify-end">
                        </div>
                    </div>
                </div>

                {/* Features Event Registeration */}
                <div className="card w-full bg-inherit shadow-sm mt-4 rounded-sm">
                    <figure><img src="./assets/eventRegisteration.png" alt="events" /></figure>
                    <h3 className="card-title text-black w-max px-2 mt-2 font-medium text-base">Event Registerations</h3>
                    <div className="card-body p-2">
                        <p className="text-gray-700 text-xs text-left">
                            Streamline your life with CardPay! No more juggling multiple channels for registrations and payments. 
                            We've got you covered with a seamless process in one place!
                        </p>
                    </div>
                </div>



                {/* Features Fees Collection */}
                <div className="card w-full bg-inherit shadow-sm mt-4 rounded-sm ">
                    <figure><img src="./assets/maskeenSchool.png" alt="events" /></figure>
                    <h3 className="card-title text-black w-max px-2 mt-2 font-medium text-base">Fees Payment</h3>
                    <div className="card-body p-2">
                        <p className="text-gray-700 text-xs text-left">
                            Are you tired of managing fees from multiple channels? 
                            Say hello to CardPay - the simple solution for collecting & Managing fees through one channel! No more hassle, just seamless payments!
                        </p>
                    </div>
                </div>

                {/* Features Pre Order */}
                <div className="card w-full bg-inherit shadow-sm mt-20 rounded-sm">
                    <figure className="bg-lightBlue overflow-visible rounded-md"><img src="./assets/preOrder.png" style={{  maxWidth: '65%', height: 'auto', marginTop:'-100px' }}  alt="events" /></figure>
                    <h3 className="card-title text-black w-max px-2 mt-2 font-medium text-base">Pre Order Food</h3>
                    <div className="card-body p-2">
                        <p className="text-gray-700 text-xs text-left">
                        Restaurant app giving you a headache? 
                        Say hello to CardPay - your all-in-one ecommerce and delivery channel, right within your institute! Simplify your restaurant business with CardPay today!
                        </p>
                    </div>
                </div>

                {/* Features Discount Deals */}
                <div className="card w-full bg-inherit shadow-sm mt-4 rounded-sm">
                    <figure><img src="./assets/discountDeals.png" style={{  maxWidth: '65%', height: 'auto' }}  alt="events" /></figure>
                    <h3 className="card-title text-black w-max px-2 mt-2 font-medium text-base">Exclusive Discounts</h3>
                    <div className="card-body p-2">
                        <p className="text-gray-700 text-xs text-left">
                        Get Exclusive CardPay discount deals alongside lucrative cashback deals. Have the biggest savings in your institute with CardPay.
                        </p>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default Features;