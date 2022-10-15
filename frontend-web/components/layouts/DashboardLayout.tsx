import { useRouter } from 'next/router';
import { FC, ReactNode } from 'react';
import BottomNav from '../nav/BottomNav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPowerOff } from '@fortawesome/free-solid-svg-icons';
import { doc, getDoc } from 'firebase/firestore';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { auth, db } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';
import { setUserState, UserState } from '../../store/userSlice';
import ContentLoader from 'react-content-loader';

export interface IDashboardLayout {
	children: ReactNode;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children }) => {
	const router = useRouter();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
	};

	const { userState } = useSelector(selectUser);
	const dispatch = useDispatch();

	useEffect(() => {
		return auth.onAuthStateChanged(user => {
			if (user) {
				if (!user.emailVerified) {
					router.push('/auth/student-verification');
				} else {
					// User is logged in
					fetchUserData(user.uid);
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
		} else {
			console.log('Could not find user document');
		}
	};

	return (
		<div className="min-h-screen w-full px-8">
			<div className="w-full mx-auto flex flex-col text-center">
				<div className="h-8"></div>

				{userState.id === '' ? (
					<ContentLoader viewBox="0 0 500 250">
						<rect
							x="148.568"
							y="44.153"
							width="193.914"
							height="23.866"
						/>
						<rect
							x="198.687"
							y="78.162"
							width="96.659"
							height="23.27"
						/>
						<rect
							x="191.527"
							y="106.802"
							width="113.962"
							height="22.076"
						/>
						<rect
							x="166.468"
							y="139.021"
							width="161.098"
							height="21.48"
						/>
					</ContentLoader>
				) : (
					<div>
						<h1>{userState.fullName}</h1>
						<h1>{userState.rollNumber}</h1>
						<h1>PKR. {userState.balance}/-</h1>
						<h1>Available balance</h1>
					</div>
				)}

				<div className="flex-grow"></div>
				<div className="h-8"></div>
				<div className="overflow-y-auto">{children}</div>
				<div className="flex-grow"></div>
				<div className="h-24"></div>

				<button
					className="btn btn-outline absolute top-5 right-5"
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
