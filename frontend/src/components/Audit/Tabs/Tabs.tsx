import { useState } from "react";
import { Base } from "../Base/Base";
import { Performance } from "../Performance/Performance";
import { Design } from "../Design/Design";
import { Analysis } from "../../../constants/types";

type Props = {
  auditResult: Analysis;
};
export const Tabs = ({ auditResult }: Props) => {
  const [currentTab, setCurrentTab] = useState<string>("base");

  const renderTab = () => {
    switch (currentTab) {
      case "base":
        return <Base seo={auditResult.seo} wordcloud={auditResult.wordcloud} />;
      case "performance":
        return <Performance performance={auditResult.performance} />;
      case "design":
        return <Design />;
      default:
        return <Base seo={auditResult.seo} wordcloud={auditResult.wordcloud} />;
    }
  };
  return (
    <>
      <button onClick={() => setCurrentTab("base")}>Base</button>
      <button onClick={() => setCurrentTab("performance")}>Performance</button>
      <button onClick={() => setCurrentTab("design")}>Дизайн</button>
      <div style={{ marginTop: "1rem" }}>{renderTab()}</div>
    </>
  );
};
