import Image, { StaticImageData } from 'next/image';
import { useRouter } from 'next/router';
import { FC } from 'react';

interface IRestaurantCard {
	id: string;
	title: string;
	description: string;
	bgImage: StaticImageData;
}

const RestaurantCard: FC<IRestaurantCard> = ({
	id,
	bgImage,
	title,
	description,
}) => {
	const router = useRouter();

	const redirectToMenu = () => {
		const href = `/dashboard/pre-order/${id}`;
		router.push(href);
	};

	return (
		<div className='card bg-base-100 shadow-xl image-full'>
			<figure>
				<Image src={bgImage} />
			</figure>
			<div className='card-body'>
				<h2 className='card-title'>{title}</h2>
				<p className='text-left'>{description}</p>
				<div className='card-actions justify-end'>
					<button
						className='btn btn-primary'
						onClick={redirectToMenu}
					>
						Menu
					</button>
				</div>
			</div>
		</div>
	);
};

export default RestaurantCard;
