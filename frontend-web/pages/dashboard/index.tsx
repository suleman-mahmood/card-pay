import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import Image from 'next/image';
import DepositIcon from '../../assets/deposit_icon.png';
import ChangePinIcon from '../../assets/change_pin_icon.png';
import { httpsCallable } from 'firebase/functions';
import { functions } from '../../services/initialize-firebase';
import ErrorAlert from '../../components/cards/ErrorAlert';
import SuccessAlert from '../../components/cards/SuccessAlert';
import { useState } from 'react';
import BoxLoading from '../../components/loaders/BoxLoading';
import { FirebaseError } from 'firebase/app';

const raastaURL = 'https://raasta.com.pk/';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

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

	const handleFarewellPayment = async () => {
		setIsLoading(true);

		const makeFarewellTransaction = httpsCallable(
			functions,
			'makeFarewellTransaction'
		);
		try {
			await makeFarewellTransaction();

			setIsLoading(false);
			setErrorMessage('');
			setSuccessMessage('Farewell payment successful!');
		} catch (error) {
			setIsLoading(false);
			setSuccessMessage('');
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<div className='flex flex-col'>
				<ErrorAlert message={errorMessage} />
				<SuccessAlert message={successMessage} />

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
			</div>

			{/* Put this part before </body> tag */}
			<input type='checkbox' id='my-modal' className='modal-toggle' />
			<div className='modal'>
				<div className='modal-box'>
					<h3 className='font-bold text-lg'>Farewell payment</h3>
					<p className='py-4'>
						Are you sure you want to pay <b>Rs.2550</b> for the
						farewell payment?
					</p>
					<div className='modal-action'>
						<label
							htmlFor='my-modal'
							className='btn bg-gradient-to-l from-primary to-primarydark text-white border-none'
							onClick={handleFarewellPayment}
						>
							Abosulutely!
						</label>
						<label
							htmlFor='my-modal'
							className='btn bg-gradient-to-l from-primary to-primarydark text-white border-none'
						>
							Still thinking :/
						</label>
					</div>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
