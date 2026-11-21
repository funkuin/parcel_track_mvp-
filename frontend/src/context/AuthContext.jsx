import React, { createContext, useContext, useMemo, useState } from 'react';

const STORAGE_KEY = 'parceltrack-session';
export const DEMO_CREDENTIALS = {
  email: 'agent@parceltrack.cm',
  staffId: 'PT-2048',
  password: 'Douala2026!',
};

const AuthContext = createContext(null);

function readSession() {
  try {
    const storedSession = localStorage.getItem(STORAGE_KEY);
    return storedSession ? JSON.parse(storedSession) : null;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readSession);

  function login(identifier, password) {
    const normalizedIdentifier = identifier.trim().toLowerCase();
    const validIdentifier = [DEMO_CREDENTIALS.email, DEMO_CREDENTIALS.staffId.toLowerCase()]
      .includes(normalizedIdentifier);

    if (!validIdentifier || password !== DEMO_CREDENTIALS.password) {
      return { success: false, error: 'That email or staff ID and password do not match.' };
    }

    const session = {
      name: 'Agency Operator',
      email: DEMO_CREDENTIALS.email,
      staffId: DEMO_CREDENTIALS.staffId,
      terminal: 'Douala Terminal',
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    setUser(session);
    return { success: true };
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
  }

  const value = useMemo(() => ({ user, login, logout, isAuthenticated: Boolean(user) }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}