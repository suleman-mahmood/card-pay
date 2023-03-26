import { createSlice } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';

export interface CartState {
	cartState: {
		itemsCount: number;
	};
}

const initialState: CartState = {
	cartState: {
		itemsCount: 0,
	},
};

export const cartSlice = createSlice({
	name: 'cart',
	initialState,
	reducers: {
		setItemsCount(state, action) {
			state.cartState.itemsCount = action.payload;
		},
		incrementItemsCount(state) {
			state.cartState.itemsCount += 1;
		},
		decrementItemsCount(state) {
			state.cartState.itemsCount -= 1;
		},
	},
	extraReducers: {
		[HYDRATE]: (state, action) => {
			return {
				...state,
				...action.payload.cart,
			};
		},
	},
});

export const { setItemsCount, incrementItemsCount, decrementItemsCount } =
	cartSlice.actions;
