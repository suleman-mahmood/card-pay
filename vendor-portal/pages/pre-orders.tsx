import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import TextField from '../components/text-field';
import { auth, db, functions } from '../services/initialize-firebase';
import { User as FirebaseUser } from 'firebase/auth';
import Navbar from '../components/navbar';
import { httpsCallable } from 'firebase/functions';
import Swal from 'sweetalert2';
import Loader from '../components/loader';
import {
	collection,
	doc,
	getDoc,
	getDocs,
	query,
	where,
} from 'firebase/firestore';

enum ORDER_STATUS_ENUM {
	pending = 'pending',
	confirmed = 'confirmed',
	denied = 'denied',
	expired = 'expired',
	insufficient_funds = 'insufficient_funds',
}

interface PreOrdersDoc {
	userUid: string;
	orderId: string;
	cart: Array<{
		restaurantId: string;
		name: string;
		price: number;
		quantity: number;
	}>;
	status: ORDER_STATUS_ENUM;
	restaurantId: string;
	specialInstructions: string;
	isDelivery: boolean;
	customerName: string;
	customerRollNumber: string;
	contactNumber: string;
	deliveryAddress: string;
}

const Transactions: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);
	const [preOrders, setPreOrders] = useState<Array<PreOrdersDoc> | null>(
		null
	);

	useEffect(() => {
		return onAuthStateChanged(auth, (user) => {
			if (user) {
				console.log(user.uid);
				fetchPreOrders(user.uid);
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchPreOrders = async (uid: string) => {
		const colRef = collection(db, 'pre-orders');
		const q = query(colRef, where('restaurantId', '==', uid));
		const querySnapshot = await getDocs(q);

		if (querySnapshot.empty) {
			console.log('Could not find user document');
		} else {
			const docs = querySnapshot.docs.map(
				(d) => d.data() as PreOrdersDoc
			);
			setPreOrders(docs);
		}

		setLoading(false);
	};

	const formatTimestamp = (timestamp: string): string => {
		const date = new Date(timestamp);
		const options: Intl.DateTimeFormatOptions = {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: 'numeric',
			minute: 'numeric',
		};

		return date.toLocaleDateString('en-US', options);
	};

	return loading ? (
		<Loader />
	) : (
		<div className='min-h-screen flex flex-col'>
			<Navbar />
			<div className='hero flex-grow'>
				<div className='w-full hero-content text-center'>
					<div className='w-full'>
						<h1 className='mb-4 text-5xl font-bold'>Pre Orders</h1>

						<h2 className='text-2xl my-4'>Delivery orders</h2>
						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Customer Name</th>
										<th>Customer Roll Number</th>
										<th>Cart</th>
										<th>Contact Number</th>
										<th>Delivery Address</th>
										<th>Special Instructions</th>
									</tr>
								</thead>
								<tbody>
									{preOrders
										?.filter((v) => v.isDelivery)
										.map((v, i) => (
											<tr key={i}>
												<th>{v.customerName}</th>
												<th>{v.customerRollNumber}</th>
												<th>
													{v.cart.map((items, i) => (
														<p key={i}>
															{items.name}:{' '}
															{items.quantity}
														</p>
													))}
												</th>
												<th>{v.contactNumber}</th>
												<th>{v.deliveryAddress}</th>
												<th>{v.specialInstructions}</th>
												{/* <th>
													{formatTimestamp(
														v.timestamp
													)}
												</th> */}
											</tr>
										))}
								</tbody>
							</table>
						</div>

						<h2 className='text-2xl my-4'>Pickup orders</h2>
						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Customer Name</th>
										<th>Customer Roll Number</th>
										<th>Cart</th>
										<th>Special Instructions</th>
									</tr>
								</thead>
								<tbody>
									{preOrders
										?.filter((v) => !v.isDelivery)
										.map((v, i) => (
											<tr key={i}>
												<th>{v.customerName}</th>
												<th>{v.customerRollNumber}</th>
												<th>
													{v.cart.map((items, i) => (
														<p key={i}>
															{items.name}:{' '}
															{items.quantity}
														</p>
													))}
												</th>
												<th>{v.specialInstructions}</th>
												{/* <th>
													{formatTimestamp(
														v.timestamp
													)}
												</th> */}
											</tr>
										))}
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Transactions;
