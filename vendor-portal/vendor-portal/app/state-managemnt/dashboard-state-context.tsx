'use client'
import { createContext, useContext, useState, FC, ReactNode } from 'react';
type DashboardContextType = {
  amount: number;
  setAmount: (amount: number) => void;
  rollNumber: number;
  setRollNumber: (rollNumber: number) => void;
  errorMessage: string;
  setErrorMessage: (errorMessage: string) => void;
  shouldFocus: boolean;
  setShouldFocus: (shouldFocus: boolean) => void;
  order: {
    [uid: string]: {
      orderId: string;
      cart: Array<{
        restaurantId: string;
        name: string;
        price: number;
        quantity: number;
      }>;
      specialInstructions: string;
      isDelivery: boolean;
      customerName: string;
      customerRollNumber: string;
      contactNumber: string;
      deliveryAddress: string;
      timestamp: number;
    };
  } | null;
  setOrder: (order: { [uid: string]: any } ) => void;
};

const DashboardContext = createContext<DashboardContextType | null>(null);

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};

type DashboardProviderProps = {
  children: ReactNode;
};

export const DashboardProvider: FC<DashboardProviderProps> = ({ children }) => {
  const [amount, setAmount] = useState(0);
  const [rollNumber, setRollNumber] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');
  const [shouldFocus, setShouldFocus] = useState(true);
  const [order, setOrder] = useState<{
    [uid: string]: {
      orderId: string;
      cart: Array<{
        restaurantId: string;
        name: string;
        price: number;
        quantity: number;
      }>;
      specialInstructions: string;
      isDelivery: boolean;
      customerName: string;
      customerRollNumber: string;
      contactNumber: string;
      deliveryAddress: string;
      timestamp: number;
    };
  } | null>(null);

  const value = {
    amount,
    setAmount,
    rollNumber,
    setRollNumber,
    errorMessage,
    setErrorMessage,
    shouldFocus,
    setShouldFocus,
    order,
    setOrder,
  };

  return <DashboardContext.Provider value={value}>{children}</DashboardContext.Provider>;
};
