function Traction() {
    return (
        <div className="mt-6 px-4">
            <h1 className="text-green-500 font-semibold text-3xl mb-4 text-left px-2">Our Traction</h1>
            <div className="grid grid-cols-2  ">
                {/* first post on users */}
                <div className="card w-full bg-gray-100 shadow-md h-max ">
                    <div className="card-body p-2 items-center">
                        <h1 className="card-title text-3xl text-center text-purple-700">2000+</h1>
                        <p className="text-black font-bold text-lg ">Users</p>
                    </div>
                </div>

                {/* second post on deposits */}
                <div className="card w-full bg-gray-100 shadow-md h-max ml-2">
                    <div className="card-body p-2 items-center">
                        <div className="flex flex-row items-end space-x-1">
                            <h1 className="card-title text-3xl text-center text-blue-500">2.5M</h1>
                            <p className="text-blue-500 font-bold">PKR</p>
                        </div>
                        <p className="text-black font-bold text-lg ">Deposits</p>
                    </div>
                </div>

                {/* Third post on vendors */}
                <div className="card w-full bg-gray-100 shadow-md h-max mt-2">
                    <div className="card-body p-2 items-center">
                        <h1 className="card-title text-3xl text-center text-green-400">17</h1>
                        <p className="text-black font-bold text-lg ">Vendors</p>
                    </div>
                </div>

                {/* Fourth post on Partners */}
                <div className="card w-full bg-gray-100 shadow-md h-max mt-2 ml-2">
                    <div className="card-body p-2 items-center">
                        <h1 className="card-title text-3xl text-center text-cyan-500">10+</h1>
                        <p className="text-black font-bold text-lg ">Partners</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Traction;
