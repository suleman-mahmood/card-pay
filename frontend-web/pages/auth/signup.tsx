import type { NextPage } from 'next';
import Router from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';

const Signup: NextPage = () => {
	const router = Router;

	const redirectToLogin = () => {
		router.push('/auth/login');
	};

	const redirectToStudentVerification = () => {
		router.push('/auth/student-verification');
	};

	return (
		<AuthLayout>
			<h1 className="text-2xl">Create your account</h1>
			<h2 className="mb-4 text-xl">
				Do you already have an account?
				<a
					className="ml-2 text-blue-500 text-xl"
					onClick={redirectToLogin}
				>
					Sign In Now
				</a>
			</h2>

			<TextField placeholder="Full Name" />
			<TextField placeholder="Roll Number" />
			<TextField placeholder="Password" />
			<TextField placeholder="Confirm Password" />
			<TextField placeholder="4-digit pin" />
			<TextField placeholder="Confirm 4-digit pin" />

			<ButtonPrimary
				onClick={redirectToStudentVerification}
				text="Sign Up"
			/>
		</AuthLayout>
	);
};

export default Signup;
