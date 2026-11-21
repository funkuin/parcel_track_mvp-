import React from 'react';
import { ArrowLeft, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function PublicTrackingPlaceholder() {
  return (
    <main className="public-placeholder">
      <header className="public-placeholder__nav"><Link className="brand-lockup" to="/login"><span className="brand-mark"><MapPin size={20} /></span><span>parcel<span className="brand-accent">track</span></span></Link><Link className="staff-link" to="/login">Agency staff <ArrowLeft size={14} /></Link></header>
      <section className="public-placeholder__body"><span className="simple-placeholder__icon"><MapPin size={24} /></span><div className="page-eyebrow">PARCEL TRACKING</div><h1>Your parcel's journey,<br />all in one place.</h1><p>The public tracking experience will be connected here.</p><span className="coming-label"><i /> MODULE SLOT READY</span></section>
      {/* TODO: Teammate integration - add public parcel lookup and tracking status here. */}
    </main>
  );
}