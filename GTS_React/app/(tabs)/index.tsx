import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { View } from 'react-native';
import HomeScreen from '@/screens/Home';
import ViewRequestScreen from '@/screens/ViewRequest';
import CreateRequestScreen from '@/screens/CreateRequest';

const App: React.FC = () => {
  return (
    <Router>
      <View style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/view-tickets" element={<ViewRequestScreen />} />
          <Route path="/create-ticket" element={<CreateRequestScreen />} />
        </Routes>
      </View>
    </Router>
  );
};

export default App;
