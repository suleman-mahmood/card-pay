import { FC, useState } from 'react';

import { useSelector } from 'react-redux';
import { selectUser } from '../../store/store';
import ContentLoader from 'react-content-loader';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRefresh } from '@fortawesome/free-solid-svg-icons';
import { httpsCallable } from 'firebase/functions';
import { functions } from '../../services/initialize-firebase';
import { FirebaseError } from 'firebase/app';
import Image from 'next/image';
import StudentCardImage from '../../assets/student_card.png';

const REFRESH_TIMEOUT = 30 * 1000;

interface IStudentCard {}

const StudentCard: FC<IStudentCard> = () => {
	const { userState } = useSelector(selectUser);

	const [refreshBalanceLoading, setRefreshBalanceLoading] = useState(false);

	const handleRefreshBalance = async () => {
		setRefreshBalanceLoading(true);
		setTimeout(() => {
			setRefreshBalanceLoading(false);
		}, REFRESH_TIMEOUT);

		const handleDepositSuccess = httpsCallable(
			functions,
			'handleDepositSuccess'
		);
		try {
			await handleDepositSuccess();
		} catch (error) {
			console.log((error as FirebaseError).message);
		}
	};

	return (
		<div className='card flex flex-row bg-white text-left shadow-xl'>
			{/* Heart card image */}
			<div className='ml-2 mt-2'>
				<Image className='rounded-xl' src={StudentCardImage} alt='' />
			</div>

			<div className='flex flex-col grow pl-2'>
				<div className='w-full pl-4 rounded-l-xl flex flex-col bg-primary text-white font-bold'>
					<h1 className='text-xl'>{userState.fullName}</h1>
					<h2 className='text-lg'>{userState.rollNumber}</h2>
				</div>
				<h2 className='text-lg font-bold'>
					PKR. {userState.balance}/-
				</h2>
				<h2 className='text-lg'>Available balance</h2>

				<h2 className='text-sm'>
					Refresh balance:
					<button onClick={handleRefreshBalance}>
						<FontAwesomeIcon className='ml-2' icon={faRefresh} />
					</button>
				</h2>

				<div className='h-10'></div>
			</div>

			{/* <h1>{userState.fullName}</h1>
			<h1>{userState.rollNumber}</h1>
			<h1>PKR. {userState.balance}/-</h1>
			<h1>Available balance</h1>
			{userState.pendingDeposits ? (
				refreshBalanceLoading ? (
					<ContentLoader viewBox='0 0 500 50'>
						<rect
							x='148.568'
							y='10'
							width='193.914'
							height='23.866'
						/>
					</ContentLoader>
				) : (
					<h1>
						Refresh balance:
						<button onClick={handleRefreshBalance}>
							<FontAwesomeIcon
								className='ml-2'
								icon={faRefresh}
							/>
						</button>
					</h1>
				)
			) : null} */}
		</div>
	);
};

export default StudentCard;
