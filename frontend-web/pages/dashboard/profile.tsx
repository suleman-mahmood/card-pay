import type { NextPage } from 'next';
import { useSelector } from 'react-redux';
import { selectUser } from '../../store/store';

import { useEffect, useState } from 'react';
import BackButton from '../../components/buttons/BackButton';
import ErrorAlert from '../../components/cards/ErrorAlert';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import TextField from '../../components/inputs/signup_text_field';

const DigitalCard: NextPage = () => {
	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const { userState } = useSelector(selectUser);
	const [reference, setReferenceNumber] = useState('');

	const already_present = () => {
		if (userState.phoneNumber.length === 0) {
			return true;
		}
		return false;
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout displayCard={true}>
			<div className='flex flex-col mb-6 '>
				<div className='grid grid-cols-1 place-items-center mt-5'>
					<h2 className=' bg-white rounded-2xl text-primarydark placeholder-primary w-full max-w-xs pl-4 pb-3 pt-3 mb-5 shadow-lg focus:bg-gray-100 text-left '>
						Email: {userState.email}
					</h2>
					<h2 className=' bg-white rounded-2xl text-primarydark placeholder-primary w-full max-w-xs pl-4 pb-3 pt-3 mb-5 shadow-lg focus:bg-gray-100 text-left items-'>
						Phone Number: {userState.phoneNumber}
					</h2>
				</div>

				{already_present() ? (
					<form className='form-control w-full items-center'>
						<TextField
							type='text'
							valueSetter={setReferenceNumber}
							placeholder='Reference Roll Number'
						/>
					</form>
				) : (
					<div className='grid grid-cols-1 place-items-center'>
						<h2 className=' bg-white rounded-2xl text-primarydark placeholder-primary w-full max-w-xs pl-4 pb-3 pt-3 mb-4 shadow-lg focus:bg-gray-100 text-left items-'>
							Phone Number: {userState.phoneNumber}
						</h2>
					</div>
				)}

				<ErrorAlert message={errorMessage} />
				<BackButton />
			</div>
		</DashboardLayout>
	);
};

export default DigitalCard;
