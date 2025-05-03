import React from "react";

type HalfCircleProps = {
  progress: number;
  radius?: number;
  stroke?: number;
};

export const HalfCircle: React.FC<HalfCircleProps> = ({
  progress,
  radius = 50,
  stroke = 8,
}) => {
  const normalizedRadius = radius - stroke / 2;
  const circumference = Math.PI * normalizedRadius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  const centerX = radius;
  const centerY = radius;

  const d = `
    M ${centerX - normalizedRadius} ${centerY}
    A ${normalizedRadius} ${normalizedRadius} 0 0 1 ${centerX + normalizedRadius} ${centerY}
  `;

  return (
    <svg width={radius * 2} height={radius}>
      <path d={d} stroke="#e5e7eb" fill="transparent" strokeWidth={stroke} />
      <path
        d={d}
        stroke="#3b82f6"
        fill="transparent"
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
      />
      <text
        x="50%"
        y="90%"
        dominantBaseline="middle"
        textAnchor="middle"
        fontSize="12"
        fill="#000"
      >
        {`${Math.round(progress)}%`}
      </text>
    </svg>
  );
};
