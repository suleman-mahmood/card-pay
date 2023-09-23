import { httpsCallable } from 'firebase/functions';
import { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BoxLoading from '../components/loaders/BoxLoading';
import { auth, functions } from '../services/initialize-firebase';

// url: http://localhost:3000/raasta?rollNumber=23100011&amount=100&fullName=Suleman%20Mahmood&phoneNumber=03333462677

const Raasta: NextPage = () => {
	const router = useRouter();

	const [creatingRequest, setCreatingRequest] = useState(false);

	useEffect(() => {
		auth.signOut();

		if (Object.keys(router.query).length === 0) {
			return;
		}

		console.log(router.query);

		if (
			router.query.rollNumber === undefined ||
			router.query.amount === undefined
		) {
			return;
		}

		if (creatingRequest) {
			return;
		}

		setCreatingRequest(true);
		checkRollNumber();
	}, [router]);

	const checkRollNumber = async () => {
		const rollNumber = router.query.rollNumber as string;
		const amount = router.query.amount as string;

		const checkRollNumberExists = httpsCallable(
			functions,
			'checkRollNumberExists'
		);
		try {
			const { data } = await checkRollNumberExists({
				rollNumber: rollNumber,
			});

			const userExists = (data as any).userExists;

			if (userExists) {
				// Goto deposit page on PayPro

				const addRaastaDepositRequest = httpsCallable(
					functions,
					'addRaastaDepositRequest'
				);
				try {
					const { data } = await addRaastaDepositRequest({
						amount: amount,
						rollNumber: rollNumber,
					});

					const url = (data as any).paymentUrl;
					window.location.href = url;
				} catch (error) {
					console.log(error);
				}
			} else {
				// Goto signup page with pre-filled fields
				router.push({
					pathname: '/auth/signup',
					query: { ...router.query, isRaastaPayment: 'true' },
				});
			}
		} catch (error) {
			console.log(error);
		}
	};

	return <BoxLoading />;
};

export default Raasta;
