import { createSlice } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';

type UserRole = 'student' | 'vendor' | 'admin';

export interface UserState {
	userState: {
		id: string;
		fullName: string;
		personalEmail: string;
		email: string;
		pendingDeposits: boolean;
		pin: string;
		phoneNumber: string;
		rollNumber: string;
		verified: boolean;
		role: UserRole;
		balance: number;
		transactions: Array<{
			amount: number;
			id: string;
			recipientName: string;
			senderName: string;
			status: string;
			timestamp: string;
		}>;
	};
}

const initialState: UserState = {
	userState: {
		id: '',
		fullName: '',
		personalEmail: '',
		email: '',
		pendingDeposits: false,
		pin: '',
		phoneNumber: '',
		rollNumber: '',
		verified: false,
		role: 'student',
		balance: 0,
		transactions: [],
	},
};

export const userSlice = createSlice({
	name: 'user',
	initialState,
	reducers: {
		setUserState(state, action) {
			state.userState = action.payload;
		},
	},
	extraReducers: {
		[HYDRATE]: (state, action) => {
			return {
				...state,
				...action.payload.user,
			};
		},
	},
});

export const { setUserState } = userSlice.actions;
