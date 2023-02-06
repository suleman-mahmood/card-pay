import { useRouter } from 'next/router';
import { FC, ReactNode, useState } from 'react';
import BottomNav from '../nav/BottomNav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPowerOff } from '@fortawesome/free-solid-svg-icons';
import { doc, getDoc } from 'firebase/firestore';
import { useEffect } from 'react';
import { auth, db, functions } from '../../services/initialize-firebase';

export interface IDashboardLayout {
	children: ReactNode;
	displayCard?: boolean;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children, displayCard }) => {
	const router = useRouter();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/');
	};

	useEffect(() => {
		return auth.onAuthStateChanged(async user => {
			if (user) {
				// User is logged in
				const verified = await fetchUserData(user.uid);

				if (!verified) {
					router.push('/auth/student-verification');
				}
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchUserData = async (uid: string) => {
		const docRef = doc(db, 'users', uid);
		const docSnap = await getDoc(docRef);

		if (docSnap.exists()) {
			// const data = docSnap.data() as UserState;
			// dispatch(setUserState(data));

			return docSnap.data().verified;
		} else {
			console.log('Could not find user document');
			return false;
		}
	};

	return (
		<div className='min-h-screen w-full px-8'>
			<div className='w-full mx-auto flex flex-col text-center'>
				{/* Top margin */}
				<div className='h-28'></div>

				{/* Blue top */}
				<div className='h-52 w-full bg-gradient-to-l from-primary to-primarydark absolute top-0 left-0 -z-10'></div>

				<div className='flex-grow'></div>
				<div className='h-8'></div>
				<div className='overflow-y-auto'>{children}</div>
				<div className='flex-grow'></div>
				<div className='h-24'></div>

				<button
					className='btn btn-outline absolute top-4 right-8 text-white'
					onClick={redirectToLogin}
				>
					<FontAwesomeIcon icon={faPowerOff} />
				</button>

				<BottomNav />
			</div>
		</div>
	);
};

export default DashboardLayout;
