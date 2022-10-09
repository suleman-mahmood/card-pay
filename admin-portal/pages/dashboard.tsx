import { onAuthStateChanged } from 'firebase/auth';
import { collection, getDocs, query, where } from 'firebase/firestore';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Loader from '../components/loader';
import { auth, db } from '../services/initialize-firebase';

const ADMIN_UID = 'JoNhydNzAWXGilGS4fRsOK1ePTm2';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(false);

	useEffect(() => {
		const fetchData = async () => {
			const ref = db.collection('users');
			const q = ref.where('balance', '>=', '1000');
			const querySnapshot = await q.get();

			console.log(querySnapshot);
		};

		// fetchData();
	}, []);

	return loading ? <Loader /> : <h1>Dashboard</h1>;
};

export default Dashboard;
