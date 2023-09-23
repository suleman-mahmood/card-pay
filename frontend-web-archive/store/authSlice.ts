import { createSlice } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';

export interface AuthState {
	authState: boolean;
}

const initialState: AuthState = {
	authState: true,
};

export const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		setAuthState(state, action) {
			state.authState = action.payload;
		},
	},
	extraReducers: {
		[HYDRATE]: (state, action) => {
			return {
				...state,
				...action.payload.auth,
			};
		},
	},
});

export const { setAuthState } = authSlice.actions;
