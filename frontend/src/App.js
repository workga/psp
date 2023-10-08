import React from 'react';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import { Search } from './components/Search/Search.js'
import { Info } from './components/Info/Info.js'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Search />} />
      <Route path="/info" element={<Info />} />
    </Routes>
  )
}
