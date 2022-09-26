import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Loader from '../components/loader';
import { auth } from '../services/initialize-firebase';

const ADMIN_UID = 'BiTFuz2mntexVphn69WfApeFoqq2';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);

	useEffect(() => {
		onAuthStateChanged(auth, user => {
			if (user) {
				if (user.uid !== ADMIN_UID) {
					router.push('/');
					return;
				}

				// Handle success
				setLoading(false);
			} else {
				// User is signed out
				router.push('/');
			}
		});
	}, []);

	return loading ? <Loader /> : <h1>Dashboard</h1>;
};

export default Dashboard;
