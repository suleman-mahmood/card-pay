import { FC, ReactNode } from 'react';
import BottomNav from '../nav/BottomNav';

export interface IDashboardLayout {
	children: ReactNode;
}

const DashboardLayout: FC<IDashboardLayout> = ({ children }) => {
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
				<BottomNav />
			</div>
		</div>
	);
};

export default DashboardLayout;
