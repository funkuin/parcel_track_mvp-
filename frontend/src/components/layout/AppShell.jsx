import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { ArrowUpRight, Box, LayoutDashboard, LogOut, MapPin, Menu, PackagePlus, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext.jsx';
import Button from '../ui/Button.jsx';

const navigation = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Register parcel', to: '/register', icon: PackagePlus },
  { label: 'Track parcel', to: '/tracking', icon: MapPin, publicRoute: true },
];

export default function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    logout();
    navigate('/login', { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${menuOpen ? 'sidebar--open' : ''}`}>
        <div className="brand-lockup">
          <div className="brand-mark"><Box size={21} strokeWidth={2.2} /></div>
          <span>parcel<span className="brand-accent">track</span></span>
          <button className="icon-button mobile-close" type="button" aria-label="Close navigation" onClick={() => setMenuOpen(false)}>
            <X size={19} />
          </button>
        </div>

        <div className="sidebar-label">WORKSPACE</div>
        <nav className="primary-nav" aria-label="Main navigation">
          {navigation.map(({ label, to, icon: Icon, publicRoute }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-link ${isActive && !publicRoute ? 'nav-link--active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              <Icon size={18} strokeWidth={1.8} />
              <span>{label}</span>
              {label === 'Track parcel' && <ArrowUpRight className="nav-external" size={14} />}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="terminal-card">
            <div className="terminal-card__icon"><MapPin size={16} /></div>
            <div>
              <span className="terminal-label">ACTIVE TERMINAL</span>
              <strong>Douala <span>↔</span> Bamenda</strong>
            </div>
            <span className="online-dot" aria-label="Online" />
          </div>
          <div className="sidebar-user">
            <div className="user-avatar">AO</div>
            <div className="sidebar-user__identity">
              <strong>{user?.name ?? 'Agency Operator'}</strong>
              <span>{user?.staffId ?? 'PT-2048'}</span>
            </div>
            <Button className="logout-button" variant="quiet" onClick={handleLogout} aria-label="Log out" title="Log out">
              <LogOut size={17} />
            </Button>
          </div>
        </div>
      </aside>

      {menuOpen && <button className="sidebar-scrim" type="button" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}

      <main className="main-panel">
        <header className="topbar">
          <button className="icon-button mobile-menu" type="button" aria-label="Open navigation" onClick={() => setMenuOpen(true)}>
            <Menu size={20} />
          </button>
          <div className="breadcrumb"><span>Agency workspace</span><span className="breadcrumb-divider">/</span><strong>Operations</strong></div>
          <div className="topbar-right">
            <span className="service-status"><span className="online-dot" /> All systems operational</span>
            <span className="topbar-date">Douala, Cameroon</span>
          </div>
        </header>
        <div className="page-content"><Outlet /></div>
      </main>
    </div>
  );
}