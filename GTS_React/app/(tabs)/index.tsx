import React, { useState, useEffect } from 'react';
import { View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import HomeScreen from '@/screens/Home';
import ViewRequestScreen from '@/screens/ViewRequest';
import CreateRequestScreen from '@/screens/CreateRequest';
import Tabs from '@/screens/tabs';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState('home');

  useEffect(() => {
    const fetchSavedView = async () => {
      try {
        const savedView = await AsyncStorage.getItem('currentView');
        if (savedView) {
          setCurrentView(savedView);
        }
      } catch (error) {
        console.error('Failed to load saved view:', error);
      }
    };
    fetchSavedView();
  }, []);

  useEffect(() => {
    const saveCurrentView = async () => {
      try {
        await AsyncStorage.setItem('currentView', currentView);
      } catch (error) {
        console.error('Failed to save current view:', error);
      }
    };
    saveCurrentView();
  }, [currentView]);

  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return <HomeScreen />;
      case 'view-tickets':
        return <ViewRequestScreen />;
      case 'create-ticket':
        return <CreateRequestScreen />;
      default:
        return <HomeScreen />;
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <Tabs setCurrentView={setCurrentView} />
      {renderCurrentView()}
    </View>
  );
};

export default App;
