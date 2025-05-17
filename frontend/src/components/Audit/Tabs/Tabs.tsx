import { useState } from "react";
import { Base } from "../Base/Base";
import { PerformanceBlock } from "../Performance/PerformanceBlock";
import { Design } from "../Design/Design";
import { Analysis } from "../../../constants/types";
import styles from "./styles.module.css";
import { SecurityAndServer } from "../SecurityAndServer/SecurityAndServer";

type Props = {
  auditResult: Analysis;
};

export const Tabs = ({ auditResult }: Props) => {
  const [currentTab, setCurrentTab] = useState<string>("base");

  const renderTab = () => {
    switch (currentTab) {
      case "base":
        return (
          <Base
            seo={auditResult.seo}
            wordcloud={auditResult.wordcloud}
            keywordsDistribution={auditResult.keywordsDistribution}
            pageReport={auditResult.pageReport}
          />
        );
      case "performance":
        return <PerformanceBlock performance={auditResult.performance} />;
      case "design":
        return <Design />;
      case "security":
        return <SecurityAndServer security={auditResult.security} />;
      default:
        return <Base seo={auditResult.seo} wordcloud={auditResult.wordcloud} />;
    }
  };
  return (
    <div>
      <button
        onClick={() => setCurrentTab("base")}
        className={`${styles.tab} ${currentTab === "base" ? styles.activeTab : ""}`}
      >
        SEO
      </button>
      <button
        onClick={() => setCurrentTab("performance")}
        className={`${styles.tab} ${currentTab === "performance" ? styles.activeTab : ""}`}
      >
        Производительность
      </button>
      <button
        onClick={() => setCurrentTab("security")}
        className={`${styles.tab} ${currentTab === "security" ? styles.activeTab : ""}`}
      >
        Безопасность и сервер
      </button>
      <button
        onClick={() => setCurrentTab("design")}
        className={`${styles.tab} ${currentTab === "design" ? styles.activeTab : ""}`}
      >
        Дизайн
      </button>
      <div style={{ marginTop: "1rem" }}>{renderTab()}</div>
    </div>
  );
};
