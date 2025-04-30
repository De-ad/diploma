import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Analysis } from "../../constants/types";
import { Cloud } from "../Cloud/Cloud";

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
      <>
        <h1>Результаты анализа {websiteURL}</h1>
        <p>{auditResult.seo.favicon.message}</p>
        <p>{auditResult.seo.robots.message}</p>
        <p>{auditResult.seo.metadata.titleValue}</p>
        <p>{auditResult.seo.metadata.descriptionValue}</p>
        <p>performance</p>
        <p>{auditResult.performance.performanceScore}</p>
        <p>{auditResult.performance.firstContentfulPaint}</p>
        <p>{auditResult.performance.largestContentfulPaint}</p>
        <p>{auditResult.performance.cumulativeLayoutShift}</p>
        <p>{auditResult.performance.totalBlockingTime}</p>
        <Cloud words={auditResult.wordcloud.data} />
      </>
    );
  }
  return <></>;
};
