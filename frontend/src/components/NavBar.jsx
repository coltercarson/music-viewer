import React from "react";
import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "1rem 2rem",
      backgroundColor: "#222",
      color: "white"
    }}>
      <div style={{ fontWeight: "bold", fontSize: "1.2rem" }}>
        Colter's Music Portal
      </div>
      <div style={{ display: "flex", gap: "1rem" }}>
        <Link style={{ color: "white", textDecoration: "none" }} to="/">Canvas View</Link>
        <Link style={{ color: "white", textDecoration: "none" }} to="/list">List View</Link>
        <Link style={{ color: "white", textDecoration: "none" }} to="/3d">3D View</Link>
        <Link style={{ color: "white", textDecoration: "none" }} to="/about">About</Link>
      </div>
    </nav>
  );
}
