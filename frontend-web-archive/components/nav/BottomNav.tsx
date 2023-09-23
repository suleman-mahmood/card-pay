import { useRouter } from 'next/router';
import { FC } from 'react';

interface IBottomNav {}

const BottomNav: FC<IBottomNav> = () => {
	const router = useRouter();

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	const redirectToTransfer = () => {
		router.push('/dashboard/transfer');
	};

	const redirectToTransactions = () => {
		router.push('/dashboard/transactions');
	};

	// const redirectToProfile = () => {
	// 	router.push('/dashboard/profile');
	// };

	return (
		<div className='btm-nav rounded-t-3xl bg-gradient-to-l from-primary to-primarydark text-white'>
			<button
				className={
					router.pathname === '/dashboard' ? 'text-secondary' : ''
				}
				onClick={redirectToDashboard}
			>
				<svg
					xmlns='http://www.w3.org/2000/svg'
					className='h-5 w-5'
					fill='none'
					viewBox='0 0 24 24'
					stroke='white'
				>
					<path
						strokeLinecap='round'
						strokeLinejoin='round'
						strokeWidth='2'
						d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'
					/>
				</svg>
				<span className='btm-nav-label'>Dashboard</span>
			</button>
			<button
				className={
					router.pathname === '/dashboard/transfer'
						? 'text-secondary'
						: ''
				}
				onClick={redirectToTransfer}
			>
				<svg
					xmlns='http://www.w3.org/2000/svg'
					className='h-5 w-5'
					fill='none'
					viewBox='0 0 24 24'
					stroke='white'
				>
					<path
						strokeLinecap='round'
						strokeLinejoin='round'
						strokeWidth='2'
						d='M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
					/>
				</svg>
				<span className='btm-nav-label'>Transfer</span>
			</button>
			<button
				className={
					router.pathname === '/dashboard/transactions'
						? 'text-secondary'
						: ''
				}
				onClick={redirectToTransactions}
			>
				<svg
					xmlns='http://www.w3.org/2000/svg'
					className='h-5 w-5'
					fill='none'
					viewBox='0 0 24 24'
					stroke='white'
				>
					<path
						strokeLinecap='round'
						strokeLinejoin='round'
						strokeWidth='2'
						d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
					/>
				</svg>
				<span className='btm-nav-label'>Transactions</span>
			</button>
			{/* <button
				className={
					router.pathname === '/dashboard/profile'
						? 'text-secondary'
						: ''
				}
				onClick={redirectToProfile}
			>
				<svg xmlns="http://www.w3.org/2000/svg" 
					width="30" height="30" 
					viewBox="0 0 32 32">
						<g fill="none" stroke="white" 
							stroke-linejoin="round" 
							stroke-miterlimit="10" 
							stroke-width="2">
								<circle cx="16" cy="16" r="15"/>
									<path d="M26 27c0-5.523-4.477-10-10-10S6 21.477 6 27"/>
								<circle cx="16" cy="11" r="6"/>
						</g>
				</svg>
				<span className='btm-nav-label'>Profile</span>
			</button> */}
		</div>
	);
};

export default BottomNav;
