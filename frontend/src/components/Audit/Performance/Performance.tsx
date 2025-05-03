import { Circle } from "../../ProgressBar/Circle";
import { PerformanceCard } from "./PerformanceCard";

type Props = {
  performance: Performance;
};

export const Performance = ({ performance }: Props) => {
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
      fullName: "First contentful paint",
      description:
        "Измеряет время с момента первого перехода пользователя на страницу до момента отображения какой-либо части содержимого страницы на экране.",
      good: 1.8,
      poor: 3,
      unit: " sec",
    },
    {
      key: "largestContentfulPaint",
      shortName: "LCP",
      fullName: "Largest Contentful Paint",
      description:
        "Показатель Core Web Vital для измерения воспринимаемой скорости загрузки, поскольку он отмечает точку на временной шкале загрузки страницы, когда, вероятно, загрузился основной контент страницы",
      good: 2.5,
      poor: 4,
      unit: " sec",
    },
    {
      key: "totalBlockingTime",
      shortName: "TBT",
      fullName: "Total Blocking Time",
      description:
        "Measures the total amount of time after First Contentful Paint (FCP) where the main thread was blocked for long enough to prevent input responsiveness.",
      good: 0.2,
      poor: 0.6,
      unit: "",
    },
  ];

  const parseValue = (value: string) => {
    if (value.includes("ms")) return parseFloat(value);
    if (value.includes("s")) return parseFloat(value);
    return parseFloat(value);
  };

  return (
    <>
      <div className="p-4 bg-white shadow rounded">
        {metricDefinitions.map((metric) => {
          const raw = performance[metric.key];
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
    </>
  );
};
