import { useRouter } from 'next/navigation';
import { FC, ReactNode, useState } from 'react';
import { doc, getDoc, onSnapshot } from 'firebase/firestore';
import { useEffect } from 'react';
import { auth, db, functions } from '../../services/initialize-firebase';
import { User } from 'firebase/auth';

// TODO, use redux for state management

export interface IDashboardLayout {
	children: ReactNode;
	displayCard?: boolean;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children, displayCard }) => {
	const router = useRouter();

	const [user, setUser] = useState<User>();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/');
	};

	useEffect(() => {
		return auth.onAuthStateChanged(async (user) => {
			if (user) {
				setUser(user);
			} else {
				redirectToLogin();
			}
		});
	}, []);

	useEffect(() => {
		if (!user) {
			return;
		}
		return onSnapshot(doc(db, 'users', user.uid), (doc) => {
			console.log('Current data: ', doc.data());
		});
	}, [user]);

	return <div className='min-h-screen w-full'>{children}</div>;
};

export default DashboardLayout;