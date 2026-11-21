import React from 'react';
import { ArrowUpRight, PackageCheck, PackagePlus, Route } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DashboardPlaceholder() {
  return (
    <section className="placeholder-page">
      <div className="page-heading-row">
        <div><div className="page-eyebrow">AGENCY OVERVIEW <span className="eyebrow-dot" /></div><h1>Good morning, operator</h1><p>Your route desk is ready for today's work.</p></div>
        <div className="date-stamp">DOUALA TERMINAL <span>CAMEROON</span></div>
      </div>
      <div className="dashboard-welcome">
        <div className="welcome-copy"><span className="welcome-kicker">PARCEL OPERATIONS <span>01</span></span><h2>Keep every<br />handoff moving.</h2><p>Register a parcel or check its progress across the Douala to Bamenda route.</p><Link className="welcome-action" to="/register">Register a parcel <ArrowUpRight size={16} /></Link></div>
        <div className="welcome-art" aria-hidden="true"><div className="art-ring art-ring--outer" /><div className="art-ring art-ring--inner" /><div className="art-route-dot art-route-dot--one" /><div className="art-route-dot art-route-dot--two" /><div className="art-route-path" /><div className="art-box"><PackageCheck size={41} strokeWidth={1.25} /></div><span className="art-label art-label--one">DLA</span><span className="art-label art-label--two">BDA</span></div>
      </div>
      <div className="placeholder-section-title"><h3>Quick access</h3><span>YOUR WORKSPACE</span></div>
      <div className="quick-links"><Link className="quick-link" to="/register"><span className="quick-link__icon quick-link__icon--green"><PackagePlus size={19} /></span><span><strong>Register parcel</strong><small>Start a new shipment entry</small></span><ArrowUpRight size={16} /></Link><Link className="quick-link" to="/tracking"><span className="quick-link__icon quick-link__icon--coral"><Route size={19} /></span><span><strong>Track a parcel</strong><small>Open public tracking lookup</small></span><ArrowUpRight size={16} /></Link></div>
      {/* TODO: Teammate integration - replace this overview placeholder with dashboard metrics and agency activity. */}
    </section>
  );
}