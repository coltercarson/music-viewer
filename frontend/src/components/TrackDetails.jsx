import React from "react";

export default function TrackDetails({ track, onClose }) {
  return (
    <div
      style={{
        position: "absolute",
        top: 40,
        right: 40,
        background: "white",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "10px",
        maxWidth: "300px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
        zIndex: 1000,
      }}
    >
      <button
        onClick={onClose}
        style={{
          float: "right",
          border: "none",
          background: "transparent",
          fontSize: "1.5rem",
          cursor: "pointer",
        }}
      >
        ×
      </button>
      <h3>{track.title}</h3>
      <p><strong>Artist:</strong> {track.artist}</p>
      <p><strong>Album:</strong> {track.album}</p>
      <p><strong>Genre(s):</strong> {track.genre}</p>
      <p><strong>Date:</strong> {track.date}</p>
      <p><strong>Track #:</strong> {track.tracknumber}</p>
      <p>
        <strong>Preview link:</strong>{" "}
        {track.preview_url ? (
          <a href={track.preview_url} target="_blank" rel="noopener noreferrer">
            {track.preview_url}
          </a>
        ) : (
          "N/A"
        )}
      </p>
      <p>
        <strong>Buy link:</strong>{" "}
        {track.buy_url ? (
          <a href={track.buy_url} target="_blank" rel="noopener noreferrer">
            {track.buy_url}
          </a>
        ) : (
          "N/A"
        )}
      </p>
    </div>
  );
}
