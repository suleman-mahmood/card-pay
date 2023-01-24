import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import Barcode from 'react-barcode';
import BackButton from '../../components/buttons/BackButton';
import ErrorAlert from '../../components/cards/ErrorAlert';
import StudentCardBarcode from '../../components/cards/StudentCardBarcode';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';

const DigitalCard: NextPage = () => {
	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout displayCard={false}>
			<div className='flex flex-col'>
				<div className='h-28'></div>
				<StudentCardBarcode />

				{/* <Barcode
					value='barcode-example'
					width={0.005 * 0.7 * screen.width}
					displayValue={false}
				/> */}
				<ErrorAlert message={errorMessage} />
				<BackButton />
			</div>
		</DashboardLayout>
	);
};

export default DigitalCard;
