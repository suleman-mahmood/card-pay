import { FC, ReactNode } from 'react';
import BottomNav from '../nav/BottomNav';

export interface IDashboardLayout {
	children: ReactNode;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children }) => {
	return (
		<div className="min-h-screen flex flex-col justify-center">
			<div className="w-full mx-auto artboard phone-1 flex flex-col justify-center text-center">
				<h1>Student Name</h1>
				<h1>Roll Number</h1>
				<h1>PKR. 000.00/-</h1>
				<h1>Available balance</h1>

				<div className="flex-grow"></div>
				{children}
				<div className="flex-grow"></div>

				<BottomNav />
			</div>
		</div>
	);
};

export default DashboardLayout;
