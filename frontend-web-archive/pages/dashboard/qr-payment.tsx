import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import BackButton from '../../components/buttons/BackButton';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';
import { useRouter } from 'next/router';
import SuccessAlert from '../../components/cards/SuccessAlert';
import QrScanner from 'qr-scanner';

const CHARACTERS_IN_UID = 28;

const Deposit: NextPage = () => {
	const router = useRouter();

	const [amount, setAmount] = useState(0);
	const { userState } = useSelector(selectUser);

	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [isModalOpen, setIsModalOpen] = useState(false);
	const [recipientUid, setRecipientUid] = useState('');

	useEffect(() => {
		if (document === null) return;

		const videoElem = document.querySelector('video');
		if (videoElem === null) return;

		// To enforce the use of the new api with detailed scan results, call the constructor with an options object, see below.
		const qrScanner = new QrScanner(
			videoElem,
			(result) => {
				if (result.data.length !== CHARACTERS_IN_UID) return;

				setRecipientUid(result.data);
				setIsModalOpen(true);
			},
			{
				/* your options or returnDetailedScanResult: true if you're not specifying any other options */
			}
		);

		qrScanner.start();
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

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='text-2xl'>Pay with QR</h1>
			<h2 className='mb-4 text-xl'>Scan QR below to pay</h2>

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			<video></video>

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
