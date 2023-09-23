import { configureStore, ThunkAction } from '@reduxjs/toolkit';
import { Action } from 'redux';
import { createWrapper } from 'next-redux-wrapper';
import { authSlice } from './authSlice';
import { userSlice } from './userSlice';
import { cartSlice } from './cartSlice';

const makeStore = () =>
	configureStore({
		reducer: {
			[authSlice.name]: authSlice.reducer,
			[userSlice.name]: userSlice.reducer,
			[cartSlice.name]: cartSlice.reducer,
		},
		devTools: true,
	});

export type AppStore = ReturnType<typeof makeStore>;
export type AppState = ReturnType<AppStore['getState']>;
export type AppThunk<ReturnType = void> = ThunkAction<
	ReturnType,
	AppState,
	unknown,
	Action
>;

export const wrapper = createWrapper<AppStore>(makeStore);

export const selectAuth = (state: AppState) => state.auth.authState;
export const selectUser = (state: AppState) => state.user;
export const selectCart = (state: AppState) => state.cart;
