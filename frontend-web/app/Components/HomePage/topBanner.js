import { useEffect, useState } from "react";


function Banner() {
    const androidUrl = "market://details?id=io.payment.cardpay";
    const iOSUrl = "https://apps.apple.com/app/id1644127078";

    const [appLink, setAppLink] = useState(androidUrl);

    useEffect(() => {
        if (window == null) {
            return;
        }
        const os = getOS();

        if (os === "Android") {
            setAppLink(androidUrl);
        }
        else if (os === "iOS") {
            setAppLink(iOSUrl);
        }
    }, []);

    const getOS = () => {
        var userAgent = window.navigator.userAgent,
            platform = window.navigator?.userAgentData?.platform || window.navigator.platform,
            macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
            windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
            iosPlatforms = ['iPhone', 'iPad', 'iPod'],
            os = null;

        if (macosPlatforms.indexOf(platform) !== -1) {
            os = 'Mac OS';
        } else if (iosPlatforms.indexOf(platform) !== -1) {
            os = 'iOS';
        } else if (windowsPlatforms.indexOf(platform) !== -1) {
            os = 'Windows';
        } else if (/Android/.test(userAgent)) {
            os = 'Android';
        } else if (/Linux/.test(platform)) {
            os = 'Linux';
        }

        return os;
    }

    const handleInstallClick = () => {
        if (window == null) {
            return;
        }
        window.location.assign(appLink);
    }

    return (
        <div className="hero min-h bg-lightBlue items-start">
            <div className="hero-content text-center flex flex-col">
                <h1 className="text-black font-medium text-2xl px-2">Smart,Secure & Quick Payments</h1>
                <h3 className="text-gray-500 text-sm px-1">Your solution for all payments Anywhere, Anytime</h3>
                <h3 className="text-gray-500 text-sm px-1">We have moved to mobile app, install it now!</h3>
                <href onClick={handleInstallClick} className="btn btn-sm rounded-full border-none text-white bg-purple-500 px-4 py-1 text-md font-semibold">
                    Get CardPay
                </href>
                <img src="./assets/mockup.png" />
            </div>
        </div>
    )


}

export default Banner;
