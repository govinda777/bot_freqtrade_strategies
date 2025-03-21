import React from 'react';

interface TermsAndConditionsPageProps {
  userType: 'client' | 'developer';
}

const TermsAndConditionsPage: React.FC<TermsAndConditionsPageProps> = ({ userType }) => {
  return (
    <div>
      <h1>Terms and Conditions</h1>
      <h2>{userType === 'developer' ? 'Developer' : 'Client'} Agreement</h2>
      <p>This is a placeholder component for the Terms and Conditions Page</p>
      
      <div>
        <h3>Agreement Terms</h3>
        <p>These would be the specific terms for the {userType}.</p>
      </div>
    </div>
  );
};

export default TermsAndConditionsPage;