import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import About from "./About";
import MapView from "./views/MapView";
import ThreeDView from "./views/ThreeDView";

export default function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<MapView />} />
        <Route path="/list" element={<div style={{ padding: "2rem" }}>List view coming soon.</div>} />
        <Route path="/3d" element={<ThreeDView />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}
