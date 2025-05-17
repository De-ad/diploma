import React from "react";
import { MdInfoOutline } from "react-icons/md";
import styles from "./styles.module.css";

type Props = {
  name: string;
  fullName: string;
  description: string;
  value: number;
  good: number;
  poor: number;
  unit?: string;
};
export const PerformanceCard = ({
  name,
  fullName,
  description,
  value,
  good,
  poor,
  unit = "",
}: Props) => {
  const minValue = 0;
  const maxValue = poor * 1.5;

  const percent = (val: number) =>
    Math.max(
      0,
      Math.min(100, ((val - minValue) / (maxValue - minValue)) * 100),
    );

  const goodPercent = percent(good);
  const poorPercent = percent(poor);
  const valuePercent = percent(value);

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.name}>{name}</span>
        <span className={styles.fullName}>{fullName}</span>
        <div className={styles.tooltipWrapper}>
          <MdInfoOutline />
          <div className={styles.tooltip}>{description}</div>
        </div>
      </div>

      <div className={styles.barContainer}>
        <div
          className={styles.rangeLabel}
          style={{ left: `${goodPercent}%`, transform: "translateX(-50%)" }}
        >
          {good}
          {unit}
        </div>
        <div
          className={styles.rangeLabel}
          style={{ left: `${poorPercent}%`, transform: "translateX(-50%)" }}
        >
          {poor}
          {unit}
        </div>

        <div
          className={`${styles.fill} ${styles.green}`}
          style={{ left: `0%`, width: `${goodPercent}%` }}
        />
        <div
          className={`${styles.fill} ${styles.yellow}`}
          style={{
            left: `${goodPercent}%`,
            width: `${poorPercent - goodPercent}%`,
          }}
        />
        <div
          className={`${styles.fill} ${styles.red}`}
          style={{ left: `${poorPercent}%`, width: `${100 - poorPercent}%` }}
        />

        {/* Current value label */}
        <div className={styles.valueLabel} style={{ left: `${valuePercent}%` }}>
          {value.toFixed(2)}
          {unit}
        </div>

        {/* Current value dot */}
        <div className={styles.dot} style={{ left: `${valuePercent}%` }} />
      </div>
    </div>
  );
};
