import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Analysis } from "../../constants/types";
import { Tabs } from "./Tabs/Tabs";

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
        <Tabs auditResult={auditResult} />
      </>
    );
  }
  return <></>;
};
