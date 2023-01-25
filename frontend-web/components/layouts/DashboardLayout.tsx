import { useRouter } from 'next/router';
import { FC, ReactNode, useState } from 'react';
import BottomNav from '../nav/BottomNav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPowerOff, faRefresh } from '@fortawesome/free-solid-svg-icons';
import { doc, getDoc } from 'firebase/firestore';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { auth, db, functions } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';
import { setUserState, UserState } from '../../store/userSlice';
import ContentLoader from 'react-content-loader';
import { httpsCallable } from 'firebase/functions';
import { FirebaseError } from 'firebase/app';
import StudentCard from '../cards/StudentCard';

export interface IDashboardLayout {
	children: ReactNode;
	displayCard?: boolean;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children, displayCard }) => {
	const router = useRouter();

	const { userState } = useSelector(selectUser);
	const dispatch = useDispatch();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
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
			const data = docSnap.data() as UserState;
			dispatch(setUserState(data));

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

				{userState.id === '' ? (
					<ContentLoader viewBox='0 0 500 250'>
						<rect
							x='148.568'
							y='44.153'
							width='193.914'
							height='23.866'
						/>
						<rect
							x='198.687'
							y='78.162'
							width='96.659'
							height='23.27'
						/>
						<rect
							x='191.527'
							y='106.802'
							width='113.962'
							height='22.076'
						/>
						<rect
							x='166.468'
							y='139.021'
							width='161.098'
							height='21.48'
						/>
					</ContentLoader>
				) : displayCard === undefined ? (
					<StudentCard />
				) : displayCard ? (
					<StudentCard />
				) : null}

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
