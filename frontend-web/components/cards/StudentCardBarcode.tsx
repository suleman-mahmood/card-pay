import { FC } from 'react';

import { useSelector } from 'react-redux';
import { selectUser } from '../../store/store';
import Image from 'next/image';
import StudentCardImage from '../../assets/student_card.png';
import Barcode from 'react-barcode';

const REFRESH_TIMEOUT = 30 * 1000;

interface IStudentCard {}

const StudentCard: FC<IStudentCard> = () => {
	const { userState } = useSelector(selectUser);

	const showName = (): string => {
		const name = userState.fullName;
		const words = name.split(' ');
		if (words.length < 2) {
			return '';
		}
		return `${words[0]} ${words[1][0]}.`;
	};

	return (
		<div className='card flex flex-col items-center bg-white shadow-xl my-4 mx-2 mt-16 overflow-visible'>
			<div className='flex flex-row'>
				{/* Heart card image */}
				<div className='ml-3 w-32 -translate-y-16'>
					<Image
						className='shadow-md bg-white rounded-2xl'
						src={StudentCardImage}
						alt=''
					/>
				</div>

				<div className='flex flex-col pl-6 pt-6'>
					<div className='w-full  px-2 text-left flex flex-col bg-gradient-to-l from-primary to-primarydark text-white font-bold '>
						<h1 className='text-xl'>{showName()}</h1>
						<h2 className='text-lg'>{userState.rollNumber}</h2>
					</div>
				</div>
			</div>
			<div className='-translate-y-8'>
				<Barcode
					value={`11${userState.rollNumber}`}
					width={2.5}
					height={50}
					displayValue={false}
				/>
			</div>
		</div>
	);
};

export default StudentCard;
