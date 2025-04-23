import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Analysis } from "../../constants/types";

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
        <p>{websiteURL}</p>
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
        <img src={auditResult.wordcloud.image} />
      </>
    );
  }
  return <></>;
};
