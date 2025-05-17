import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Analysis, DesignAnalysis } from "../../constants/types";
import { Tabs } from "./Tabs/Tabs";
import { Circle } from "../ProgressBar/Circle";
import styles from "./styles.module.css";
import { HalfCircle } from "../ProgressBar/HalfCircle";
export const Audit = () => {
  let { websiteURL } = useParams();
  const [auditResult, setAuditResult] = useState<Analysis>();
  const [designScore, setDesignScore] = useState<number>();
  const [llmAnalyzeResult, setLlmAnalyzeResult] =
    useState<DesignAnalysis | null>(null);
  const [vlmAnalyzeResult, setVlmAnalyzeResult] =
    useState<DesignAnalysis | null>(null);

  useEffect(() => {
    let stored = sessionStorage.getItem("auditResult");
    if (stored) {
      const data = JSON.parse(stored);
      setAuditResult(data);
    }
    stored = sessionStorage.getItem("vlmAnalyzeResult");
    if (stored) {
      const data = JSON.parse(stored);
      setVlmAnalyzeResult(data);
    }
    stored = sessionStorage.getItem("llmAnalyzeResult");
    if (stored) {
      const data = JSON.parse(stored);
      setLlmAnalyzeResult(data);
    }
  }, []);
  useEffect(() => {
    if (llmAnalyzeResult && vlmAnalyzeResult) {
      const avg =
        (parseInt(llmAnalyzeResult.message.finalGrade) +
          parseInt(vlmAnalyzeResult.message.finalGrade)) /
        2;
      setDesignScore(avg);
    }
  }, [llmAnalyzeResult, vlmAnalyzeResult]);

  const getCommonScore = () => {
    let securityScore = auditResult?.score.security;
    let seoScore = auditResult?.score.seo;
    let performanceScore = auditResult?.score.performance;
    const securityWeight = 1;
    const seoWeight = 1;
    const performanceWeight = 1;
    const designWeight = 1;

    return (
      (securityScore * securityWeight +
        performanceScore * performanceWeight +
        seoScore * seoWeight +
        designScore * designWeight) /
      4
    );
  };

  if (auditResult) {
    return (
      <div>
        <h1>Результаты анализа {websiteURL}</h1>
        <h2>Общая оценка</h2>
        <div className={styles.grade}>
          <div className={styles.param}>
            <Circle progress={getCommonScore()} colored={true} />
          </div>

          <div className={styles.separateParams}>
            <div className={styles.param}>
              <HalfCircle
                progress={auditResult.score.performance}
                colored={true}
              />
              Производительность
            </div>
            <div className={styles.param}>
              <HalfCircle progress={auditResult.score.seo} colored={true} />
              SEO
            </div>

            <div className={styles.param}>
              <HalfCircle
                progress={auditResult.score.security}
                colored={true}
              />
              Безопасность
            </div>
            <div className={styles.param}>
              <HalfCircle progress={designScore} colored={true} />
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
