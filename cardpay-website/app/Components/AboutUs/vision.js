function VisionRibbon() {
    return (
        <>
            {/* <div className="card card-side bg-inherit rounded-none ">
                <img src="./assets/Vision.png" alt="Vision" style={{maxWidth:'35%', height:'auto'}} />
                <div className="card-body py-6 px-4">
                    <h2 className="card-title">Our Vision</h2>
                    <p className="text-xs text-left"> </p>
                    
                </div>
            </div> */}
            <div class="w-screen bg-white border border-gray-200 rounded-lg shadow mt-8">
                    <img class="rounded-t-lg" src="./assets/Vision.png" alt="" />
                <div class="p-5 bg-visionColor rounded-b-lg">
                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-white">Our Vision</h5>
                    <p class="mb-3 font-normal text-gray-100 ">We aim to provide financial power to every institution where banks have failed to do so.</p>
                </div>
            </div>
        </>
    )
}

export default VisionRibbon;