import { GetMe } from '@/api/gelios.api';
import { User } from "../api/gelios.types"
import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext<User | null>(null);

interface AuthUserProviderProps {
  children: React.ReactNode;
}

export const UserProvider = ({ children }: AuthUserProviderProps ) => {
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    async function GetCurrentUser() {
      const userResponse = await GetMe()
      setUser(userResponse.data)
    }
    GetCurrentUser();
  }, []);
  return (
    <UserContext.Provider value={user}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
