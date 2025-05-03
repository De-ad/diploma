import { useState } from "react";
import { Base } from "../Base/Base";
import { Performance } from "../Performance/Performance";
import { Design } from "../Design/Design";
import { Analysis } from "../../../constants/types";
import styles from "./styles.module.css";
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
    <span>
      <button
        onClick={() => setCurrentTab("base")}
        className={`${styles.tab} ${currentTab === "base" ? styles.activeTab : ""}`}
      >
        Base
      </button>
      <button
        onClick={() => setCurrentTab("performance")}
        className={`${styles.tab} ${currentTab === "performance" ? styles.activeTab : ""}`}
      >
        Производительность
      </button>
      <button
        onClick={() => setCurrentTab("design")}
        className={`${styles.tab} ${currentTab === "design" ? styles.activeTab : ""}`}
      >
        Дизайн
      </button>
      <div style={{ marginTop: "1rem" }}>{renderTab()}</div>
    </span>
  );
};
