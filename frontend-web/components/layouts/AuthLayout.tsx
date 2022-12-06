import { useRouter } from 'next/router';
import { FC, ReactNode, useEffect } from 'react';
import { auth } from '../../services/initialize-firebase';

export interface IAuthLayout {
	children: ReactNode;
}

const AuthLayout: FC<IAuthLayout> = ({ children }) => {
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

	return (
		<div className='min-h-screen flex flex-col justify-center'>
			<div className='w-full mx-auto artboard phone-1 flex flex-col justify-center text-center'>
				{children}
			</div>
		</div>
	);
};

export default AuthLayout;
