import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Analysis } from "../../constants/types";
import { Tabs } from "./Tabs/Tabs";
import { Circle } from "../ProgressBar/Circle";
import styles from "./styles.module.css";
import { HalfCircle } from "../ProgressBar/HalfCircle";
export const Audit = () => {
  let { websiteURL } = useParams();
  const [auditResult, setAuditResult] = useState<Analysis>();

  useEffect(() => {
    const stored = sessionStorage.getItem("auditResult");
    if (stored) {
      const data = JSON.parse(stored);
      setAuditResult(data);
    }
  }, []);

  if (auditResult) {
    return (
      <div>
        <h1>Результаты анализа {websiteURL}</h1>
        <h2>Общее</h2>
        <div className={styles.grade}>
          <div className={styles.param}>
            Общая оценка
            <Circle progress={auditResult.performance.performanceScore} />
          </div>

          <div className={styles.separateParams}>
            <div className={styles.param}>
              <HalfCircle progress={auditResult.performance.performanceScore} />
              Производительность
            </div>
            <div className={styles.param}>
              <HalfCircle progress={20} />
              SEO
            </div>
            <div className={styles.param}>
              <HalfCircle progress={10} />
              Дизайн
            </div>
          </div>
        </div>
        <Tabs auditResult={auditResult} />
      </div>
    );
  }
  return <></>;
};
