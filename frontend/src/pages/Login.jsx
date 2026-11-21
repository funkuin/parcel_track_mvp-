import React, { useState } from 'react';
import { ArrowRight, Box, Check, Eye, EyeOff, MapPin, ShieldCheck, Truck } from 'lucide-react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { DEMO_CREDENTIALS, useAuth } from '../context/AuthContext.jsx';
import Button from '../components/ui/Button.jsx';
import TextField from '../components/ui/TextField.jsx';

export default function Login() {
  const { login, isAuthenticated } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  function fillDemo() {
    setIdentifier(DEMO_CREDENTIALS.email);
    setPassword(DEMO_CREDENTIALS.password);
    setErrors({});
    setFormError('');
  }

  function handleSubmit(event) {
    event.preventDefault();
    const nextErrors = {};
    if (!identifier.trim()) nextErrors.identifier = 'Enter your email or staff ID.';
    if (!password) nextErrors.password = 'Enter your password.';
    setErrors(nextErrors);
    setFormError('');
    if (Object.keys(nextErrors).length) return;

    const result = login(identifier, password);
    if (!result.success) {
      setFormError(result.error);
      return;
    }
    navigate(location.state?.from?.pathname ?? '/dashboard', { replace: true });
  }

  return (
    <main className="login-page">
      <section className="login-story" aria-label="ParcelTrack route">
        <div className="login-story__top">
          <a className="brand-lockup brand-lockup--light" href="/login" aria-label="ParcelTrack home">
            <span className="brand-mark"><Box size={21} strokeWidth={2.2} /></span>
            <span>parcel<span className="brand-accent">track</span></span>
          </a>
          <span className="story-tag"><span className="online-dot" /> AGENCY NETWORK</span>
        </div>

        <div className="story-content">
          <div className="story-kicker"><span /> CAMEROON, CONNECTED</div>
          <h1>Every parcel.<br /><span>On its way.</span></h1>
          <p>One clear view of the road between your terminal and every destination.</p>

          <div className="route-visual" aria-label="Route from Douala to Bamenda">
            <div className="route-line"><span className="route-line__progress" /><span className="route-pin route-pin--start"><MapPin size={17} /></span><span className="route-pin route-pin--end"><MapPin size={17} /></span><span className="route-van"><Truck size={18} /></span></div>
            <div className="route-cities"><span><strong>Douala</strong><small>Coastal terminal</small></span><span className="route-distance">367 KM</span><span className="route-city--end"><strong>Bamenda</strong><small>Northwest region</small></span></div>
          </div>
        </div>

        <div className="story-footer"><span><ShieldCheck size={16} /> Secure agency access</span><span>BUILT FOR THE JOURNEY <ArrowRight size={14} /></span></div>
        <div className="story-orbit story-orbit--one" /><div className="story-orbit story-orbit--two" />
      </section>

      <section className="login-form-panel">
        <div className="login-form-wrap">
          <div className="form-heading">
            <div className="form-eyebrow"><span className="form-eyebrow__bar" /> STAFF PORTAL</div>
            <h2>Welcome back</h2>
            <p>Sign in to your agency workspace.</p>
          </div>

          <form className="login-form" onSubmit={handleSubmit} noValidate>
            <TextField
              label="Email or staff ID"
              name="identifier"
              autoComplete="username"
              placeholder="you@agency.cm or PT-2048"
              value={identifier}
              onChange={(event) => { setIdentifier(event.target.value); setErrors((previous) => ({ ...previous, identifier: '' })); setFormError(''); }}
              error={errors.identifier}
            />
            <div className="password-field">
              <TextField
                label="Password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                placeholder="Enter your password"
                value={password}
                onChange={(event) => { setPassword(event.target.value); setErrors((previous) => ({ ...previous, password: '' })); setFormError(''); }}
                error={errors.password}
              />
              <button className="password-toggle" type="button" onClick={() => setShowPassword((visible) => !visible)} aria-label={showPassword ? 'Hide password' : 'Show password'}>
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>

            {formError && <div className="form-alert" role="alert">{formError}</div>}

            <Button className="login-submit" type="submit">Sign in <ArrowRight size={17} /></Button>
          </form>

          <div className="form-divider"><span /> OR <span /></div>
          <Button className="demo-login" variant="secondary" type="button" onClick={fillDemo}><Check size={16} /> Fill demo credentials</Button>

          <div className="demo-note"><span className="demo-note__dot" /><span>Demo access is ready for this workspace.</span></div>
          <div className="login-legal">By signing in, you agree to your agency's operational access policy.</div>
        </div>
        <div className="mobile-brand"><Box size={17} /> ParcelTrack <span>AGENCY PORTAL</span></div>
      </section>
    </main>
  );
}