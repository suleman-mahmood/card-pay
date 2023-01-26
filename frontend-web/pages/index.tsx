import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import WelcomeLayout from '../components/layouts/WelcomeLayout';
import Image from 'next/image';


const Home: NextPage = () => {
	const router = useRouter();

	const redirectToAuth = () => {
		router.push('auth/login');
	};

	return (
		<WelcomeLayout>
			<div className='flex flex-col'>
				<div className='flex flex-row justify-around'>
					<div className='flex flex-col'>
							<div className='w-28'>
								<img src="https://i.ibb.co/6yGMFSW/Whats-App-Image-2022-08-06-at-4-35-23-PM-removebg-preview.png" alt="logo" className='shadow-sm'></img>
							</div>
					</div>
				</div>
			</div>
			<h1 className='mb-1 mt-2 text-4xl font-semibold'>Welcome to CardPay</h1>
			<h2 className='mb-4 text-xl'>
				Revolutionize your campus experience
			</h2>
			<button className='bg-white rounded-full shadow-lg text-primarydark text-2xl font-bold py-2' onClick={redirectToAuth}>Continue</button>
		</WelcomeLayout>
	);
};

export default Home;
