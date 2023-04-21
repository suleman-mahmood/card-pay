import {
	faIdCard,
	faLock,
	faMoneyBillTransfer,
	faPowerOff,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import Image from 'next/image';
import DepositIcon from '../../assets/deposit_icon.png';
import ChangePinIcon from '../../assets/change_pin_icon.png';

const raastaURL = 'https://raasta.com.pk/';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	const redirectToChangePin = () => {
		router.push('/dashboard/change-pin');
	};

	const redirectToDigitalCard = () => {
		router.push('/dashboard/digital-card');
	};

	const redirectToPreOrder = () => {
		router.push('/dashboard/pre-order');
	};

	return (
		<DashboardLayout>
			<div className='flex flex-col'>
				<div className='flex flex-row justify-around'>
					<div className='flex flex-col'>
						<button onClick={redirectToDeposit}>
							<div className='w-24 shadow-lg p-3 rounded-2xl'>
								<Image src={DepositIcon} alt='' />
							</div>
						</button>
						<h3 className='text-lg mt-1'>Deposit</h3>
					</div>

					<div className='flex flex-col'>
						<button onClick={redirectToChangePin}>
							<div className='w-24 shadow-lg p-4 rounded-2xl'>
								<Image src={ChangePinIcon} alt='' />
							</div>
						</button>
						<h3 className='text-lg'>Change Pin</h3>
					</div>
				</div>

				<div className='flex flex-row justify-around'>
					<div className='flex flex-col'>
						<button onClick={redirectToDigitalCard}>
							<div className='w-24 shadow-lg p-4 rounded-2xl'>
								<img src='https://i.ibb.co/5RYhN9P/Digi.png' />
							</div>
						</button>
						<h3 className='text-lg mt-1'>Digital Card</h3>
					</div>

					<div className='flex flex-col'>
						<button onClick={redirectToPreOrder}>
							<div className='w-24 shadow-lg p-4 rounded-2xl'>
								<img src='https://i.ibb.co/19m9pJg/preorder.png' />
							</div>
						</button>
						<h3 className='text-lg mt-1'>Pre Order</h3>
					</div>
				</div>

				<div className='flex flex-col items-center'>
					<a href={raastaURL} target='_blank'
						rel='noreferrer'
						className='flex flex-col items-center w-24 shadow-lg p-2 mt-2  rounded-2xl '>
						<img src='https://i.ibb.co/qMxxtV4/raasta.png' />
					</a>
					<h3 className='text-lg mt-1'>Raasta Trip</h3>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
