import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
	faChevronUp,
	faChevronDown,
	faSquare,
} from '@fortawesome/free-solid-svg-icons';
import { useRouter } from 'next/router';
import { faqs } from '../../assets/faqs';
import BackButton from '../../components/buttons/BackButton';
import AuthLayout from '../../components/layouts/AuthLayout';

const FAQPage = () => {
	const [activeIndex, setActiveIndex] = useState<number | null>(null);
	const router = useRouter();

	const toggleDropdown = (index: number) =>
		setActiveIndex(activeIndex === index ? null : index);

	return (
		<AuthLayout>
			<h1 className='text-2xl mb-4 text-primarydark font-bold text-center'>
				FAQs
			</h1>

			<div className='space-y-2'>
				{faqs.map((faq, index) => (
					<div
						key={index}
						className='border rounded-md overflow-hidden'
					>
						<div
							className='bg-gradient-to-l from-primary to-primarydark text-white px-4 py-3 cursor-pointer'
							onClick={() => toggleDropdown(index)}
						>
							<div className='flex justify-between items-center'>
								<p className='text-lg font-semibold text-left'>
									{faq.question}
								</p>
								<FontAwesomeIcon
									icon={
										activeIndex === index
											? faChevronUp
											: faChevronDown
									}
									className='text-md text-white'
								/>
							</div>
						</div>
						{activeIndex === index && (
							<div className='p-2 bg-white text-sm text-left'>
								<p>{faq.answer}</p>
							</div>
						)}
					</div>
				))}
			</div>

			<BackButton textColor='text-blue-500' />
		</AuthLayout>
	);
};

export default FAQPage;
