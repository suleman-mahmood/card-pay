import type { NextPage } from 'next';
import Router from 'next/router';
import ButtonPrimary from '../components/buttons/ButtonPrimary';
import AuthLayout from '../components/layouts/AuthLayout';

const Home: NextPage = () => {
	const router = Router;

	const redirectToAuth = () => {
		router.push('auth/login');
	};

	return (
		<AuthLayout>
			<h1 className="mb-4 text-2xl text-primary">Welcome to CardPay</h1>
			<h2 className="mb-4 text-xl text-primary font-semibold">
				Revolutionize your campus experience
			</h2>
			<ButtonPrimary onClick={redirectToAuth} text="Continue!" />
		</AuthLayout>
	);
};

export default Home;
