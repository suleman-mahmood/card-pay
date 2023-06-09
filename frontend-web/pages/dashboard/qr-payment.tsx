import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import BackButton from '../../components/buttons/BackButton';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';
import QrReader from 'react-qr-scanner';
import { useRouter } from 'next/router';
import SuccessAlert from '../../components/cards/SuccessAlert';

const CHARACTERS_IN_UID = 28;

const Deposit: NextPage = () => {
	const router = useRouter();

	const [amount, setAmount] = useState(0);
	const { userState } = useSelector(selectUser);

	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const [iAmRendered, setIAmRendered] = useState(false);

	const [isModalOpen, setIsModalOpen] = useState(false);
	const [recipientUid, setRecipientUid] = useState('');

	useEffect(() => {
		setIAmRendered(true);
	}, []);

	const handlePaymentSend = async () => {
		if (amount <= 0) {
			setErrorMessage('Please enter an amount greater than 0');
			return;
		} else if (userState.id === '') {
			setErrorMessage('Please refresh the page');
			return;
		} else if (recipientUid.length !== CHARACTERS_IN_UID) {
			setErrorMessage('Wrong QR code');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const makeQRTransaction = httpsCallable(functions, 'makeQRTransaction');
		try {
			await makeQRTransaction({
				amount: amount,
				recipientUid: recipientUid,
			});

			setIsLoading(false);
			setErrorMessage('');
			setSuccessMessage('QR Payment sent successfully');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	const handleAmountChange = (n: number) => {
		setAmount(n);
	};

	const onScan = (data: any) => {
		if (data === null) return;
		if (data.text.length !== CHARACTERS_IN_UID) return;

		setRecipientUid(data.text);
		setIsModalOpen(true);
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='text-2xl'>Pay with QR</h1>
			<h2 className='mb-4 text-xl'>Scan QR below to pay</h2>

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			{iAmRendered ? (
				<QrReader
					delay={100}
					style={{
						height: 240,
						width: 320,
					}}
					onError={(e: any) => console.log(e)}
					onScan={onScan}
				/>
			) : null}

			{/* Open the modal using ID.showModal() method */}
			<dialog className={'modal ' + (isModalOpen ? 'modal-open' : '')}>
				<form method='dialog' className='modal-box'>
					<h3 className='mb-4 font-bold text-lg'>Enter amount</h3>
					<TextField
						placeholder='0000'
						type='number'
						valueSetter={handleAmountChange}
					/>

					<div
						className='modal-action'
						onClick={() => setIsModalOpen(false)}
					>
						<button
							className='btn btn-primary'
							onClick={handlePaymentSend}
						>
							Send!
						</button>
						<button
							className='btn btn-error'
							onClick={() => router.back()}
						>
							Cancel
						</button>
					</div>
				</form>
			</dialog>

			<BackButton />
		</DashboardLayout>
	);
};

export default Deposit;
