import type { NextPage } from 'next';
import Router from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';

const Login: NextPage = () => {
	const router = Router;

	const redirectToSignup = () => {
		router.push('/auth/signup');
	};

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	return (
		<AuthLayout>
			<h1 className="text-2xl">Sign in to your account</h1>
			<h2 className="mb-4 text-xl">
				Don&apos;t have an account yet?
				<a
					className="ml-2 text-blue-500 text-xl"
					onClick={redirectToSignup}
				>
					Sign Up Now
				</a>
			</h2>

			<TextField placeholder="Roll Number" />
			<TextField placeholder="Password" />

			<ButtonPrimary onClick={redirectToDashboard} text="Log In" />
		</AuthLayout>
	);
};

export default Login;
