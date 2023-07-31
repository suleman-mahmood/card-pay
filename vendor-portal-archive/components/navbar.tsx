import { signOut } from 'firebase/auth';
import { useRouter } from 'next/router';
import React from 'react';
import { auth } from '../services/initialize-firebase';

export default function Navbar() {
	const router = useRouter();

	const handleLogout = () => {
		signOut(auth);
	};

	return (
		<div className='navbar bg-base-100 py-4 px-8'>
			<div className='flex-1'>
				<a
					onClick={() => router.push('/dashboard')}
					className='btn btn-ghost normal-case text-xl'
				>
					CardPay
				</a>
			</div>
			<div className='flex-none'>
				<button
					className='btn btn-primary mr-4'
					onClick={() => router.push('/pre-orders')}
				>
					Pre-orders
				</button>
				<button
					className='btn btn-primary mr-4'
					onClick={() => router.push('/transactions')}
				>
					Transactions
				</button>
				<button className='btn btn-accent' onClick={handleLogout}>
					Logout
				</button>
			</div>
		</div>
	);
}
