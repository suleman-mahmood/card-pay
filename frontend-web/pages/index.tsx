import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import ButtonPrimary from '../components/buttons/ButtonPrimary';
import AuthLayout from '../components/layouts/AuthLayout';
import { auth } from '../services/initialize-firebase';

const Home: NextPage = () => {
	const router = useRouter();

	useEffect(() => {
		return auth.onAuthStateChanged(user => {
			if (user) {
				if (user.emailVerified) {
					router.push('/dashboard/');
				} else {
					router.push('/auth/student-verification');
				}
			}
		});
	}, []);

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
