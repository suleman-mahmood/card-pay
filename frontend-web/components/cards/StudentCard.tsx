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
		<div className='card flex flex-row bg-white text-left shadow-xl relative h-48 overflow-visible'>
			{/* Heart card image */}
			<div className='absolute left-2 bottom-16 w-28'>
				<Image
					className='shadow-md bg-white rounded-2xl'
					src={StudentCardImage}
					alt=''
				/>
			</div>

			<div className='flex flex-col grow pl-2 absolute right-0 bottom-0 top-10'>
				<div className='w-full pl-4  flex flex-col bg-gradient-to-l from-primary to-primarydark text-white font-bold pr-5 mb-4'>
					<h1 className='text-xl'>{userState.fullName}</h1>
					<h2 className='text-lg'>{userState.rollNumber}</h2>
				</div>
				<h1 className='text-xl text-black font-bold'>
					PKR. {userState.balance}/-
				</h1>
				<div className='flex flex-row space-x-5'>
					<h6 className='text-sm text-black'>Available balance</h6>
					<button onClick={handleRefreshBalance}>
						<FontAwesomeIcon
							className='ml-2'
							icon={faRefresh}
							size='sm'
						/>
					</button>
				</div>

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
