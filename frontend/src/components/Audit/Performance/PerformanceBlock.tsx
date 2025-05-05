import { Performance } from "../../../constants/types";
import { Circle } from "../../ProgressBar/Circle";
import { PerformanceCard } from "./PerformanceCard";

type Props = {
  performance: Performance;
};

export const PerformanceBlock = ({ performance }: Props) => {
  const metricDefinitions = [
    {
      key: "cumulativeLayoutShift",
      shortName: "CLS",
      fullName: "Cumulative Layout Shift",
      description:
        "Это показатель наибольшего количества изменений макета для каждого неожиданного изменения макета, которое происходит в течение всего жизненного цикла страницы.",
      good: 0.1,
      poor: 0.25,
      unit: "",
    },
    {
      key: "firstContentfulPaint",
      shortName: "FCP",
      fullName: "First Contentful Paint",
      description:
        "Измеряет время с момента первого перехода пользователя на страницу до момента отображения какой-либо части содержимого страницы на экране.",
      good: 1.8,
      poor: 3.0,
      unit: " sec",
    },
    {
      key: "largestContentfulPaint",
      shortName: "LCP",
      fullName: "Largest Contentful Paint",
      description:
        "Показатель Core Web Vital для измерения воспринимаемой скорости загрузки, поскольку он отмечает точку на временной шкале загрузки страницы, когда, вероятно, загрузился основной контент страницы.",
      good: 2.5,
      poor: 4.0,
      unit: " sec",
    },
    {
      key: "totalBlockingTime",
      shortName: "TBT",
      fullName: "Total Blocking Time",
      description:
        "Измеряет общее время, в течение которого главный поток был заблокирован после FCP настолько, что это мешало отклику на ввод пользователя.",
      good: 200,
      poor: 600,
      unit: " ms",
    },
    {
      key: "speedIndex",
      shortName: "SI",
      fullName: "Speed Index",
      description:
        "Индекс скорости измеряет, насколько быстро контент отображается визуально во время загрузки страницы.",
      good: 3.4,
      poor: 5.8,
      unit: " sec",
    },
  ];

  const parseValue = (value: string) => {
    if (value.includes("ms")) return parseFloat(value);
    if (value.includes("s")) return parseFloat(value);
    return parseFloat(value);
  };

  return (
    <>
      <div>
        {Object.entries(performance).map(([strategyName, metrics], index) => (
          <div key={index}>
            <h2>{strategyName}</h2>
            <Circle
              progress={performance[strategyName].performanceScore}
              colored={true}
            />
            {metricDefinitions.map((metric) => {
              const raw = metrics[metric.key];
              if (!raw) return null;
              const parsed = parseValue(raw);
              return (
                <PerformanceCard
                  key={metric.key}
                  name={metric.shortName}
                  fullName={metric.fullName}
                  description={metric.description}
                  value={parsed}
                  good={metric.good}
                  poor={metric.poor}
                  unit={metric.unit}
                />
              );
            })}
          </div>
        ))}
      </div>
    </>
  );
};
