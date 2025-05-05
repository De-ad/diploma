import React from "react";

type Props = {
  progress: number;
  radius?: number;
  stroke?: number;
  colored?: boolean;
};

export const Circle: React.FC<Props> = ({
  progress,
  radius = 50,
  stroke = 8,
  colored = false,
}) => {
  const normalizedRadius = radius - stroke / 2;
  const circumference = 2 * Math.PI * normalizedRadius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  const getColor = () => {
    if (!colored) return "var(--main-color-light)";
    if (progress < 50) return "var(--red)";
    if (progress < 90) return "var(--yellow)";
    return "var(--green)";
  };

  return (
    <svg width={radius * 2} height={radius * 2}>
      {/* Background Circle */}
      <circle
        stroke="#e5e7eb"
        fill="transparent"
        strokeWidth={stroke}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      {/* Progress Circle */}
      <circle
        stroke={getColor()}
        fill="transparent"
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
        transform={`rotate(-90 ${radius} ${radius})`}
      />
      {/* Center Text */}
      <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle">
        {`${Math.round(progress)}%`}
      </text>
    </svg>
  );
};
