import React, { useState } from 'react';
import { Rect, Text, Group } from "react-konva";
import config from '../../../config.json';

export default function TrackTile({ track, onClick, onPlayClick }) {
  const size = config.tileSize;
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Group
      x={track.x}
      y={track.y}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Rect
        width={size}
        height={size}
        fill={track.colour || "lightblue"}
        stroke="black"
        strokeWidth={2}
        cornerRadius={1}
      />
      <Text
        text={`${track.artist}\n${track.title}\nGenre: ${track.genre}`}
        fontSize={10}
        padding={8}
        width={size}
        height={size}
        fill="black"
        wrap="word"
      />

      {/* Show play button on hover */}
      {isHovered && track.preview_url && (
        <Text
          text="▶"
          fontSize={14}
          fill="white"
          x={4}
          y={size - 18}
          onClick={(e) => {
            e.cancelBubble = true; // prevent bubbling to tile onClick
            onPlayClick(track.preview_url, track.id);
          }}
        />
      )}
    </Group>
  );
}
