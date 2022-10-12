import { useRouter } from 'next/router';
import { FC, ReactNode } from 'react';
import { auth } from '../../services/initialize-firebase';
import BottomNav from '../nav/BottomNav';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPowerOff } from '@fortawesome/free-solid-svg-icons';

export interface IDashboardLayout {
	children: ReactNode;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children }) => {
	const router = useRouter();

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
	};

	return (
		<div className="min-h-screen w-full px-8">
			<div className="w-full mx-auto flex flex-col text-center">
				<div className="h-8"></div>

				<h1>Student Name</h1>
				<h1>Roll Number</h1>
				<h1>PKR. 000.00/-</h1>
				<h1>Available balance</h1>

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
