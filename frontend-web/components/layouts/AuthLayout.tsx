import { FC, ReactNode } from 'react';

export interface IAuthLayout {
	children: ReactNode;
}

const AuthLayout: FC<IAuthLayout> = ({ children }) => {
	return (
		<div className="min-h-screen flex flex-col justify-center">
			<div className="w-full mx-auto artboard phone-1 flex flex-col justify-center text-center">
				{children}
			</div>
		</div>
	);
};

export default AuthLayout;
