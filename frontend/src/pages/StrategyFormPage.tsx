import React from 'react';
import { useParams } from 'react-router-dom';

interface StrategyFormPageProps {
  exposureStep?: boolean;
  creditsStep?: boolean;
  buyCreditsStep?: boolean;
}

const StrategyFormPage: React.FC<StrategyFormPageProps> = ({ 
  exposureStep = false, 
  creditsStep = false,
  buyCreditsStep = false
}) => {
  const { id } = useParams<{ id: string }>();
  
  let content;
  if (exposureStep) {
    content = <h2>Exposure Level Configuration</h2>;
  } else if (creditsStep) {
    content = <h2>Send Credits Form</h2>;
  } else if (buyCreditsStep) {
    content = <h2>Buy Credits Form</h2>;
  } else {
    content = <h2>Strategy Configuration for ID: {id}</h2>;
  }

  return (
    <div>
      <h1>Strategy Form Page</h1>
      {content}
      <p>This is a placeholder component for the Strategy Form Page</p>
    </div>
  );
};

export default StrategyFormPage;