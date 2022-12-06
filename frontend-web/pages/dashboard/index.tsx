import {
	faLock,
	faMoneyBillTransfer,
	faPowerOff,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	const redirectToChangePin = () => {
		router.push('/dashboard/change-pin');
	};

	return (
		<DashboardLayout>
			<div className='flex flex-col'>
				<div className='flex flex-row justify-around'>
					<div className='flex flex-col'>
						<button onClick={redirectToDeposit}>
							<FontAwesomeIcon
								className='h-14 p-4 bg-primary rounded-xl text-white shadow-xl'
								icon={faMoneyBillTransfer}
							/>
						</button>
						<h3 className='text-xl'>Deposit</h3>
					</div>

					<div className='flex flex-col'>
						<button onClick={redirectToChangePin}>
							<FontAwesomeIcon
								className='h-14 p-4 bg-primary rounded-xl text-white shadow-xl'
								icon={faLock}
							/>
						</button>
						<h3 className='text-xl'>Change Pin</h3>
					</div>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
