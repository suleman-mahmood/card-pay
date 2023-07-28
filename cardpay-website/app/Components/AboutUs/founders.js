function Founders() {
    return (
        <div className="mt-8 px-4 w-screen">

            <h1 className="text-2xl text-left mb-4 text-blue-800 font-semibold">Our Founding Team</h1>

            <div className="card bg-transparent shadow-xl">
                <figure><img src="/assets/Tayyab.jpeg" alt="Tayyab" /></figure>
                <div className="card-body text-black items-center">
                    <h2 className="card-title">Tayyab Rashad</h2>
                    <p>LUMS 23" BSc ACF</p>
                </div>
            </div>

            <div className="card bg-transparent shadow-xl mt-4">
                <figure><img src="/assets/Suleman.jpg" alt="Suleman" /></figure>
                <div className="card-body text-black items-center">
                    <h2 className="card-title">Suleman Mahmood</h2>
                    <p>LUMS 23" BSc CS</p>
                </div>
            </div>

            <div className="card bg-transparent shadow-xl mt-4">
                <figure><img src="/assets/Shamsi.jpg" alt="Shamsi" /></figure>
                <div className="card-body text-black items-center">
                    <h2 className="card-title w-max">Abdul Rehman Shamsi</h2>
                    <p>LUMS 23" BSc MGS</p>
                </div>
            </div>

        </div>
    )
}

export default Founders;