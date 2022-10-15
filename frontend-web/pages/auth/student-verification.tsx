import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import AuthLayout from '../../components/layouts/AuthLayout';
import { auth } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
	};

	return (
		<AuthLayout>
			<h1 className="text-2xl">Verification link sent on email</h1>
			<h2 className="mb-4 text-xl">
				Click the link in the email sent to your Lums Outlook&apos;s
				inbox
			</h2>

			<ButtonPrimary onClick={redirectToLogin} text="Proceed to login" />
		</AuthLayout>
	);
};

export default Login;
