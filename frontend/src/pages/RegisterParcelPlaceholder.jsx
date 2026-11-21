import React from 'react';
import { ArrowLeft, PackagePlus } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function RegisterParcelPlaceholder() {
  return (
    <section className="placeholder-page simple-placeholder">
      <Link className="back-link" to="/dashboard"><ArrowLeft size={15} /> Dashboard</Link>
      <div className="simple-placeholder__content"><span className="simple-placeholder__icon"><PackagePlus size={24} /></span><div className="page-eyebrow">AGENCY WORKSPACE</div><h1>Register a parcel</h1><p>The parcel intake workspace will be connected here.</p><span className="coming-label"><i /> MODULE SLOT READY</span></div>
      {/* TODO: Teammate integration - mount the parcel registration flow on this page. */}
    </section>
  );
}