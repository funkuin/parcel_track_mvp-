import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import AppShell from './components/layout/AppShell.jsx';
import ProtectedRoute from './components/layout/ProtectedRoute.jsx';
import Login from './pages/Login.jsx';
import DashboardPlaceholder from './pages/DashboardPlaceholder.jsx';
import RegisterParcelPlaceholder from './pages/RegisterParcelPlaceholder.jsx';
import PublicTrackingPlaceholder from './pages/PublicTrackingPlaceholder.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/tracking" element={<PublicTrackingPlaceholder />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPlaceholder />} />
          <Route path="register" element={<RegisterParcelPlaceholder />} />
          <Route path="agency/*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}