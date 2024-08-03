import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import CreateRequestScreen from '@/screens/CreateRequest';
import HomeScreen from '@/screens/Home';
import ViewRequestScreen from '@/screens/ViewRequest';

const Tab = createBottomTabNavigator();

const Tabs: React.FC = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="CreateRequest" component={CreateRequestScreen} />
      <Tab.Screen name="PreviousRequests" component={ViewRequestScreen} />
    </Tab.Navigator>
  );
};

export default Tabs;
