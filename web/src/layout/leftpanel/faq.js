import React from 'react';

// Modules
import { __ } from '../../helpers/translation';

export default () => (
  <div className="faq-panel">
    <div className="faq-header">
      <span className="left-panel-back-button">
        <i className="material-icons" aria-hidden="true">arrow_back</i>
      </span>
      <span className="title">{__('misc.faq')}</span>
    </div>
    <div className="faq" />
  </div>
);
