import { doc, getDoc } from 'firebase/firestore';
import { useRouter } from 'next/router';
import { FC, ReactNode, useEffect } from 'react';
import { auth, db } from '../../services/initialize-firebase';
import { UserState } from '../../store/userSlice';

export interface IAuthLayout {
	children: ReactNode;
}

const WelcomeLayout: FC<IAuthLayout> = ({ children }) => {
	const router = useRouter();

	useEffect(() => {
		return auth.onAuthStateChanged(async (user) => {
			if (user) {
				const docRef = doc(db, 'users', user.uid);
				const docSnap = await getDoc(docRef);
				if (!docSnap.exists()) {
					console.log('No user document found');
					return;
				}
				const data = docSnap.data()!;

				if (data.verified) {
					router.push('/dashboard/');
				} else {
					router.push('/auth/student-verification');
				}
			}
		});
	}, []);

	return (
		<div className='min-h-screen bg-gradient-to-l from-primary to-primarydark flex flex-col justify-center'>
			<div className='w-full mx-auto artboard phone-1 flex flex-col justify-center text-white text-center'>
				{children}
			</div>

			{/* <footer className='footer absolute bottom-0 p-4 bg-neutral text-neutral-content'>
				<div className='w-full grid-flow-col text-center'>
					<div className='w-full flex flex-row justify-center'>
						<p className='mr-1'>Made with ❤️ by</p>
						<a
							href='https://www.linkedin.com/in/sulemanmahmood/'
							className='underline font-bold'
							target='_blank'
							rel='noreferrer'
						>
							Suleman
						</a>
					</div>
				</div>
			</footer> */}
		</div>
	);
};

export default WelcomeLayout;
