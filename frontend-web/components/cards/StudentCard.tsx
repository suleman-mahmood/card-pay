import { FC, useEffect, useState } from 'react';

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

	useEffect(() => {
		const refreshBalance = async () => {
			if (userState.pendingDeposits) {
				const handleDepositSuccess = httpsCallable(
					functions,
					'handleDepositSuccess'
				);
				try {
					await handleDepositSuccess();
				} catch (error) {
					console.log((error as FirebaseError).message);
				}
			}
		};
		refreshBalance();
	}, []);

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

	const showName = (): string => {
		const name = userState.fullName;
		const words = name.split(' ');
		if (words.length < 2) {
			return name;
		}
		return `${words[0]} ${words[1][0]}.`;
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
				<div className='w-full pl-2 flex flex-col bg-gradient-to-l from-primary to-primarydark text-white font-bold pr-5 mb-4'>
					<h1 className='text-xl'>{showName()}</h1>
					<h2 className='text-lg'>{userState.rollNumber}</h2>
				</div>
				<h1 className='text-xl text-black font-bold'>
					PKR. {userState.balance}/-
				</h1>
				<div className='flex flex-col'>
					<h6 className='text-sm text-black'>Available balance</h6>

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
							<h6 className='text-sm text-gray-500'>
								Refresh balance:
								<button onClick={handleRefreshBalance}>
									<FontAwesomeIcon
										className='ml-2'
										icon={faRefresh}
										size='sm'
									/>
								</button>
							</h6>
						)
					) : null}
				</div>

				<div className='h-10'></div>
			</div>
		</div>
	);
};

export default StudentCard;
