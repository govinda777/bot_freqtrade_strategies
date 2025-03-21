import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';

// Mock strategy data - in a real app, this would come from an API
const mockStrategies = [
  {
    id: 1,
    name: 'CombinedBinHAndCluc',
    description: 'Combines BinHV45 and ClucMay72018 strategies for a balanced approach',
    developer: 'FreqTrade Team',
    performance: {
      monthlyROI: 4.5,
      winRate: 62,
      avgProfitPerTrade: 2.1,
      totalTrades: 189
    },
    riskLevel: 'moderate',
    popularity: 87,
    minCredits: 50
  },
  {
    id: 2,
    name: 'NostalgiaForInfinityX',
    description: 'Advanced multi-indicator strategy with sophisticated risk management',
    developer: 'Iterativ',
    performance: {
      monthlyROI: 5.8,
      winRate: 58,
      avgProfitPerTrade: 2.8,
      totalTrades: 152
    },
    riskLevel: 'aggressive',
    popularity: 92,
    minCredits: 100
  },
  {
    id: 3,
    name: 'E0V1E Strategy',
    description: 'Simple yet effective strategy based on moving averages and RSI',
    developer: 'SSSSI',
    performance: {
      monthlyROI: 3.2,
      winRate: 65,
      avgProfitPerTrade: 1.7,
      totalTrades: 212
    },
    riskLevel: 'conservative',
    popularity: 76,
    minCredits: 30
  },
  {
    id: 4,
    name: 'DWT Strategy',
    description: 'Applies Discrete Wavelet Transform to identify patterns in price movements',
    developer: 'NateEmma',
    performance: {
      monthlyROI: 6.2,
      winRate: 54,
      avgProfitPerTrade: 3.5,
      totalTrades: 128
    },
    riskLevel: 'aggressive',
    popularity: 81,
    minCredits: 120
  },
  {
    id: 5,
    name: 'LSTM-Based Strategy',
    description: 'Uses deep learning LSTM networks to predict price movements',
    developer: 'Netanelshoshan',
    performance: {
      monthlyROI: 7.1,
      winRate: 51,
      avgProfitPerTrade: 4.3,
      totalTrades: 105
    },
    riskLevel: 'aggressive',
    popularity: 88,
    minCredits: 150
  }
];

// Filter options
interface FilterOptions {
  riskLevel: string[];
  minROI: number | null;
  minWinRate: number | null;
  sortBy: 'popularity' | 'performance' | 'credits';
}

const StrategySelectionPage: React.FC = () => {
  const navigate = useNavigate();
  const { userCredits } = useAuth();
  const [strategies, setStrategies] = useState(mockStrategies);
  const [filteredStrategies, setFilteredStrategies] = useState(mockStrategies);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    riskLevel: [],
    minROI: null,
    minWinRate: null,
    sortBy: 'popularity'
  });

  // Filter and sort strategies based on options
  useEffect(() => {
    let result = [...strategies];
    
    // Apply search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(
        strategy => 
          strategy.name.toLowerCase().includes(term) || 
          strategy.description.toLowerCase().includes(term) ||
          strategy.developer.toLowerCase().includes(term)
      );
    }
    
    // Apply risk level filter
    if (filterOptions.riskLevel.length > 0) {
      result = result.filter(strategy => 
        filterOptions.riskLevel.includes(strategy.riskLevel)
      );
    }
    
    // Apply ROI filter
    if (filterOptions.minROI !== null) {
      result = result.filter(strategy => 
        strategy.performance.monthlyROI >= (filterOptions.minROI || 0)
      );
    }
    
    // Apply win rate filter
    if (filterOptions.minWinRate !== null) {
      result = result.filter(strategy => 
        strategy.performance.winRate >= (filterOptions.minWinRate || 0)
      );
    }
    
    // Apply sorting
    switch (filterOptions.sortBy) {
      case 'popularity':
        result.sort((a, b) => b.popularity - a.popularity);
        break;
      case 'performance':
        result.sort((a, b) => b.performance.monthlyROI - a.performance.monthlyROI);
        break;
      case 'credits':
        result.sort((a, b) => a.minCredits - b.minCredits);
        break;
    }
    
    setFilteredStrategies(result);
  }, [strategies, searchTerm, filterOptions]);

  // Handle filter updates
  const handleRiskLevelChange = (level: string) => {
    setFilterOptions(prev => {
      const riskLevel = prev.riskLevel.includes(level)
        ? prev.riskLevel.filter(l => l !== level)
        : [...prev.riskLevel, level];
      
      return { ...prev, riskLevel };
    });
  };

  const handleROIChange = (value: number | null) => {
    setFilterOptions(prev => ({ ...prev, minROI: value }));
  };

  const handleWinRateChange = (value: number | null) => {
    setFilterOptions(prev => ({ ...prev, minWinRate: value }));
  };

  const handleSortChange = (value: 'popularity' | 'performance' | 'credits') => {
    setFilterOptions(prev => ({ ...prev, sortBy: value }));
  };

  // Handle strategy selection
  const handleSelectStrategy = (strategyId: number) => {
    navigate(`/strategy-form/${strategyId}`);
  };

  return (
    <PageContainer>
      <Header>
        <h1>Select a Trading Strategy</h1>
        <p>Browse available strategies and select one that matches your investment goals and risk tolerance.</p>
      </Header>

      <ContentWrapper>
        <Sidebar>
          <FilterSection>
            <h3>Filters</h3>

            <FilterGroup>
              <FilterLabel>Risk Level</FilterLabel>
              <CheckboxGroup>
                <CheckboxItem>
                  <input 
                    type="checkbox" 
                    id="conservative"
                    checked={filterOptions.riskLevel.includes('conservative')}
                    onChange={() => handleRiskLevelChange('conservative')}
                  />
                  <label htmlFor="conservative">Conservative</label>
                </CheckboxItem>
                <CheckboxItem>
                  <input 
                    type="checkbox" 
                    id="moderate"
                    checked={filterOptions.riskLevel.includes('moderate')}
                    onChange={() => handleRiskLevelChange('moderate')}
                  />
                  <label htmlFor="moderate">Moderate</label>
                </CheckboxItem>
                <CheckboxItem>
                  <input 
                    type="checkbox" 
                    id="aggressive"
                    checked={filterOptions.riskLevel.includes('aggressive')}
                    onChange={() => handleRiskLevelChange('aggressive')}
                  />
                  <label htmlFor="aggressive">Aggressive</label>
                </CheckboxItem>
              </CheckboxGroup>
            </FilterGroup>

            <FilterGroup>
              <FilterLabel>Minimum ROI (%/month)</FilterLabel>
              <RangeSlider
                type="range"
                min="0"
                max="10"
                step="0.5"
                value={filterOptions.minROI || 0}
                onChange={(e) => handleROIChange(parseFloat(e.target.value))}
              />
              <SliderValue>{filterOptions.minROI || 0}%</SliderValue>
            </FilterGroup>

            <FilterGroup>
              <FilterLabel>Minimum Win Rate (%)</FilterLabel>
              <RangeSlider
                type="range"
                min="0"
                max="100"
                step="5"
                value={filterOptions.minWinRate || 0}
                onChange={(e) => handleWinRateChange(parseFloat(e.target.value))}
              />
              <SliderValue>{filterOptions.minWinRate || 0}%</SliderValue>
            </FilterGroup>

            <FilterGroup>
              <FilterLabel>Sort By</FilterLabel>
              <Select 
                value={filterOptions.sortBy}
                onChange={(e) => handleSortChange(e.target.value as any)}
              >
                <option value="popularity">Popularity</option>
                <option value="performance">Performance</option>
                <option value="credits">Required Credits (Low to High)</option>
              </Select>
            </FilterGroup>

            <ResetButton onClick={() => setFilterOptions({
              riskLevel: [],
              minROI: null,
              minWinRate: null,
              sortBy: 'popularity'
            })}>
              Reset Filters
            </ResetButton>
          </FilterSection>
        </Sidebar>

        <MainContent>
          <SearchBar>
            <SearchIcon>🔍</SearchIcon>
            <SearchInput 
              type="text" 
              placeholder="Search strategies by name, description or developer..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </SearchBar>

          <ResultStats>
            Found {filteredStrategies.length} strategies{' '}
            {searchTerm && <span>matching "{searchTerm}"</span>}
          </ResultStats>

          <StrategiesList>
            {filteredStrategies.length > 0 ? (
              filteredStrategies.map(strategy => (
                <StrategyCard key={strategy.id}>
                  <div>
                    <StrategyName>{strategy.name}</StrategyName>
                    <StrategyDeveloper>by {strategy.developer}</StrategyDeveloper>
                    <StrategyDescription>{strategy.description}</StrategyDescription>
                    
                    <PerformanceGrid>
                      <PerformanceItem>
                        <PerformanceValue>{strategy.performance.monthlyROI}%</PerformanceValue>
                        <PerformanceLabel>Monthly ROI</PerformanceLabel>
                      </PerformanceItem>
                      <PerformanceItem>
                        <PerformanceValue>{strategy.performance.winRate}%</PerformanceValue>
                        <PerformanceLabel>Win Rate</PerformanceLabel>
                      </PerformanceItem>
                      <PerformanceItem>
                        <PerformanceValue>${strategy.performance.avgProfitPerTrade}</PerformanceValue>
                        <PerformanceLabel>Avg. Profit</PerformanceLabel>
                      </PerformanceItem>
                      <PerformanceItem>
                        <PerformanceValue>{strategy.performance.totalTrades}</PerformanceValue>
                        <PerformanceLabel>Total Trades</PerformanceLabel>
                      </PerformanceItem>
                    </PerformanceGrid>
                  </div>

                  <StrategyFooter>
                    <RiskLevel level={strategy.riskLevel}>
                      {strategy.riskLevel.charAt(0).toUpperCase() + strategy.riskLevel.slice(1)}
                    </RiskLevel>
                    <CreditsRequired>
                      {strategy.minCredits <= userCredits ? (
                        <>
                          <CreditsBadge>{strategy.minCredits} Credits</CreditsBadge>
                          <SelectButton onClick={() => handleSelectStrategy(strategy.id)}>
                            Select Strategy
                          </SelectButton>
                        </>
                      ) : (
                        <>
                          <CreditsBadge insufficient>{strategy.minCredits} Credits Required</CreditsBadge>
                          <InsufficientCreditsButton onClick={() => navigate('/buy-credits')}>
                            Buy Credits
                          </InsufficientCreditsButton>
                        </>
                      )}
                    </CreditsRequired>
                  </StrategyFooter>
                </StrategyCard>
              ))
            ) : (
              <NoResultsMessage>
                No strategies found matching your criteria. Try adjusting your filters.
              </NoResultsMessage>
            )}
          </StrategiesList>
        </MainContent>
      </ContentWrapper>
    </PageContainer>
  );
};

// Styled Components
const PageContainer = styled.div`
  width: 100%;
`;

const Header = styled.div`
  margin-bottom: 2rem;
  
  h1 {
    margin: 0 0 0.5rem;
    color: ${props => props.theme.colors.text.primary};
  }
  
  p {
    color: ${props => props.theme.colors.text.secondary};
    font-size: 1.1rem;
    margin: 0;
  }
`;

const ContentWrapper = styled.div`
  display: flex;
  gap: 2rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const Sidebar = styled.div`
  width: 300px;
  flex-shrink: 0;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const MainContent = styled.div`
  flex: 1;
`;

const FilterSection = styled.div`
  background-color: ${props => props.theme.colors.background.paper};
  padding: 1.5rem;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  
  h3 {
    margin: 0 0 1.5rem;
    color: ${props => props.theme.colors.text.primary};
    font-size: 1.25rem;
  }
`;

const FilterGroup = styled.div`
  margin-bottom: 1.5rem;
`;

const FilterLabel = styled.div`
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text.primary};
`;

const CheckboxGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const CheckboxItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  input {
    margin: 0;
  }
  
  label {
    font-size: 0.9rem;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const RangeSlider = styled.input`
  width: 100%;
  margin: 0.5rem 0;
`;

const SliderValue = styled.div`
  font-size: 0.9rem;
  color: ${props => props.theme.colors.text.secondary};
  text-align: right;
`;

const Select = styled.select`
  width: 100%;
  padding: 0.5rem;
  border-radius: ${props => props.theme.borderRadius.small};
  border: 1px solid ${props => props.theme.colors.divider};
  background-color: white;
  font-size: 0.9rem;
  color: ${props => props.theme.colors.text.primary};
`;

const ResetButton = styled.button`
  background-color: transparent;
  border: 1px solid ${props => props.theme.colors.divider};
  color: ${props => props.theme.colors.text.secondary};
  padding: 0.5rem 1rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.9rem;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
`;

const SearchBar = styled.div`
  display: flex;
  align-items: center;
  background-color: ${props => props.theme.colors.background.paper};
  border-radius: ${props => props.theme.borderRadius.small};
  padding: 0 1rem;
  box-shadow: ${props => props.theme.shadows[1]};
  margin-bottom: 1.5rem;
`;

const SearchIcon = styled.div`
  font-size: 1rem;
  color: ${props => props.theme.colors.text.secondary};
  margin-right: 0.5rem;
`;

const SearchInput = styled.input`
  flex: 1;
  border: none;
  padding: 1rem 0;
  font-size: 1rem;
  background-color: transparent;
  color: ${props => props.theme.colors.text.primary};
  
  &:focus {
    outline: none;
  }
  
  &::placeholder {
    color: ${props => props.theme.colors.text.hint};
  }
`;

const ResultStats = styled.div`
  font-size: 0.9rem;
  color: ${props => props.theme.colors.text.secondary};
  margin-bottom: 1rem;
  
  span {
    font-style: italic;
  }
`;

const StrategiesList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const StrategyCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: ${props => props.theme.colors.background.paper};
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  padding: 1.5rem;
  transition: box-shadow 0.3s;
  
  &:hover {
    box-shadow: ${props => props.theme.shadows[2]};
  }
`;

const StrategyName = styled.h3`
  margin: 0 0 0.25rem;
  color: ${props => props.theme.colors.text.primary};
  font-size: 1.25rem;
`;

const StrategyDeveloper = styled.div`
  font-size: 0.9rem;
  color: ${props => props.theme.colors.text.secondary};
  margin-bottom: 1rem;
`;

const StrategyDescription = styled.p`
  margin: 0 0 1.5rem;
  color: ${props => props.theme.colors.text.secondary};
  line-height: 1.5;
`;

const PerformanceGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
  
  @media (max-width: 576px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const PerformanceItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const PerformanceValue = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 0.25rem;
`;

const PerformanceLabel = styled.div`
  font-size: 0.8rem;
  color: ${props => props.theme.colors.text.secondary};
`;

interface RiskLevelProps {
  level: string;
}

const RiskLevel = styled.div<RiskLevelProps>`
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.85rem;
  font-weight: 500;
  background-color: ${props => {
    switch (props.level) {
      case 'conservative':
        return props.theme.colors.riskLevels.conservative + '20';
      case 'moderate':
        return props.theme.colors.riskLevels.moderate + '20';
      case 'aggressive':
        return props.theme.colors.riskLevels.aggressive + '20';
      default:
        return props.theme.colors.primary + '20';
    }
  }};
  color: ${props => {
    switch (props.level) {
      case 'conservative':
        return props.theme.colors.riskLevels.conservative;
      case 'moderate':
        return props.theme.colors.riskLevels.moderate;
      case 'aggressive':
        return props.theme.colors.riskLevels.aggressive;
      default:
        return props.theme.colors.primary;
    }
  }};
`;

const StrategyFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
`;

const CreditsRequired = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

interface CreditsBadgeProps {
  insufficient?: boolean;
}

const CreditsBadge = styled.div<CreditsBadgeProps>`
  padding: 0.35rem 0.75rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.85rem;
  background-color: ${props => 
    props.insufficient 
      ? props.theme.colors.error + '20' 
      : props.theme.colors.primary + '20'
  };
  color: ${props => 
    props.insufficient 
      ? props.theme.colors.error 
      : props.theme.colors.primary
  };
`;

const SelectButton = styled.button`
  background-color: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #303f9f;
  }
`;

const InsufficientCreditsButton = styled.button`
  background-color: ${props => props.theme.colors.error};
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #d32f2f;
  }
`;

const NoResultsMessage = styled.div`
  text-align: center;
  padding: 3rem 0;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 1.1rem;
`;

export default StrategySelectionPage;