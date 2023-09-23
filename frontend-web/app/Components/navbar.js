'use client';
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";


const navBar = () => {

    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    const redirectToAboutUs = () => {
        router.push('/aboutUs');
    }

    const logout = () => {
        auth.signOut();
        router.push('/login');
    }

    const dashboard = () => {
        router.push('/');
    }

    const [sticky, setSticky] = useState(false);
    const [navBgColor, setNavBgColor] = useState('bg-lightBlue');
    const [shadow, setShadow] = useState('shadow-sm');

    const handleStickyNavbar = () => {
        if (window.scrollY >= 80) {
            setSticky(true);
            setNavBgColor('bg-white');
            setShadow('shadow-md')
        } else {
            setSticky(false);
            setNavBgColor('bg-lightBlue');
            setShadow('shadow-sm');
        }
    };

    useEffect(() => {
        window.addEventListener("scroll", handleStickyNavbar);
        return () => {
            window.removeEventListener("scroll", handleStickyNavbar);
        };
    }, []);


    return (
        <div className={`sticky top-0 z-50 ${navBgColor}`}>
            <div className={`navbar ${shadow} px-2 text-black`}>
                <div className="grid grid-cols-3 items-center">
                    <img src='./assets/logo.svg' style={{ maxWidth: '35%', height: 'auto' }} ></img>
                    <div onClick={dashboard} className="text-2xl items-center font-bold text-blue-800 mx-auto p-2 ">
                        <a>CardPay</a>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end' }} className={`dropdown dropdown-bottom dropdown-end items-center ${isOpen ? 'open' : ''}  `}>
                        <label tabIndex={0} className="btn btn-square btn-ghost" onClick={toggleDropdown}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block w-6 h-6 stroke-current"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
                        </label>
                        {isOpen && (
                            <ul tabIndex={0} className="text-black dropdown-content z-[1] menu p-2 shadow-sm bg-white w-max rounded-md mt-2 ">
                                <li onClick={redirectToAboutUs}><a>About us</a></li>
                                <hr />
                                <li><a>Meet our Team</a></li>
                                <hr />
                                <li><a>Signing up</a></li>
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )



};

export default navBar;