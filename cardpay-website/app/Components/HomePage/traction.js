import { useEffect, useState, useRef } from "react";

function Traction() {

    const [counter, setCounter] = useState(1);
    const elementRef = useRef(null);
    const [magic, setMagic] = useState(true);

    const handleScroll = () => {
        const element = elementRef.current;
        if (!magic) {
            return;
        }
        if (element) {
            const { top, bottom } = element.getBoundingClientRect();
            const isInView = top >= 0 && bottom <= window.innerHeight;
            if (isInView && magic) {
                // Calculate the number of increments and the duration for 10 seconds
                const totalIncrements = 20;
                const totalDurationMs = 2500; // 10 seconds
                const incrementValue = 1;
                const incrementDuration = totalDurationMs / totalIncrements;

                // Helper function to update the counter smoothly
                const updateCounterSmoothly = (currentIncrement) => {
                    setCounter(currentIncrement * incrementValue);
                };

                // Start the smooth animation
                let currentIncrement = 1;
                const interval = setInterval(() => {
                    updateCounterSmoothly(currentIncrement);
                    currentIncrement += 1;
                    if (currentIncrement > totalIncrements) {
                        clearInterval(interval);
                    }
                }, incrementDuration);
                setMagic(false);
            }
        }
    };



    useEffect(() => {
        // Call handleScroll on the initial render to check if the element is already in view
        handleScroll();

        // Add the event listener to update the counter when the element comes into view while scrolling
        window.addEventListener('scroll', handleScroll);

        // Clean up the event listener on component unmount
        return () => window.removeEventListener('scroll', handleScroll);
    }, [magic]);


    return (
        <div className="p-4">
            <h1 className="text-green-500 font-semibold text-3xl mb-4 text-left px-2">Our Traction</h1>
            <div id="traction" ref={elementRef} className="stats stats-vertical  bg-white lg:stats-horizontal shadow">
                <div className="stat">
                    <div className="stat-value text-purple-700">{100 * counter}+</div>
                    <div className="stat-desc text-black text-base">users</div>
                </div>

                <div className="stat">
                    <div className="stat-value text-blue-700">{(0.125 * counter).toFixed(2)}M</div>
                    <div className="stat-desc text-black text-base">Deposits</div>
                </div>

                <div className="stat">
                    <div className="stat-value text-green-700">{counter}</div>
                    <div className="stat-desc text-black text-base">Vendors</div>
                </div>

            </div>
        </div>
        
    )
}

export default Traction;
