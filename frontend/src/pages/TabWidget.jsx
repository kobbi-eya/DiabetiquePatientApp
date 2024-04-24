// Définition du composant TabWidget
import React, { useState } from 'react'; 

const TabWidget = ({ children }) => {
    const [activeTab, setActiveTab] = useState(1);
  
    const handleTabClick = (index) => {
      setActiveTab(index);
    };
  
    return (
      <div className="tab-widget">
        <div className="tab-buttons">
          {React.Children.map(children, (child, index) => (
            <button
              key={index}
              onClick={() => handleTabClick(index + 1)}
              className={activeTab === index + 1 ? 'tab active' : 'tab'}
            >
              {child.props.label}
            </button>
          ))}
        </div>
        <div className="tab-content">
          {React.Children.toArray(children).filter(
            (child, index) => activeTab === index + 1
          )}
        </div>
      </div>
    );
  };
  
  // Assurez-vous d'exporter le composant TabWidget pour pouvoir l'utiliser dans d'autres fichiers
  export default TabWidget;
  